import React, { useEffect, useRef, useState } from "react";
import {
  Box,
  Typography,
  Button,
  Container,
  CircularProgress,
  Paper,
  Alert,
  Snackbar,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
} from "@mui/material";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import UploadFileIcon from "@mui/icons-material/UploadFile";
import { LinearProgress } from "@mui/material";
import axios from "axios";
import logo from "../assets/logo.png";
import FraudCharts from "./FraudCharts";


const Dashboard: React.FC = () => {
  const [user, setUser] = useState<{ firstname: string } | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isPredicting, setIsPredicting] = useState(false);
  const [successOpen, setSuccessOpen] = useState(false);
  const [uploadProgress, setUploadProgress] = useState<number>(0);
  const [uploadInProgress, setUploadInProgress] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [rows, setRows] = useState<any[]>([]);
  const [totalRows, setTotalRows] = useState(0);
  const [page, setPage] = useState(0);
  const [pageSize, setPageSize] = useState(10);
  const [loading, setLoading] = useState(false);
  const [showFraudOnly, setShowFraudOnly] = useState(false);
  const [selectedTx, setSelectedTx] = useState<any | null>(null);

  const [predictedFraud, setPredictedFraud] = useState<any[]>([]);
  const [allPredicted, setAllPredicted] = useState<any[]>([]);
  const [showPredictions, setShowPredictions] = useState(false);
  const [showOnlyPredFraud, setShowOnlyPredFraud] = useState(true);

  const columns: GridColDef[] = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "merchant", headerName: "Merchant", width: 150 },
    { field: "amt", headerName: "Amount", width: 100 },
    { field: "category", headerName: "Category", width: 120 },
    { field: "city", headerName: "City", width: 120 },
    { field: "is_fraud", headerName: "Fraud", width: 90, type: "boolean" },
  ];

  useEffect(() => {
    axios
      .get("http://localhost:8000/auth/me", { withCredentials: true })
      .then((res) => setUser(res.data))
      .catch(() => {
        window.location.href = "/login";
      });
  }, []);

  const fetchTransactions = async () => {
    setLoading(true);
    try {
      const res = await axios.get(
        `http://localhost:8000/transactions?limit=${pageSize}&offset=${page * pageSize}${showFraudOnly ? "&is_fraud=true" : ""}`
      );
      setRows(res.data.transactions);
      setTotalRows(res.data.total);
    } catch (err) {
      console.error("Error fetching transactions:", err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchTransactions();
  }, [page, pageSize, showFraudOnly, successOpen]);

  useEffect(() => {
    if (uploadProgress === 100) {
      const timeout = setTimeout(() => setUploadInProgress(false), 1000);
      return () => clearTimeout(timeout);
    }
  }, [uploadProgress]);


  const handleLogout = async () => {
    await axios.post("http://localhost:8000/auth/logout", {}, { withCredentials: true });
    window.location.href = "/";
  };

  const handleSubmitUpload = async () => {
      if (!file) {
        setUploadError("Please select a CSV file before uploading.");
        return;
      }

      const formData = new FormData();
      formData.append("file", file);
      setIsUploading(true);

      try {
        const uploadedRes = await axios.post("http://localhost:8000/upload-csv", formData, {
          headers: { "Content-Type": "multipart/form-data" },
          withCredentials: true,
        });

        const res = await axios.get("http://localhost:8000/predict-fraud", {
          withCredentials: true,
        });

        setPredictedFraud(res.data.fraudulent);
        setAllPredicted(res.data.all);
        setShowPredictions(true);
        setSuccessOpen(true);
        setFile(null);
        if (fileInputRef.current) fileInputRef.current.value = "";
      } catch (err: any) {
        setUploadError(err.response?.data?.detail || "Upload or Prediction failed.");
      } finally {
        setIsUploading(false);
      }
  } 

  if (!user) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="md" sx={{ mt: 6, mb: 8 }}>
      <Box display="flex" justifyContent="flex-end" mb={2}>
        <Button variant="contained" color="error" onClick={handleLogout} size="small">
          Logout
        </Button>
      </Box>

      <Paper elevation={4} sx={{ p: 5, borderRadius: 4, textAlign: "center" }}>
        <img src={logo} alt="FRAUDetective Logo" width={100} height={100} style={{ borderRadius: 16, marginBottom: 16 }} />
        <Typography variant="h4" fontWeight={700} mb={1}>
          Welcome, {user.firstname}!
        </Typography>
        <Typography variant="body1" sx={{ mb: 4, color: "#555" }}>
          Upload a CSV file to analyze credit card transactions.
        </Typography>

        {uploadError && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {uploadError}
          </Alert>
        )}
      </Paper>

      <Box display="flex" flexDirection="column" alignItems="center" gap={2} mt={2}>
        <Button
          variant="outlined"
          component="label"
          startIcon={<UploadFileIcon />}
          sx={{ textTransform: "none", width: "100%" }}
        >
          Choose CSV File
          <input
            ref={fileInputRef}
            type="file"
            accept=".csv"
            hidden
            onChange={(e) => {
              const selectedFile = e.target.files?.[0];
              if (!selectedFile) return;
              setFile(selectedFile);
              setUploadError(null);
            }}
          />
        </Button>

        {file && (
          <Typography variant="body2" color="text.secondary">
            Selected: {file.name}
          </Typography>
        )}

        <Button
          variant="contained"
          color="success"
          onClick={handleSubmitUpload}
          disabled={isUploading}
          sx={{ textTransform: "none", fontWeight: 600, width: "100%" }}
        >
          {isUploading ? <CircularProgress size={24} color="inherit" /> : "Upload & Predict"}
        </Button>
        {
          uploadInProgress && (
            <Box width="100%" sx={{ mt: 2 }}>
              <Typography variant="body2" color="text.secondary">
                Uploading: {uploadProgress}%
              </Typography>
              <LinearProgress variant="determinate" value={uploadProgress} />
            </Box>
          )
        }
      </Box>

      {showPredictions && (
        <>
          <Typography variant="h6" mt={6} mb={2} fontWeight={600}>
            Detected Fraudulent Transactions
          </Typography>

          <Button
            variant="outlined"
            onClick={() => setShowOnlyPredFraud(!showOnlyPredFraud)}
            sx={{ mb: 2 }}
          >
            {showOnlyPredFraud ? "Show All Predictions" : "Show Only Predicted Frauds"}
          </Button>

          <Box height={400}>
            <DataGrid
              rows={(showOnlyPredFraud ? predictedFraud : allPredicted).map((row, index) => ({ id: index + 1, ...row }))}
              columns={columns}
              initialState={{
                pagination: {
                  paginationModel: { pageSize: 10, page: 0 },
                },
              }}
              pageSizeOptions={[20]}
            />
          </Box>
          <FraudCharts data={predictedFraud} />
        </>
      )}

      <Dialog open={!!selectedTx} onClose={() => setSelectedTx(null)} fullWidth maxWidth="sm">
        <DialogTitle>Transaction #{selectedTx?.id}</DialogTitle>
        <DialogContent>
          <DialogContentText>
            <strong>Merchant:</strong> {selectedTx?.merchant}<br />
            <strong>Amount:</strong> ${selectedTx?.amt}<br />
            <strong>Category:</strong> {selectedTx?.category}<br />
            <strong>City:</strong> {selectedTx?.city}<br />
            <strong>Time:</strong> {selectedTx?.trans_date_trans_time}<br />
            <strong>Fraud:</strong> {selectedTx?.is_fraud ? "Yes" : "No"}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSelectedTx(null)} color="primary">Close</Button>
        </DialogActions>
      </Dialog>

      <Snackbar
        open={successOpen}
        autoHideDuration={3000}
        onClose={() => setSuccessOpen(false)}
        message="CSV uploaded successfully"
      />

    </Container>
  );
};

export default Dashboard;

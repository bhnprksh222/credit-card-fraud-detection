import React, { useState } from "react";
import {
  Box,
  Button,
  Container,
  TextField,
  Typography,
  Alert,
  Stack,
  Divider,
  Paper,
} from "@mui/material";
import axios from "axios";
import logo from "../assets/logo.png";
import GoogleIcon from '../assets/google-icon.svg'

const Login: React.FC = () => {
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const form = new URLSearchParams();
    form.append("username", formData.username);
    form.append("password", formData.password);

    try {
      await axios.post("http://localhost:8000/auth/login", form, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        withCredentials: true,
      });
      window.location.href = "/dashboard";
    } catch (err: any) {
      setError(err.response?.data?.detail || "Login failed");
    }
  };

  const handleGoogleLogin = () => {
    window.location.href = "http://localhost:8000/auth/google";
  };

  return (
    <Container
      maxWidth="sm"
      sx={{
        mt: 8,
        mb: 8, 
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
      }}
    >
      <Box display="flex" justifyContent="center" mb={4}>
        <img
          src={logo}
          alt="FRAUDetective Logo"
          width={100}
          height={100}
          style={{ borderRadius: 16 }}
        />
      </Box>

      <Paper elevation={4} sx={{ p: 5, borderRadius: 4, backgroundColor: "#fff" }}>
        <Typography
          variant="h4"
          align="center"
          gutterBottom
          sx={{ fontFamily: "'Poppins', sans-serif", fontWeight: 600 }}
        >
          Welcome Back
        </Typography>
        <Typography variant="body1" align="center" color="text.secondary" sx={{ mb: 4 }}>
          Login to your account
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <form onSubmit={handleSubmit}>
          <Stack spacing={3}>
            <TextField
              label="Username or Email"
              name="username"
              fullWidth
              onChange={handleChange}
              variant="outlined"
            />
            <TextField
              label="Password"
              name="password"
              type="password"
              fullWidth
              onChange={handleChange}
              variant="outlined"
            />
            <Button
              type="submit"
              variant="contained"
              color="primary"
              fullWidth
              size="large"
              sx={{ textTransform: "none", fontWeight: 600 }}
            >
              Login
            </Button>
          </Stack>
        </form>

        <Divider sx={{ my: 4 }}>or</Divider>

        <Button
          variant="outlined"
          fullWidth
          onClick={handleGoogleLogin}
          startIcon={
            <img
              src={GoogleIcon}
              alt="Google"
              style={{ width: 20, height: 20 }}
            />
          }
          sx={{
            textTransform: "none",
            fontWeight: 500,
            borderColor: "#FEC84B",
            color: "#FEC84B",
            "&:hover": {
              borderColor: "#fdbb2d",
              backgroundColor: "#fff9eb",
            },
          }}
        >
          Continue with Google
        </Button>

        <Typography align="center" variant="body2" sx={{ mt: 4 }}>
          Don’t have an account?{" "}
          <a href="/signup" style={{ color: "#1976d2", textDecoration: "none", fontWeight: 500 }}>
            Sign up
          </a>
        </Typography>
      </Paper>
    </Container>
  );
};

export default Login;


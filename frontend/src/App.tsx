import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Signup from "./pages/Signup";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import OAuthSuccess from "./pages/OAuthSuccess";
import { Box, Container } from "@mui/material";

function App() {
  return (
    <Router>
      <Box
        sx={{
          backgroundColor: "#FCF3E0", 
          minHeight: "100vh",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "flex-start",
          paddingTop: 6,
        }}
      >
        <Container maxWidth="lg" sx={{ width: "100%", px: 2 }}>
          <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/oauth-success" element={<OAuthSuccess />} />
          </Routes>
        </Container>
      </Box>
    </Router>
  );
}

export default App;


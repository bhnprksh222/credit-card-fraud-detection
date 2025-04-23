import React, { useState } from "react";
import {
  Box, Button, Container, TextField, Typography,
  Alert, Stack, Divider, Paper, CircularProgress,
  Snackbar
} from "@mui/material";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import API from "../api/axios";
import logo from "../assets/logo.png";
import GoogleIcon from "../assets/google-icon.svg";

const signupSchema = z.object({
  username: z.string().min(3, "Username must be at least 3 characters"),
  email: z.string().email("Invalid email"),
  firstname: z.string().min(1, "First name is required"),
  lastname: z.string().min(1, "Last name is required"),
  password: z.string().min(6, "Password must be at least 6 characters"),
  confirmPassword: z.string(),
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords do not match",
  path: ["confirmPassword"],
});

type SignupForm = z.infer<typeof signupSchema>;

const Signup: React.FC = () => {
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [successOpen, setSuccessOpen] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<SignupForm>({
    resolver: zodResolver(signupSchema),
  });

  const onSubmit = async (data: SignupForm) => {
    setLoading(true);
    try {
      await API.post("/auth/signup", {
        username: data.username,
        email: data.email,
        password: data.password,
        firstname: data.firstname,
        lastname: data.lastname,
      });
      <Snackbar
        open={successOpen}
        autoHideDuration={3000}
        onClose={() => setSuccessOpen(false)}
        message="Signup successful! Redirecting to login..."
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      />
      setSuccessOpen(true);
      reset();
      setTimeout(() => {
        window.location.href = "/";
      }, 1500);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Signup failed");
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleSignup = () => {
    window.location.href = "http://localhost:8000/auth/google";
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4, mb: 6 }}>
      <Box display="flex" justifyContent="center" mb={3}>
        <img src={logo} alt="FRAUDetective Logo" width={100} height={100} style={{ borderRadius: 16 }} />
      </Box>

      <Paper elevation={4} sx={{ p: 5, borderRadius: 4, backgroundColor: "#fff" }}>
        <Typography variant="h4" align="center" gutterBottom sx={{ fontFamily: "'Poppins', sans-serif", fontWeight: 600 }}>
          Create Account
        </Typography>
        <Typography variant="body1" align="center" color="text.secondary" sx={{ mb: 4 }}>
          Start your journey with FRAUDetective
        </Typography>

        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

        <form onSubmit={handleSubmit(onSubmit)}>
          <Stack spacing={3}>
            <TextField
              label="Username"
              {...register("username")}
              error={!!errors.username}
              helperText={errors.username?.message}
              fullWidth disabled={isSubmitting}
            />
            <TextField
              label="Email"
              type="email"
              {...register("email")}
              error={!!errors.email}
              helperText={errors.email?.message}
              fullWidth disabled={isSubmitting}
            />
            <TextField
              label="First Name"
              {...register("firstname")}
              error={!!errors.firstname}
              helperText={errors.firstname?.message}
              fullWidth disabled={isSubmitting}
            />
            <TextField
              label="Last Name"
              {...register("lastname")}
              error={!!errors.lastname}
              helperText={errors.lastname?.message}
              fullWidth disabled={isSubmitting}
            />
            <TextField
              label="Password"
              type="password"
              {...register("password")}
              error={!!errors.password}
              helperText={errors.password?.message}
              fullWidth disabled={isSubmitting}
            />
            <TextField
              label="Confirm Password"
              type="password"
              {...register("confirmPassword")}
              error={!!errors.confirmPassword}
              helperText={errors.confirmPassword?.message}
              fullWidth disabled={isSubmitting}
            />

            <Button
              type="submit"
              variant="contained"
              color="primary"
              fullWidth
              size="large"
              disabled={isSubmitting}
              sx={{ textTransform: "none", fontWeight: 600 }}
              startIcon={loading ? <CircularProgress size={20} /> : null}
            >
              {loading ? "Creating..." : "Sign Up"}
            </Button>
          </Stack>
        </form>

        <Divider sx={{ my: 4 }}>or</Divider>

        <Button
          variant="outlined"
          fullWidth
          onClick={handleGoogleSignup}
          startIcon={<img src={GoogleIcon} alt="Google" style={{ width: 20, height: 20 }} />}
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
          Already have an account?{" "}
          <a href="/" style={{ color: "#1976d2", textDecoration: "none", fontWeight: 500 }}>
            Login
          </a>
        </Typography>
      </Paper>
    </Container>
  );
};

export default Signup;


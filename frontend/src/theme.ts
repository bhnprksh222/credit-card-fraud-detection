import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    background: {
      default: "#FCF3E0",
    },
    primary: {
      main: "#FEC84B",
    },
    secondary: {
      main: "#FAD6D7",
    },
    text: {
      primary: "#1F2937",
    },
  },
  typography: {
    fontFamily: "'Inter', sans-serif",
    h1: { fontFamily: "'Poppins', sans-serif", fontWeight: 700 },
    h2: { fontFamily: "'Poppins', sans-serif", fontWeight: 600 },
    h3: { fontFamily: "'Poppins', sans-serif" },
  },
  shape: {
    borderRadius: 16,
  },
});

export default theme;

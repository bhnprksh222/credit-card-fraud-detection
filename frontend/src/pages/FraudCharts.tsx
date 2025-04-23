import React from "react";
import {
  Box,
  Typography,
} from "@mui/material";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
} from "recharts";

interface Transaction {
  merchant: string;
  category: string;
  amt: number;
  city: string;
  is_fraud: boolean;
  predicted_fraud: number;
  hour: number;
  day_of_week: number;
  month: number;
}

interface FraudChartsProps {
  data: Transaction[];
}

const FraudCharts: React.FC<FraudChartsProps> = ({ data }) => {
  const categoryCount = data.reduce((acc: any, curr) => {
    acc[curr.category] = (acc[curr.category] || 0) + 1;
    return acc;
  }, {});

  const categoryData = Object.entries(categoryCount).map(([key, value]) => ({
    category: key,
    count: value as number,
  }));

  const hourlyData = Array.from({ length: 24 }, (_, i) => ({
    hour: i,
    count: data.filter((d) => d.hour === i).length,
  }));

  const dailyData = Array.from({ length: 7 }, (_, i) => ({
    day: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][i],
    count: data.filter((d) => d.day_of_week === i).length,
  }));

  const monthlyData = Array.from({ length: 12 }, (_, i) => ({
    month: i + 1,
    count: data.filter((d) => d.month === i + 1).length,
  }));

  return (
    <Box mt={6}>
      <Typography variant="h5" fontWeight={700} mb={2}>Fraud Distribution by Category</Typography>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={categoryData}>
          <XAxis dataKey="category" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="count" fill="#EF4444" />
        </BarChart>
      </ResponsiveContainer>

      <Typography variant="h5" fontWeight={700} mt={6} mb={2}>Fraudulent Transactions by Hour</Typography>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={hourlyData}>
          <XAxis dataKey="hour" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="count" fill="#3B82F6" />
        </BarChart>
      </ResponsiveContainer>

      <Typography variant="h5" fontWeight={700} mt={6} mb={2}>Fraud by Day of Week</Typography>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={dailyData}>
          <XAxis dataKey="day" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="count" fill="#10B981" />
        </BarChart>
      </ResponsiveContainer>

      <Typography variant="h5" fontWeight={700} mt={6} mb={2}>Fraud by Month</Typography>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={monthlyData}>
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="count" fill="#F59E0B" />
        </BarChart>
      </ResponsiveContainer>
    </Box>
  );
};

export default FraudCharts;

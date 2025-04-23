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
  LineChart,
  Line,
  AreaChart,
  Area,
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

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#A28FD0", "#FF6384"];

const FraudCharts: React.FC<FraudChartsProps> = ({ data }) => {
  // Aggregate data
  const categoryCount = data.reduce((acc: Record<string, number>, curr) => {
    acc[curr.category] = (acc[curr.category] || 0) + 1;
    return acc;
  }, {});
  const categoryData = Object.entries(categoryCount).map(([key, value]) => ({
    category: key,
    count: value,
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
      {/* Pie Chart for Category Distribution */}
      <Typography variant="h5" fontWeight={700} mb={2}>
        Fraud Distribution by Category
      </Typography>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={categoryData}
            dataKey="count"
            nameKey="category"
            cx="50%"
            cy="50%"
            outerRadius={100}
            
          >
            {categoryData.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend layout="horizontal" verticalAlign="bottom" />
        </PieChart>
      </ResponsiveContainer>

      {/* Line Chart for Hourly Fraud Trend */}
      <Typography variant="h5" fontWeight={700} mt={6} mb={2}>
        Fraudulent Transactions by Hour
      </Typography>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={hourlyData}>
          <XAxis dataKey="hour" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="count" stroke="#3B82F6" dot={false} />
        </LineChart>
      </ResponsiveContainer>

      {/* Bar Chart for Day of Week */}
      <Typography variant="h5" fontWeight={700} mt={6} mb={2}>
        Fraud by Day of Week
      </Typography>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={dailyData}>
          <XAxis dataKey="day" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="count" fill="#10B981" />
        </BarChart>
      </ResponsiveContainer>

      {/* Area Chart for Monthly Trend */}
      <Typography variant="h5" fontWeight={700} mt={6} mb={2}>
        Fraud by Month
      </Typography>
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={monthlyData}>
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Area type="monotone" dataKey="count" stroke="#F59E0B" fill="#FEEBC8" />
        </AreaChart>
      </ResponsiveContainer>
    </Box>
  );
};

export default FraudCharts;

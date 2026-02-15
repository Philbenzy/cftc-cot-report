import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import { TrendingUp } from 'lucide-react';

const formatNumber = (num) => {
  if (Math.abs(num) >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M';
  }
  if (Math.abs(num) >= 1000) {
    return (num / 1000).toFixed(0) + 'K';
  }
  return num.toString();
};

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload || !payload.length) return null;

  return (
    <div style={{
      background: '#252525',
      border: '1px solid #333',
      borderRadius: '4px',
      padding: '12px',
      fontSize: '12px',
    }}>
      <div style={{ color: '#888', marginBottom: '8px' }}>{label}</div>
      {payload.map((entry, index) => (
        <div key={index} style={{ color: entry.color, marginBottom: '4px' }}>
          {entry.name}: {entry.value.toLocaleString()}
        </div>
      ))}
    </div>
  );
};

const NetPositionChart = ({ data }) => {
  if (!data || !data.length) return null;

  const chartData = data.map(item => ({
    date: item.date.slice(5), // MM-DD format
    noncomm_net: item.noncomm_net,
    comm_net: item.comm_net,
  }));

  return (
    <div className="chart-card full-width">
      <div className="chart-title">
        <TrendingUp size={16} />
        净持仓趋势
      </div>
      <div className="chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 10, right: 30, left: 10, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#333" />
            <XAxis
              dataKey="date"
              stroke="#666"
              fontSize={11}
              tickLine={false}
            />
            <YAxis
              stroke="#666"
              fontSize={11}
              tickLine={false}
              tickFormatter={formatNumber}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend
              wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }}
              iconType="circle"
            />
            <Line
              type="monotone"
              dataKey="noncomm_net"
              name="非商业净持仓"
              stroke="#D4AF37"
              strokeWidth={2}
              dot={{ fill: '#D4AF37', r: 3 }}
              activeDot={{ r: 5 }}
            />
            <Line
              type="monotone"
              dataKey="comm_net"
              name="商业净持仓"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={{ fill: '#3b82f6', r: 3 }}
              activeDot={{ r: 5 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default NetPositionChart;

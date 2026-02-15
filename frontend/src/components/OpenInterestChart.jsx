import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import { Activity } from 'lucide-react';

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
      <div style={{ color: '#D4AF37' }}>
        未平仓合约: {payload[0].value.toLocaleString()}
      </div>
    </div>
  );
};

const OpenInterestChart = ({ data }) => {
  if (!data || !data.length) return null;

  const chartData = data.map(item => ({
    date: item.date.slice(5),
    open_interest: item.open_interest,
  }));

  // 计算平均值用于颜色区分
  const avgOI = chartData.reduce((sum, item) => sum + item.open_interest, 0) / chartData.length;

  return (
    <div className="chart-card">
      <div className="chart-title">
        <Activity size={16} />
        未平仓合约量
      </div>
      <div className="chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} margin={{ top: 10, right: 20, left: 10, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
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
            <Bar dataKey="open_interest" radius={[4, 4, 0, 0]}>
              {chartData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={entry.open_interest >= avgOI ? '#D4AF37' : '#B8952F'}
                  opacity={0.85}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default OpenInterestChart;

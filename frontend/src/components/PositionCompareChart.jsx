import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import { BarChart3 } from 'lucide-react';

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

const PositionCompareChart = ({ data }) => {
  if (!data || !data.length) return null;

  // 只取最近6周数据，避免图表过于拥挤
  const recentData = data.slice(-6);

  const chartData = recentData.map(item => ({
    date: item.date.slice(5),
    noncomm_long: item.noncomm_long,
    noncomm_short: item.noncomm_short,
    comm_long: item.comm_long,
    comm_short: item.comm_short,
  }));

  return (
    <div className="chart-card">
      <div className="chart-title">
        <BarChart3 size={16} />
        多空持仓对比（近6周）
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
            <Legend
              wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }}
              iconType="square"
            />
            <Bar
              dataKey="noncomm_long"
              name="非商业多头"
              fill="#22c55e"
              radius={[2, 2, 0, 0]}
            />
            <Bar
              dataKey="noncomm_short"
              name="非商业空头"
              fill="#ef4444"
              radius={[2, 2, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default PositionCompareChart;

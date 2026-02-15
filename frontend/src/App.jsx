import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import './styles/theme.css';

// 示例数据 - 实际使用时从gold_cot_data.json加载
const SAMPLE_DATA = {
  "summary": {
    "latest_date": "2025-02-11",
    "noncomm_net": 254832,
    "comm_net": -287456,
    "open_interest": 542103,
    "noncomm_net_change": 12543,
    "comm_net_change": -15234,
    "oi_change": 8921,
    "long_short_ratio": 2.34
  },
  "weekly_data": [
    {"date": "2024-11-19", "noncomm_long": 298000, "noncomm_short": 78000, "noncomm_spreading": 45000, "comm_long": 120000, "comm_short": 385000, "open_interest": 498000, "noncomm_net": 220000, "comm_net": -265000, "noncomm_net_change": 0, "comm_net_change": 0, "oi_change": 0},
    {"date": "2024-11-26", "noncomm_long": 305000, "noncomm_short": 75000, "noncomm_spreading": 46000, "comm_long": 118000, "comm_short": 390000, "open_interest": 505000, "noncomm_net": 230000, "comm_net": -272000, "noncomm_net_change": 10000, "comm_net_change": -7000, "oi_change": 7000},
    {"date": "2024-12-03", "noncomm_long": 295000, "noncomm_short": 82000, "noncomm_spreading": 44000, "comm_long": 125000, "comm_short": 378000, "open_interest": 495000, "noncomm_net": 213000, "comm_net": -253000, "noncomm_net_change": -17000, "comm_net_change": 19000, "oi_change": -10000},
    {"date": "2024-12-10", "noncomm_long": 302000, "noncomm_short": 79000, "noncomm_spreading": 47000, "comm_long": 122000, "comm_short": 388000, "open_interest": 512000, "noncomm_net": 223000, "comm_net": -266000, "noncomm_net_change": 10000, "comm_net_change": -13000, "oi_change": 17000},
    {"date": "2024-12-17", "noncomm_long": 310000, "noncomm_short": 72000, "noncomm_spreading": 48000, "comm_long": 115000, "comm_short": 395000, "open_interest": 520000, "noncomm_net": 238000, "comm_net": -280000, "noncomm_net_change": 15000, "comm_net_change": -14000, "oi_change": 8000},
    {"date": "2024-12-24", "noncomm_long": 308000, "noncomm_short": 74000, "noncomm_spreading": 47000, "comm_long": 117000, "comm_short": 392000, "open_interest": 518000, "noncomm_net": 234000, "comm_net": -275000, "noncomm_net_change": -4000, "comm_net_change": 5000, "oi_change": -2000},
    {"date": "2024-12-31", "noncomm_long": 312000, "noncomm_short": 70000, "noncomm_spreading": 49000, "comm_long": 113000, "comm_short": 398000, "open_interest": 525000, "noncomm_net": 242000, "comm_net": -285000, "noncomm_net_change": 8000, "comm_net_change": -10000, "oi_change": 7000},
    {"date": "2025-01-07", "noncomm_long": 318000, "noncomm_short": 68000, "noncomm_spreading": 50000, "comm_long": 110000, "comm_short": 402000, "open_interest": 530000, "noncomm_net": 250000, "comm_net": -292000, "noncomm_net_change": 8000, "comm_net_change": -7000, "oi_change": 5000},
    {"date": "2025-01-14", "noncomm_long": 315000, "noncomm_short": 71000, "noncomm_spreading": 49000, "comm_long": 112000, "comm_short": 398000, "open_interest": 528000, "noncomm_net": 244000, "comm_net": -286000, "noncomm_net_change": -6000, "comm_net_change": 6000, "oi_change": -2000},
    {"date": "2025-01-21", "noncomm_long": 320000, "noncomm_short": 69000, "noncomm_spreading": 51000, "comm_long": 108000, "comm_short": 405000, "open_interest": 535000, "noncomm_net": 251000, "comm_net": -297000, "noncomm_net_change": 7000, "comm_net_change": -11000, "oi_change": 7000},
    {"date": "2025-01-28", "noncomm_long": 317000, "noncomm_short": 72000, "noncomm_spreading": 50000, "comm_long": 111000, "comm_short": 400000, "open_interest": 532000, "noncomm_net": 245000, "comm_net": -289000, "noncomm_net_change": -6000, "comm_net_change": 8000, "oi_change": -3000},
    {"date": "2025-02-04", "noncomm_long": 322000, "noncomm_short": 80000, "noncomm_spreading": 52000, "comm_long": 115000, "comm_short": 387000, "open_interest": 533182, "noncomm_net": 242289, "comm_net": -272222, "noncomm_net_change": -2711, "comm_net_change": 16778, "oi_change": 1182},
    {"date": "2025-02-11", "noncomm_long": 328000, "noncomm_short": 73168, "noncomm_spreading": 53000, "comm_long": 112000, "comm_short": 399456, "open_interest": 542103, "noncomm_net": 254832, "comm_net": -287456, "noncomm_net_change": 12543, "comm_net_change": -15234, "oi_change": 8921}
  ],
  "updated_at": "2025-02-15 10:30:00",
  "market": "GOLD (COMEX)",
  "weeks": 13
};

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        // 尝试从本地JSON文件加载
        const response = await fetch('/data/gold_cot_data.json');
        if (response.ok) {
          const jsonData = await response.json();
          setData(jsonData);
        } else {
          // 使用示例数据
          console.log('Using sample data');
          setData(SAMPLE_DATA);
        }
      } catch (err) {
        console.log('Loading sample data due to:', err.message);
        setData(SAMPLE_DATA);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading) {
    return (
      <div className="loading">
        <div className="loading-spinner"></div>
        <span>Loading CFTC Data...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="loading">
        <span style={{ color: '#ef4444' }}>Error: {error}</span>
      </div>
    );
  }

  return <Dashboard data={data} />;
}

export default App;

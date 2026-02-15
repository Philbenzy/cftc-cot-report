import React from 'react';
import { Coins } from 'lucide-react';
import MetricCards from './MetricCards';
import NetPositionChart from './NetPositionChart';
import OpenInterestChart from './OpenInterestChart';
import PositionCompareChart from './PositionCompareChart';
import WeeklyChangeTable from './WeeklyChangeTable';

const Dashboard = ({ data }) => {
  if (!data) {
    return (
      <div className="loading">
        <div className="loading-spinner"></div>
        <span>Loading CFTC Data...</span>
      </div>
    );
  }

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div>
          <h1 className="dashboard-title">
            <Coins size={28} />
            CFTC COT Report - {data.market}
          </h1>
          <p className="dashboard-subtitle">
            Commitments of Traders | 近{data.weeks}周持仓数据分析
          </p>
        </div>
        <div className="update-time">
          <div>最新数据: {data.summary?.latest_date}</div>
          <div>更新时间: {data.updated_at}</div>
        </div>
      </header>

      {/* Metric Cards */}
      <MetricCards summary={data.summary} />

      {/* Charts Grid */}
      <div className="charts-grid">
        <NetPositionChart data={data.weekly_data} />
        <OpenInterestChart data={data.weekly_data} />
        <PositionCompareChart data={data.weekly_data} />
      </div>

      {/* Weekly Change Table */}
      <WeeklyChangeTable data={data.weekly_data} />
    </div>
  );
};

export default Dashboard;

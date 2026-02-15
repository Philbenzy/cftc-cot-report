import React from 'react';
import { TrendingUp, TrendingDown, Activity, BarChart3, Scale } from 'lucide-react';

const formatNumber = (num) => {
  if (num === undefined || num === null) return '-';
  return num.toLocaleString('en-US');
};

const formatChange = (num) => {
  if (num === undefined || num === null) return '-';
  const prefix = num > 0 ? '+' : '';
  return prefix + num.toLocaleString('en-US');
};

const MetricCard = ({ label, value, change, icon: Icon, type = 'default' }) => {
  const isPositive = change > 0;
  const isNegative = change < 0;

  return (
    <div className="metric-card">
      <div className="metric-label">
        {Icon && <Icon size={14} style={{ marginRight: 6, verticalAlign: 'middle' }} />}
        {label}
      </div>
      <div className={`metric-value ${type === 'ratio' ? '' : isPositive ? 'positive' : isNegative ? 'negative' : ''}`}>
        {type === 'ratio' ? value : formatNumber(value)}
      </div>
      {change !== undefined && (
        <div className={`metric-change ${isPositive ? 'positive' : isNegative ? 'negative' : ''}`}>
          {isPositive ? <TrendingUp size={14} /> : isNegative ? <TrendingDown size={14} /> : null}
          <span>周变化: {formatChange(change)}</span>
        </div>
      )}
    </div>
  );
};

const MetricCards = ({ summary }) => {
  if (!summary) return null;

  return (
    <div className="metrics-grid">
      <MetricCard
        label="非商业净持仓"
        value={summary.noncomm_net}
        change={summary.noncomm_net_change}
        icon={TrendingUp}
      />
      <MetricCard
        label="商业净持仓"
        value={summary.comm_net}
        change={summary.comm_net_change}
        icon={TrendingDown}
      />
      <MetricCard
        label="未平仓合约"
        value={summary.open_interest}
        change={summary.oi_change}
        icon={Activity}
      />
      <MetricCard
        label="多空比"
        value={summary.long_short_ratio}
        icon={Scale}
        type="ratio"
      />
    </div>
  );
};

export default MetricCards;

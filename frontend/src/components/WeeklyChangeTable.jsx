import React from 'react';
import { Table } from 'lucide-react';

const formatNumber = (num) => {
  if (num === undefined || num === null) return '-';
  return num.toLocaleString('en-US');
};

const formatChange = (num) => {
  if (num === undefined || num === null) return '-';
  const prefix = num > 0 ? '+' : '';
  return prefix + num.toLocaleString('en-US');
};

const WeeklyChangeTable = ({ data }) => {
  if (!data || !data.length) return null;

  // 倒序显示，最新的在前面
  const tableData = [...data].reverse();

  return (
    <div className="table-card">
      <div className="chart-title">
        <Table size={16} />
        周度持仓变化明细
      </div>
      <table className="data-table">
        <thead>
          <tr>
            <th>日期</th>
            <th style={{ textAlign: 'right' }}>非商业净持仓</th>
            <th style={{ textAlign: 'right' }}>周变化</th>
            <th style={{ textAlign: 'right' }}>商业净持仓</th>
            <th style={{ textAlign: 'right' }}>周变化</th>
            <th style={{ textAlign: 'right' }}>未平仓合约</th>
            <th style={{ textAlign: 'right' }}>周变化</th>
          </tr>
        </thead>
        <tbody>
          {tableData.map((row, index) => (
            <tr key={row.date}>
              <td>{row.date}</td>
              <td className="number">{formatNumber(row.noncomm_net)}</td>
              <td className={`number ${row.noncomm_net_change > 0 ? 'positive' : row.noncomm_net_change < 0 ? 'negative' : ''}`}>
                {formatChange(row.noncomm_net_change)}
              </td>
              <td className="number">{formatNumber(row.comm_net)}</td>
              <td className={`number ${row.comm_net_change > 0 ? 'positive' : row.comm_net_change < 0 ? 'negative' : ''}`}>
                {formatChange(row.comm_net_change)}
              </td>
              <td className="number">{formatNumber(row.open_interest)}</td>
              <td className={`number ${row.oi_change > 0 ? 'positive' : row.oi_change < 0 ? 'negative' : ''}`}>
                {formatChange(row.oi_change)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default WeeklyChangeTable;

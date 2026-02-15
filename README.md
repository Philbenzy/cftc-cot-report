# CFTC COT 金属期货持仓分析仪表盘

基于 CFTC（美国商品期货交易委员会）COT（Commitments of Traders）报告的金属期货持仓可视化分析工具。

## 功能特性

- **多品种支持**：黄金、白银、铜、铂金、钯金
- **时间范围选择**：3个月、6个月、1年
- **可视化图表**：
  - 净持仓趋势与边际变化组合图
  - 非商业持仓周度变化分析
  - 未平仓合约量（含中位数标注）
  - 多空持仓对比（近12周）
- **数据表格**：周度持仓变化明细，含变化率

## 项目结构

```
cftc_report/
├── backend/
│   ├── cftc_data_fetcher.py   # 数据获取脚本
│   └── requirements.txt        # Python依赖
├── data/
│   └── cot_data.json           # 数据文件
├── frontend/                    # React项目（可选）
├── dashboard.html               # 主仪表盘页面
└── README.md
```

## 快速开始

### 1. 安装 Python 依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 获取 CFTC 数据

```bash
cd backend
python cftc_data_fetcher.py
```

首次运行会从 CFTC 下载数据，生成 `data/cot_data.json` 文件。

### 3. 启动本地服务器

```bash
cd /path/to/cftc_report
python -m http.server 8080
```

### 4. 访问仪表盘

打开浏览器访问：http://localhost:8080/dashboard.html

## 每周更新流程

CFTC 数据每周五美东时间 15:30 发布（数据为周二收盘）。

```bash
# 更新数据
cd backend
python cftc_data_fetcher.py

# 刷新浏览器页面即可查看最新数据
```

## 数据说明

### COT 报告类型

本项目使用 **Legacy Futures** 报告，包含：

| 类别 | 说明 |
|------|------|
| 非商业（Noncommercial） | 投机者持仓，通常为对冲基金、资管机构 |
| 商业（Commercial） | 套保者持仓，通常为生产商、贸易商 |
| 未平仓合约（Open Interest） | 市场总持仓量，反映参与热度 |

### 关键指标

- **净持仓**：多头持仓 - 空头持仓
- **多空比**：多头持仓 / 空头持仓
- **周变化**：本周净持仓 - 上周净持仓
- **变化率**：周变化 / 上周净持仓绝对值

## 支持的品种

| 品种 | 代码 | 交易所 |
|------|------|--------|
| 黄金 | gold | COMEX |
| 白银 | silver | COMEX |
| 铜 | copper | COMEX |
| 铂金 | platinum | NYMEX |
| 钯金 | palladium | NYMEX |

## 技术栈

- **后端**：Python + cot-reports 库
- **前端**：HTML + Chart.js
- **数据源**：CFTC 官方数据

## 许可证

MIT License

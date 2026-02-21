# CFTC COT 期货持仓分析仪表盘

基于 CFTC（美国商品期货交易委员会）持仓报告的多品种期货持仓可视化分析工具，支持商品期货（COT）、外汇与加密货币（TFF）等多种市场数据。

## 功能特性

### 报告类型支持

- **COT (Disaggregated)**：商品期货持仓报告
  - 关注 **Managed Money（管理基金）** 持仓动态
  - 包含生产商、交易商等各类参与者数据

- **TFF (Traders in Financial Futures)**：金融期货持仓报告
  - 关注 **Leveraged Funds（杠杆资金/对冲基金）** 持仓动态
  - 涵盖外汇、股指、加密货币等金融衍生品

### 多品种支持

支持 **21+ 品种**，涵盖贵金属、工业金属、能源、农产品、外汇、加密货币、股票指数等。

### 时间范围选择

- 3个月（13周）
- 6个月（26周）
- 1年（52周）
- 3年（156周）

### 可视化图表

- **净持仓趋势与边际变化组合图**：折线显示持仓水平，柱状图显示周度变化量
- **Other Reportable / 交易商持仓周度变化**：绿色增仓/红色减仓，含中位数参考线
- **未平仓合约量**：市场参与热度指标，含中位数标注
- **多空持仓对比（近12周）**：直观对比多头/空头力量变化

### 特色数据分析

#### 黄金品种专属
- **GVZ 波动率指数 vs 非商业净持仓**：观察市场恐慌程度与投机持仓的背离关系
- **GVZ 独立走势 + GLD 周成交量**：波动率均值参考线

#### 铜品种专属
- **COMEX 铜期货曲线（当前快照）**：期限结构可视化，识别 Contango/Backwardation
- **COMEX 季度合约价差历史**：M1-M3 价差趋势，反映库存松紧
- **沪铜（SHFE）期货曲线**：国内铜市场期限结构
- **沪铜季度合约价差历史**：国内外市场对比参考
- **沪铜注册仓单量**：SHFE 周度库存数据，含中位数对比

### 数据表格

周度持仓变化明细表，包含：
- 各类持仓者净持仓
- 周变化量
- 变化率（%）

## 项目亮点

✨ **21+ 品种全覆盖**：贵金属、工业金属、能源、外汇、加密货币、股指一站式分析
📊 **双报告支持**：COT（商品）+ TFF（金融），适配不同市场特性
🎯 **特色深度数据**：黄金 GVZ 波动率、铜期限结构、沪铜仓单数据
⚡ **零配置使用**：纯前端仪表盘，打开即用，支持在线访问
🤖 **自动化更新**：GitHub Actions 每周自动获取最新数据
📈 **中位数参考线**：历史分位数对比，快速识别极端持仓

## 预览

### 一、净持仓趋势与边际变化

折线图展示持仓水平，柱状图显示周度变化量（右轴），直观观察资金流入流出。

<img width="1478" height="729" alt="净持仓与边际变化" src="https://github.com/user-attachments/assets/4bf3f064-7519-4f87-984f-d867adc1e991" />

### 二、未平仓合约量 & 多空对比

中位数参考线是判断市场参与热度的优秀指标。柱色深浅反映相对历史水平的高低。

<img width="1459" height="354" alt="未平仓合约量与多空对比" src="https://github.com/user-attachments/assets/ffec40c0-5a9c-41c6-b6a7-d447303895b6" />

### 三、周度持仓变化明细表

包含净持仓、周变化、变化率等关键数据，支持历史回溯。

<img width="1442" height="417" alt="明细表" src="https://github.com/user-attachments/assets/b8fea785-90e3-4d81-8064-01871135d6a3" />


## 项目结构

```
cftc_report/
├── backend/
│   ├── cftc_data_fetcher.py   # 数据获取与处理核心脚本
│   └── requirements.txt        # Python依赖（cot-reports、yfinance、akshare等）
├── data/
│   └── cot_data.json           # 统一数据文件（包含所有品种、GVZ、期货曲线等）
├── frontend/                    # React 前端（组件化架构）
│   └── src/
│       ├── components/         # 可复用图表组件
│       │   ├── Dashboard.jsx
│       │   ├── NetPositionChart.jsx
│       │   ├── OpenInterestChart.jsx
│       │   ├── PositionCompareChart.jsx
│       │   ├── WeeklyChangeTable.jsx
│       │   └── MetricCards.jsx
│       └── App.jsx
├── dashboard.html               # 独立 HTML 仪表盘（纯前端，无需构建）
├── .github/
│   └── workflows/
│       └── update_data.yml     # GitHub Actions 自动更新数据
└── README.md
```

## 快速开始

### 方式一：在线访问（推荐）

可直接下载访问：dashboard.html

*数据每周五自动更新，无需本地运行*

### 方式二：本地运行

#### 1. 克隆仓库

```bash
git clone https://github.com/Philbenzy/cftc-cot-report.git
cd cftc-cot-report
```

#### 2. 安装 Python 依赖

```bash
cd backend
pip install -r requirements.txt
```

#### 3. 获取数据（首次运行或手动更新）

```bash
python cftc_data_fetcher.py
```

首次运行会下载以下数据：
- CFTC COT/TFF 持仓数据（近3年）
- GVZ 黄金波动率指数（黄金品种）
- CME COMEX 铜期货曲线（铜品种）
- SHFE 沪铜期货曲线与注册仓单（铜品种）

生成的数据文件：`../data/cot_data.json`

#### 4. 启动本地服务器

```bash
cd ..
python -m http.server 8080
```

或使用任意 HTTP 服务器工具（如 `npx serve`、VS Code Live Server 等）

#### 5. 访问仪表盘

打开浏览器访问：http://localhost:8080/dashboard.html

## 数据更新

### 自动更新（GitHub Actions）

项目已配置 GitHub Actions，每周六 UTC 00:00 自动运行数据更新脚本，并将最新数据推送到仓库。

**工作流文件**：`.github/workflows/update_data.yml`

### 手动更新

```bash
cd backend
python cftc_data_fetcher.py
```

**更新周期**：
- CFTC 数据：每周五美东时间 15:30 发布（数据截至周二收盘）
- GVZ 数据：每日更新
- 期货曲线：实时数据
- 沪铜仓单：每周五更新

## 数据说明

### 报告类型详解

#### COT Disaggregated（商品期货持仓报告）

用于分析商品市场（贵金属、工业金属、能源、农产品等）的持仓结构。

**持仓者分类**：

| 类别 | 英文 | 说明 | 市场角色 |
|------|------|------|----------|
| **管理基金** | Managed Money | 对冲基金、CTA、资管机构 | **核心投机力量**，趋势追踪者 |
| **生产商** | Producer/Merchant | 生产商、加工商、贸易商 | 套保者，通常与价格反向操作 |
| **Swap Dealer** | Swap Dealer | 互换交易商 | 对冲互换合约风险 |
| **Other Reportable** | Other Reportable | 其他大额持仓者 | 除上述三类外的机构 |

**核心关注指标**：
- **Managed Money 净持仓**：反映投机资金对市场的多空观点
- **净持仓边际变化**：周度增减量，反映资金流入流出

#### TFF（Traders in Financial Futures）金融期货持仓报告

用于分析外汇、股指、加密货币等金融衍生品市场。

**持仓者分类**：

| 类别 | 英文 | 说明 | 市场角色 |
|------|------|------|----------|
| **杠杆资金** | Leveraged Funds | 对冲基金、高频交易、杠杆投机者 | **核心投机力量**，方向性交易主力 |
| **资产管理** | Asset Manager/Institutional | 养老金、主权基金、共同基金 | 机构投资者，长期配置 |
| **交易商** | Dealer/Intermediary | 做市商、中介机构 | 流动性提供者 |

**核心关注指标**：
- **Leveraged Funds 净持仓**：反映杠杆投机资金的方向性仓位
- **Asset Manager 净持仓**：反映机构长期配置意愿

### 关键指标定义

- **净持仓（Net Position）**：多头持仓 - 空头持仓
- **多空比（Long/Short Ratio）**：多头持仓 / 空头持仓
- **周变化（Weekly Change）**：本周净持仓 - 上周净持仓
- **变化率（Change %）**：周变化 / 上周净持仓绝对值
- **未平仓合约（Open Interest）**：市场总持仓量，反映参与热度
- **中位数（Median）**：用于判断当前水平是否处于历史高位或低位

### 数据发布周期

- CFTC 数据每周五美东时间 15:30 发布
- 数据截至日期为周二收盘
- 本项目自动更新数据（通过 GitHub Actions）

## 支持的品种

### COT 商品期货（Disaggregated Futures + Options）

#### 贵金属
| 品种 | 代码 | 交易所 | 特色数据 |
|------|------|--------|----------|
| 黄金 | gold | COMEX | GVZ 波动率 + GLD 成交量 |
| 微型黄金 | micro_gold | COMEX | GVZ 波动率 + GLD 成交量 |
| 白银 | silver | COMEX | - |
| 铂金 | platinum | NYMEX | - |
| 钯金 | palladium | NYMEX | - |

#### 工业金属
| 品种 | 代码 | 交易所 | 特色数据 |
|------|------|--------|----------|
| 铜 | copper | COMEX | COMEX期货曲线 + 沪铜数据 + 注册仓单 |
| 铝 | aluminum | COMEX | - |
| 钴 | cobalt | COMEX | - |
| 氢氧化锂 | lithium | COMEX | - |

#### 能源
| 品种 | 代码 | 交易所 |
|------|------|--------|
| WTI原油 | wti | NYMEX |

#### 农产品
| 品种 | 代码 | 交易所 |
|------|------|--------|
| 棕榈油 | palm_oil | CME |

### TFF 金融期货（Traders in Financial Futures）

#### 外汇
| 品种 | 代码 | 交易所 |
|------|------|--------|
| 欧元 | euro | CME |
| 英镑 | gbp | CME |
| 日元 | jpy | CME |
| 澳元 | aud | CME |
| 加元 | cad | CME |
| 瑞郎 | chf | CME |

#### 加密货币
| 品种 | 代码 | 交易所 |
|------|------|--------|
| 比特币 | bitcoin | CME |

#### 股票指数
| 品种 | 代码 | 交易所 |
|------|------|--------|
| 标普500 | sp500 | CME |
| 纳斯达克100 | nasdaq | CME |
| 罗素2000 | russell | CME |
| VIX | vix | CBOE |

## 技术栈

### 后端
- **Python 3.x**
- **数据获取库**：
  - `cot-reports`：CFTC COT/TFF 官方数据（[项目地址](https://github.com/NDelventhal/cot_reports)）
  - `yfinance`：GVZ 波动率指数、GLD 成交量
  - `akshare`：沪铜（SHFE）期货曲线、注册仓单数据
  - `requests`：CME 期货曲线数据
- **数据处理**：`pandas`

### 前端
- **独立版本**：HTML + Chart.js 4.x（无需构建，直接打开浏览器）
- **React 版本**：React 18 + 组件化架构（可选）

### 数据源
- **CFTC 官方数据**：商品期货（COT Disaggregated）+ 金融期货（TFF）
- **Yahoo Finance**：GVZ 黄金波动率指数、GLD ETF 成交量
- **CME Group**：COMEX 铜期货实时曲线数据
- **上海期货交易所（SHFE）**：沪铜期货曲线、注册仓单数据

### 自动化
- **GitHub Actions**：每周自动更新数据并推送到仓库
- **数据回退机制**：GitHub Raw → 本地文件 → 内置数据（三级回退，确保可用性）

## 使用场景

### 适用人群
- **期货交易者**：跟踪大资金（管理基金/杠杆资金）持仓变化，辅助交易决策
- **量化研究员**：挖掘 COT 数据与价格的领先/滞后关系
- **市场分析师**：撰写持仓分析报告，观察资金流向
- **投资机构**：监控机构投资者（Asset Manager）配置意愿
- **学习者**：了解期货市场参与者结构，学习持仓分析方法

### 典型应用
1. **趋势确认**：管理基金大幅增仓时，往往伴随趋势行情
2. **反向指标**：极端持仓（超过历史95分位数）可能是反转信号
3. **背离分析**：价格创新高但持仓下降，可能预示动能减弱
4. **跨市场对比**：黄金 COT + GVZ 波动率，观察恐慌与持仓背离
5. **期限结构**：铜期货 Contango/Backwardation，判断库存松紧

## 常见问题

**Q1：数据延迟多久？**
A：CFTC 数据每周五 15:30（美东时间）发布，数据截至周二收盘，有约3天延迟。本项目通过 GitHub Actions 每周六自动更新。

**Q2：为什么黄金品种有 GVZ 数据，其他品种没有？**
A：GVZ 是 CBOE 推出的黄金波动率指数，仅针对黄金市场。其他金属没有对应的波动率指数产品。

**Q3：沪铜数据是否实时？**
A：沪铜期货曲线数据每次运行脚本时获取当日最新数据，注册仓单数据为每周五上期所发布数据。

**Q4：TFF 报告与 COT 报告有什么区别？**
A：TFF 用于外汇、股指、加密货币等金融衍生品，关注 Leveraged Funds（杠杆资金）；COT Disaggregated 用于商品期货，关注 Managed Money（管理基金）。两者核心逻辑相同，但分类略有差异。

**Q5：可以添加其他品种吗？**
A：可以！在 `backend/cftc_data_fetcher.py` 中的 `COMMODITIES` 或 `FX_INSTRUMENTS` 字典添加新品种配置即可。需要知道该品种在 CFTC 报告中的准确名称（Market and Exchange Names）。

## 开发计划

- [ ] 支持自定义时间范围（日期选择器）
- [ ] 添加价格走势叠加显示（K线 + COT 持仓）
- [ ] 支持更多衍生指标（持仓净额历史分位数、COI 指标等）
- [ ] 添加品种相关性分析（如铜价与沪铜的价差关系）
- [ ] 移动端适配优化

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

如果觉得项目有帮助，请给个 ⭐️ Star 支持一下～

## 联系方式

📧 Email: thedarksideomoono@gmail.com

🐛 反馈 Bug 或建议：[GitHub Issues](https://github.com/Philbenzy/cftc-cot-report/issues)

---

祝大家 2026 多多陪伴家人，多多赚钱～ 💰✨

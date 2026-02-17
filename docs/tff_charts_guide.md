# TFF 报告图表说明文档

CFTC **TFF（Traders in Financial Futures）** 报告，中文全称"金融期货交易商报告"，每周五与 COT 报告同步发布，数据截止日为当周二。本仪表盘使用的是 **`traders_in_financial_futures_futopt`** 版本，即期货 + 期权合并数据（Futures and Options Combined）。

TFF 报告覆盖在美国受监管交易所交易的金融期货品种，包括外汇（欧元、英镑、日元、澳元、加元、瑞郎）、加密货币（比特币 CME）和股票指数（标普500、纳斯达克100、罗素2000、VIX）。

---

## 一、TFF 报告参与者分类

TFF 报告将持仓者拆分为四类，仪表盘只使用前三类：

| 仪表盘显示名称 | CFTC 官方名称 | 典型机构 | 字段前缀 |
|---|---|---|---|
| 杠杆资金 | Leveraged Funds | 对冲基金、CTA（商品交易顾问）、CPO（商品池运营商） | `Lev_Money_` |
| 资产管理 | Asset Manager / Institutional | 养老金、共同基金、保险公司、主权财富基金 | `Asset_Mgr_` |
| 交易商 | Dealer / Intermediary | 投行、经纪商、做市商（通常为大型银行） | `Dealer_` |
| 其他可报告 | Other Reportables | 不属于以上三类的其他须报告交易者 | `Other_Rept_` |

> **字段后缀说明**：本仪表盘统一使用 `_All` 结尾字段，表示**期货 + 期权合并**持仓量（Futures and Options Combined）。

---

## 二、原始字段名称速查

以下为从 CFTC 原始 CSV/ZIP 文件中提取的字段名称，也是 `cftc_data_fetcher.py` 中 `TFF_COL_MAP` 所映射的原始列名：

| 原始字段名 | 仪表盘内部字段 | 含义 |
|---|---|---|
| `Open_Interest_All` | `open_interest` | 市场总未平仓合约量（期货+期权） |
| `Lev_Money_Positions_Long_All` | `mm_long` | 杠杆资金多头持仓（期货+期权） |
| `Lev_Money_Positions_Short_All` | `mm_short` | 杠杆资金空头持仓（期货+期权） |
| `Lev_Money_Positions_Spread_All` | `mm_spreading` | 杠杆资金价差持仓（同时持有多空，通常为跨期套利） |
| `Asset_Mgr_Positions_Long_All` | `prod_long` | 资产管理多头持仓（期货+期权） |
| `Asset_Mgr_Positions_Short_All` | `prod_short` | 资产管理空头持仓（期货+期权） |
| `Dealer_Positions_Long_All` | `other_long` | 交易商多头持仓（期货+期权） |
| `Dealer_Positions_Short_All` | `other_short` | 交易商空头持仓（期货+期权） |

> **注**：仪表盘前端复用了 COT 的内部字段命名约定（`mm_*` / `prod_*` / `other_*`），含义对应到不同的 CFTC 分类，见上表第一列。

---

## 三、图表详细说明

### 图 1：净持仓趋势与边际变化

**功能**：在同一坐标系中展示杠杆资金和资产管理的净持仓趋势，同时用柱状图显示杠杆资金的周度增减。

**使用字段**：

| 系列 | 类型 | 来源字段 | 计算方式 |
|---|---|---|---|
| 杠杆资金净持仓（折线，左轴） | 折线 | `Lev_Money_Positions_Long_All` - `Lev_Money_Positions_Short_All` | `mm_net = mm_long - mm_short` |
| 资产管理净持仓（折线，左轴） | 折线 | `Asset_Mgr_Positions_Long_All` - `Asset_Mgr_Positions_Short_All` | `prod_net = prod_long - prod_short` |
| 杠杆资金周变化（柱状，右轴） | 柱状 | 本周 `mm_net` − 上周 `mm_net` | `mm_net_change` |

**解读要点**：
- **杠杆资金净持仓**是最核心的方向性指标，代表对冲基金和 CTA 的集体方向判断。净持仓持续走高意味着做多共识加强；净持仓快速大幅下降（紫色/红色大柱）往往对应价格回调或趋势反转。
- **资产管理净持仓**通常量级更大且方向较稳定，代表养老金等长线机构的配置方向。若资产管理与杠杆资金方向相同，多空力量更为一致。
- 周变化柱状图用绿色（增仓）/ 红色（减仓）直观呈现边际动能变化，适合判断趋势加速或衰竭。

---

### 图 2：交易商持仓周度变化

**功能**：单独展示交易商（Dealer/Intermediary）净持仓的周度变化，并标注中位数基准线。

**使用字段**：

| 系列 | 类型 | 来源字段 | 计算方式 |
|---|---|---|---|
| 净持仓变化（柱状） | 柱状 | `Dealer_Positions_Long_All` - `Dealer_Positions_Short_All` | `other_net_change`（本周 `other_net` − 上周） |
| 中位数线（虚线） | 折线 | 以上 `other_net_change` 序列 | 所选时间段内的中位数 |

**角色背景**：

交易商（Dealer/Intermediary）主要是大型投资银行和经纪商。他们既做市又有自营头寸，其持仓往往是**客户需求的镜像**：当客户（杠杆资金、资产管理）大量买入时，交易商通常持有对应的空头进行对冲。因此：

- 交易商净持仓通常与杠杆资金**方向相反**；
- 交易商净空头大幅扩张 → 客户端（杠杆资金）正在大举做多；
- 交易商净空头收窄或转多 → 客户端在减仓或反向操作。

**解读要点**：
- 该图重点不在于交易商的绝对方向，而在于**变化速率**：突然的大幅增减往往预示市场结构正在快速改变。
- 中位数线提供了历史基准，超出中位数区间的异常变化值得重点关注。

---

### 图 3：未平仓合约量

**功能**：展示市场总持仓量（Open Interest）的历史走势，并以中位数为阈值用深浅色区分高低水位。

**使用字段**：

| 系列 | 类型 | 来源字段 | 计算方式 |
|---|---|---|---|
| 未平仓合约（柱状） | 柱状 | `Open_Interest_All` | 直接读取，不做加工 |
| 中位数线（虚线） | 折线 | 同上 | 所选时间段内的中位数 |

**颜色规则**：
- 亮色（金黄）：当周 OI ≥ 中位数，市场参与度处于相对高位；
- 暗色：当周 OI < 中位数，市场参与度处于相对低位。

**解读要点**：
- OI 是衡量市场**参与热度**和**资金流入流出**的关键指标。
- 价格上涨 + OI 同步扩张 → 新资金入场推动，趋势健康；价格上涨 + OI 萎缩 → 空头回补驱动，趋势可持续性存疑。
- OI 突然大幅下降通常对应大规模平仓或合约到期换月。

---

### 图 4：杠杆资金多空持仓对比（近 12 周）

**功能**：聚焦最近 12 周，并排展示杠杆资金的多头和空头绝对量，并各自标注中位数参考线。

**使用字段**：

| 系列 | 类型 | 来源字段 | 计算方式 |
|---|---|---|---|
| 杠杆资金多头（柱状） | 柱状 | `Lev_Money_Positions_Long_All` | 直接读取 (`mm_long`) |
| 杠杆资金空头（柱状） | 柱状 | `Lev_Money_Positions_Short_All` | 直接读取 (`mm_short`) |
| 多头中位数线（绿色虚线） | 折线 | 同上 | 近 12 周 `mm_long` 的中位数 |
| 空头中位数线（红色虚线） | 折线 | 同上 | 近 12 周 `mm_short` 的中位数 |

**颜色规则**：
- 多头柱：亮绿（当周多头 ≥ 近 12 周多头中位数）/ 暗绿（低于中位数）；
- 空头柱：亮红（当周空头 ≥ 近 12 周空头中位数）/ 暗红（低于中位数）。

**解读要点**：
- 净持仓图（图1）只反映多空之差，本图还原多头和空头的**绝对量**，信息量更完整。
- **多头和空头同时扩张**：双边持仓量上升，说明市场分歧加剧，方向性不明朗；
- **多头扩张 + 空头萎缩**：典型的单边看多结构，做多共识正在凝聚；
- **多头萎缩 + 空头扩张**：看空情绪上升；
- **多头和空头同时萎缩**：市场参与者正在撤离，流动性下降，需结合 OI 图（图3）确认。

---

## 四、字段映射总结（原始字段 → 图表系列）

```
原始字段（CFTC CSV）                     图表系列
─────────────────────────────────────────────────────────────────
Open_Interest_All               →  图3 未平仓合约量（柱状）

Lev_Money_Positions_Long_All    →  图1 杠杆资金净持仓（折线，分子）
                                   图4 杠杆资金多头（柱状）
Lev_Money_Positions_Short_All   →  图1 杠杆资金净持仓（折线，分母）
                                   图4 杠杆资金空头（柱状）
Lev_Money_Positions_Spread_All  →  记录但不在图表中展示（价差仓）

Asset_Mgr_Positions_Long_All    →  图1 资产管理净持仓（折线，分子）
Asset_Mgr_Positions_Short_All   →  图1 资产管理净持仓（折线，分母）

Dealer_Positions_Long_All       →  图2 交易商净持仓变化（分子）
Dealer_Positions_Short_All      →  图2 交易商净持仓变化（分母）
─────────────────────────────────────────────────────────────────
派生字段（程序计算）
mm_net          = Lev_Money_Long - Lev_Money_Short
prod_net        = Asset_Mgr_Long - Asset_Mgr_Short
other_net       = Dealer_Long    - Dealer_Short
mm_net_change   = 本周 mm_net   - 上周 mm_net
other_net_change= 本周 other_net - 上周 other_net
oi_change       = 本周 open_interest - 上周 open_interest
```

---

## 五、品种清单

### 外汇

| 代码 | 品种 | CFTC 原始市场名称 | 最新 OI（2026-02） |
|---|---|---|---|
| euro | 欧元 | EURO FX - CHICAGO MERCANTILE EXCHANGE | 1,051,803 |
| gbp | 英镑 | BRITISH POUND - CHICAGO MERCANTILE EXCHANGE | 255,409 |
| jpy | 日元 | JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE | 374,126 |
| aud | 澳元 | AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE | 280,024 |
| cad | 加元 | CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE | 250,132 |
| chf | 瑞郎 | SWISS FRANC - CHICAGO MERCANTILE EXCHANGE | 106,816 |

### 加密货币

| 代码 | 品种 | CFTC 原始市场名称 | 最新 OI（2026-02） |
|---|---|---|---|
| bitcoin | 比特币 | BITCOIN - CHICAGO MERCANTILE EXCHANGE | 25,466 |

> 注：比特币 OI 单位为张，每张合约 = 5 BTC。

### 股票指数

| 代码 | 品种 | CFTC 原始市场名称 | 最新 OI（2026-02） | 说明 |
|---|---|---|---|---|
| sp500 | 标普500 | S&P 500 Consolidated | 2,643,248 | 聚合所有 S&P 500 相关合约，含 E-mini 与标准合约 |
| nasdaq | 纳斯达克100 | NASDAQ-100 Consolidated | 312,271 | 聚合所有 Nasdaq-100 合约 |
| russell | 罗素2000 | RUSSELL E-MINI | 427,126 | 小盘股代表性指数 |
| vix | VIX | VIX FUTURES - CBOE FUTURES EXCHANGE | 371,926 | 标普500隐含波动率指数期货，来自 CBOE |

**关于股指 TFF 持仓的特殊解读：**

- **标普500**：杠杆资金（对冲基金/CTA）对 S&P 500 的净持仓通常为**空头主导**（净空头），因为大量对冲基金持有股票组合，同时在期货端做空对冲，并非真正的空头方向。**快速增仓（减少净空头）才是真实的看多信号。**
- **VIX 期货**：VIX 合约结构特殊——VIX 均值回归特性显著，长期持有多头会因 Contango 结构（远月溢价）而损耗价值。杠杆资金在 VIX 上的净空头扩张，通常对应市场的"低恐慌"状态；VIX 持仓方向反转往往预示市场波动率即将变化。

---

## 六、数据来源

- **报告类型**：`traders_in_financial_futures_futopt`（TFF，期货+期权合并版）
- **发布机构**：CFTC（U.S. Commodity Futures Trading Commission）
- **发布频率**：每周五 15:30 美东时间
- **数据截止日**：每周二收盘
- **获取方式**：通过 `cot-reports` Python 库自动下载（`cot.cot_year(year, cot_report_type=...)`）
- **CFTC 官方说明**：https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm

"""
CFTC COT Report Data Fetcher
- Disaggregated Futures + Options：商品期货（金属、能源、农产品）
  核心关注：Managed Money（管理基金）持仓
- Traders in Financial Futures（TFF）：外汇 & 加密货币
  核心关注：Leveraged Funds（杠杆资金/对冲基金）持仓
"""

import json
import os
import time
from datetime import datetime, timedelta
import pandas as pd
import requests
import cot_reports as cot
import yfinance as yf
import akshare as ak


# ── COT Disaggregated 商品品种配置 ───────────────────────────────────────────
COMMODITIES = {
    "gold":      {"name": "黄金",     "name_en": "GOLD (COMEX)",           "pattern": r"^GOLD - COMMODITY EXCHANGE"},
    "silver":    {"name": "白银",     "name_en": "SILVER (COMEX)",         "pattern": r"^SILVER - COMMODITY EXCHANGE"},
    "copper":    {"name": "铜",       "name_en": "COPPER (COMEX)",         "pattern": r"^COPPER.* - COMMODITY EXCHANGE"},
    "platinum":  {"name": "铂金",     "name_en": "PLATINUM (NYMEX)",       "pattern": r"^PLATINUM - NEW YORK MERCANTILE"},
    "palladium": {"name": "钯金",     "name_en": "PALLADIUM (NYMEX)",      "pattern": r"^PALLADIUM - NEW YORK MERCANTILE"},
    "micro_gold":{"name": "微型黄金", "name_en": "MICRO GOLD (COMEX)",     "pattern": r"^MICRO GOLD - COMMODITY EXCHANGE"},
    "aluminum":  {"name": "铝",       "name_en": "ALUMINUM (COMEX)",       "pattern": r"^ALUMINUM - COMMODITY EXCHANGE"},
    "cobalt":    {"name": "钴",       "name_en": "COBALT (COMEX)",         "pattern": r"^COBALT - COMMODITY EXCHANGE"},
    "lithium":   {"name": "氢氧化锂", "name_en": "LITHIUM HYDROXIDE (COMEX)", "pattern": r"^LITHIUM HYDROXIDE - COMMODITY EXCHANGE"},
    "wti":       {"name": "WTI原油",  "name_en": "WTI CRUDE OIL (NYMEX)", "pattern": r"^WTI-PHYSICAL - NEW YORK MERCANTILE"},
    "palm_oil":  {"name": "棕榈油",   "name_en": "PALM OIL (CME)",         "pattern": r"^USD Malaysian Crude Palm Oil"},
}

# ── TFF 外汇、加密货币及股指品种配置 ─────────────────────────────────────────
FX_INSTRUMENTS = {
    # 外汇
    "euro":     {"name": "欧元",       "name_en": "EURO FX (CME)",            "pattern": r"^EURO FX - CHICAGO MERCANTILE"},
    "gbp":      {"name": "英镑",       "name_en": "BRITISH POUND (CME)",      "pattern": r"^BRITISH POUND - CHICAGO MERCANTILE"},
    "jpy":      {"name": "日元",       "name_en": "JAPANESE YEN (CME)",       "pattern": r"^JAPANESE YEN - CHICAGO MERCANTILE"},
    "aud":      {"name": "澳元",       "name_en": "AUSTRALIAN DOLLAR (CME)",  "pattern": r"^AUSTRALIAN DOLLAR - CHICAGO MERCANTILE"},
    "cad":      {"name": "加元",       "name_en": "CANADIAN DOLLAR (CME)",    "pattern": r"^CANADIAN DOLLAR - CHICAGO MERCANTILE"},
    "chf":      {"name": "瑞郎",       "name_en": "SWISS FRANC (CME)",        "pattern": r"^SWISS FRANC - CHICAGO MERCANTILE"},
    # 加密货币
    "bitcoin":  {"name": "比特币",     "name_en": "BITCOIN (CME)",            "pattern": r"^BITCOIN - CHICAGO MERCANTILE"},
    # 股票指数
    "sp500":    {"name": "标普500",    "name_en": "S&P 500 (CME)",            "pattern": r"^S&P 500 Consolidated"},
    "nasdaq":   {"name": "纳斯达克100","name_en": "NASDAQ-100 (CME)",         "pattern": r"^NASDAQ-100 Consolidated"},
    "russell":  {"name": "罗素2000",   "name_en": "RUSSELL 2000 (CME)",       "pattern": r"^RUSSELL E-MINI"},
    "vix":      {"name": "VIX",        "name_en": "VIX (CBOE)",               "pattern": r"^VIX FUTURES"},
}

# TFF 列名映射
# mm_*   → Leveraged Funds（杠杆资金 / 对冲基金 / CTA）
# prod_* → Asset Manager（资产管理 / 机构投资者）
# other_*→ Dealer/Intermediary（交易商 / 做市商）
TFF_COL_MAP = {
    'open_interest': ['Open_Interest_All'],
    'mm_long':    ['Lev_Money_Positions_Long_All'],
    'mm_short':   ['Lev_Money_Positions_Short_All'],
    'mm_spread':  ['Lev_Money_Positions_Spread_All'],
    'prod_long':  ['Asset_Mgr_Positions_Long_All'],
    'prod_short': ['Asset_Mgr_Positions_Short_All'],
    'other_long':  ['Dealer_Positions_Long_All'],
    'other_short': ['Dealer_Positions_Short_All'],
}

# 输出路径
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def fetch_cot_data(years: list = None) -> pd.DataFrame:
    """获取 COT Disaggregated Futures + Options 报告数据"""
    if years is None:
        current_year = datetime.now().year
        years = [current_year - 3, current_year - 2, current_year - 1, current_year]
    all_data = []
    for year in years:
        try:
            print(f"  {year} 年...", end=" ")
            df = cot.cot_year(year=year, cot_report_type="disaggregated_futopt")
            all_data.append(df)
            print("OK")
        except Exception as e:
            print(f"失败: {e}")
    if not all_data:
        raise ValueError("未能获取任何数据")
    return pd.concat(all_data, ignore_index=True)


def fetch_tff_data(years: list = None) -> pd.DataFrame:
    """获取 TFF（Traders in Financial Futures）报告数据"""
    if years is None:
        current_year = datetime.now().year
        years = [current_year - 3, current_year - 2, current_year - 1, current_year]
    all_data = []
    for year in years:
        try:
            print(f"  {year} 年...", end=" ")
            df = cot.cot_year(year=year, cot_report_type="traders_in_financial_futures_futopt")
            all_data.append(df)
            print("OK")
        except Exception as e:
            print(f"失败: {e}")
    if not all_data:
        raise ValueError("未能获取任何TFF数据")
    return pd.concat(all_data, ignore_index=True)


def filter_commodity_data(df: pd.DataFrame, pattern: str) -> pd.DataFrame:
    """根据正则表达式筛选特定品种数据"""
    market_col = None
    for col in df.columns:
        if 'market' in col.lower() and 'exchange' in col.lower():
            market_col = col
            break
    if market_col is None:
        raise ValueError("未找到市场名称列")
    mask = df[market_col].str.match(pattern, case=False, na=False)
    return df[mask].copy()


def get_column_value(row, possible_names, default=0):
    """从多个可能的列名中获取值"""
    for name in possible_names:
        if name in row.index:
            val = row[name]
            if pd.notna(val):
                return int(val)
    return default


def process_commodity_data(df: pd.DataFrame, weeks: int = 52, col_map: dict = None) -> list:
    """
    处理品种数据，返回周度数据列表。
    col_map 为 None 时使用 Disaggregated 默认映射；
    传入 TFF_COL_MAP 时处理 TFF 外汇/加密数据。
    """
    # 日期列查找
    date_col = None
    for col in df.columns:
        if 'yyyy-mm-dd' in col.lower():
            date_col = col
            break
    if date_col is None:
        for col in df.columns:
            if 'date' in col.lower():
                date_col = col
                break
    if date_col is None:
        return []

    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col, ascending=False).head(weeks).copy()
    df = df.sort_values(date_col, ascending=True)

    # 默认 Disaggregated 列名映射
    if col_map is None:
        col_map = {
            'open_interest': ['Open_Interest_All'],
            'mm_long':       ['M_Money_Positions_Long_All'],
            'mm_short':      ['M_Money_Positions_Short_All'],
            'mm_spread':     ['M_Money_Positions_Spread_All'],
            'prod_long':     ['Prod_Merc_Positions_Long_All'],
            'prod_short':    ['Prod_Merc_Positions_Short_All'],
            'other_long':    ['Other_Rept_Positions_Long_All'],
            'other_short':   ['Other_Rept_Positions_Short_All'],
        }

    records = []
    for _, row in df.iterrows():
        mm_long    = get_column_value(row, col_map['mm_long'])
        mm_short   = get_column_value(row, col_map['mm_short'])
        prod_long  = get_column_value(row, col_map['prod_long'])
        prod_short = get_column_value(row, col_map['prod_short'])
        other_long  = get_column_value(row, col_map.get('other_long', []))
        other_short = get_column_value(row, col_map.get('other_short', []))

        record = {
            "date":         row[date_col].strftime("%Y-%m-%d"),
            "mm_long":      mm_long,
            "mm_short":     mm_short,
            "mm_spreading": get_column_value(row, col_map.get('mm_spread', [])),
            "prod_long":    prod_long,
            "prod_short":   prod_short,
            "other_long":   other_long,
            "other_short":  other_short,
            "open_interest": get_column_value(row, col_map['open_interest']),
            "mm_net":    mm_long - mm_short,
            "prod_net":  prod_long - prod_short,
            "other_net": other_long - other_short,
        }
        records.append(record)

    for i in range(1, len(records)):
        records[i]["mm_net_change"]    = records[i]["mm_net"]    - records[i-1]["mm_net"]
        records[i]["prod_net_change"]  = records[i]["prod_net"]  - records[i-1]["prod_net"]
        records[i]["other_net_change"] = records[i]["other_net"] - records[i-1]["other_net"]
        records[i]["oi_change"]        = records[i]["open_interest"] - records[i-1]["open_interest"]

    if records:
        records[0]["mm_net_change"]    = 0
        records[0]["prod_net_change"]  = 0
        records[0]["other_net_change"] = 0
        records[0]["oi_change"]        = 0

    return records


def calculate_summary(records: list) -> dict:
    """计算汇总指标"""
    if not records:
        return {}
    latest = records[-1]
    return {
        "latest_date":     latest.get("date", ""),
        "mm_net":          latest.get("mm_net", 0),
        "prod_net":        latest.get("prod_net", 0),
        "open_interest":   latest.get("open_interest", 0),
        "mm_net_change":   latest.get("mm_net_change", 0),
        "prod_net_change": latest.get("prod_net_change", 0),
        "oi_change":       latest.get("oi_change", 0),
        "long_short_ratio": round(latest.get("mm_long", 0) / max(latest.get("mm_short", 1), 1), 2),
    }


def fetch_gvz_data(start_year: int = 2023) -> list:
    """获取 GVZ 黄金波动率指数 与 GLD 周成交量"""
    print("\n正在获取 GVZ 与 GLD 成交量数据...")
    start = f"{start_year}-01-01"
    gvz_df = yf.download("^GVZ", start=start, auto_adjust=True, progress=False)
    gld_df = yf.download("GLD",  start=start, auto_adjust=True, progress=False)

    if gvz_df.empty:
        print("  警告: GVZ 数据获取失败")
        return []

    gvz_close = gvz_df["Close"].squeeze()
    gvz_close.index = pd.to_datetime(gvz_close.index).tz_localize(None)

    gld_vol = pd.Series(dtype=float)
    if not gld_df.empty:
        gld_vol = gld_df["Volume"].squeeze()
        gld_vol.index = pd.to_datetime(gld_vol.index).tz_localize(None)
        gld_vol = gld_vol.resample("W-TUE").sum()

    start_dt = pd.Timestamp(start)
    end_dt   = pd.Timestamp.today()
    tuesdays = pd.date_range(start=start_dt, end=end_dt, freq="W-TUE")

    records = []
    for tue in tuesdays:
        window = gvz_close[gvz_close.index <= tue]
        if window.empty:
            continue
        gvz_val = round(float(window.iloc[-1]), 2)
        gld_val = None
        if tue in gld_vol.index:
            gld_val = int(gld_vol[tue])
        elif not gld_vol.empty:
            w = gld_vol[gld_vol.index <= tue]
            if not w.empty:
                gld_val = int(w.iloc[-1])
        records.append({"date": tue.strftime("%Y-%m-%d"), "close": gvz_val, "gld_volume": gld_val})

    print(f"  成功: {len(records)} 周数据，最新: {records[-1]['date'] if records else 'N/A'}")
    return records


def _next_month(year: int, month: int):
    """返回下一个月的 (year, month)"""
    return (year + 1, 1) if month == 12 else (year, month + 1)


def get_copper_contract(date: datetime, offset: int = 0):
    """
    返回给定日期的第 (offset+1) 个活跃 COMEX 铜期货合约。
    以每月 25 日作为合约到期的保守估计（实际为交割月倒数第 3 个交易日）。
    offset=0 → M1（近月），offset=2 → M3（第三月）
    返回: (ticker, delivery_year, delivery_month)
    """
    MONTH_CODES = {1:'F', 2:'G', 3:'H', 4:'J', 5:'K', 6:'M',
                   7:'N', 8:'Q', 9:'U', 10:'V', 11:'X', 12:'Z'}
    y, m = date.year, date.month
    count = 0
    while True:
        if datetime(y, m, 25) > date:
            if count == offset:
                return f"HG{MONTH_CODES[m]}{str(y)[-2:]}.CMX", y, m
            count += 1
        y, m = _next_month(y, m)


def _fetch_cme_settlements(trade_date_str: str) -> list:
    """从 CME 公开 API 获取指定日期的铜期货结算价列表"""
    url = (
        f"https://www.cmegroup.com/CmeWS/mvc/Settlements/futures/settlements"
        f"/HG/future?tradeDate={trade_date_str}&version=final"
    )
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=12)
        if resp.status_code != 200:
            return []
        return resp.json().get("settlements", [])
    except Exception:
        return []


def _parse_settle(val: str):
    """将结算价字符串转为 float，失败返回 None"""
    if not val or val.strip() in ("", "-", "---", "UNCH", "EST", "A", "B"):
        return None
    try:
        return float(val.replace(",", ""))
    except ValueError:
        return None


def fetch_copper_curve_data(weeks: int = 156) -> dict:
    """
    获取 COMEX 铜期货期限结构数据：
    - snapshot ：yfinance 抓取当前活跃合约价格（未来 12 个月）
    - spread_history：使用当前活跃季度合约的长期历史数据计算近远月价差
      策略：下载当前活跃的季度合约（H/K/N/U/Z），这些合约在 yfinance 中
      保留有完整的上市至今历史（可追溯至 2020-2021 年），通过它们计算每周
      "最近未到期季度合约 M1" 与 "第三近季度合约 M3" 的价差。
    价格单位：USD/lb
    """
    print("\n正在获取 COMEX 铜期货期限结构数据...")
    today = datetime.now()

    MONTH_CODES = {1: 'F', 2: 'G', 3: 'H', 4: 'J', 5: 'K', 6: 'M',
                   7: 'N', 8: 'Q', 9: 'U', 10: 'V', 11: 'X', 12: 'Z'}
    QUARTERLY = {3, 5, 7, 9, 12}   # H, K, N, U, Z 季度月

    # ── 快照：用 yfinance 下载当前活跃合约（含非季度月） ──────────────────────
    snapshot_meta = []
    for i in range(12):
        ticker, y, m = get_copper_contract(today, offset=i)
        snapshot_meta.append({"ticker": ticker, "year": y, "month": m})

    tickers_list = [s["ticker"] for s in snapshot_meta]
    snapshot = []
    try:
        raw = yf.download(tickers_list, period="5d", auto_adjust=True, progress=False)
        if not raw.empty:
            if isinstance(raw.columns, pd.MultiIndex):
                close_df = raw["Close"].copy()
            else:
                close_df = pd.DataFrame({tickers_list[0]: raw["Close"]})
            close_df.index = pd.to_datetime(close_df.index).tz_localize(None)
            for item in snapshot_meta:
                s = close_df.get(item["ticker"])
                if s is None:
                    continue
                s = s.dropna()
                if s.empty:
                    continue
                snapshot.append({
                    "month":    f"{item['year']}-{item['month']:02d}",
                    "price":    round(float(s.iloc[-1]), 4),
                    "contract": item["ticker"]
                })
    except Exception as e:
        print(f"  快照获取失败: {e}")

    # ── 价差历史：利用活跃季度合约的长期历史 ─────────────────────────────────
    # 生成未来 3 年内的季度合约列表（这些合约通常有 3-5 年历史数据）
    quarterly_meta = []
    y, m = today.year, today.month
    for _ in range(37):
        if m in QUARTERLY:
            ticker = f"HG{MONTH_CODES[m]}{str(y)[-2:]}.CMX"
            quarterly_meta.append({
                "ticker": ticker,
                "year": y, "month": m,
                "expiry": datetime(y, m, 25)   # 以 25 日为保守到期日
            })
        y, m = _next_month(y, m)

    qtickers = [q["ticker"] for q in quarterly_meta]
    start_date = (today - timedelta(days=weeks * 7 + 30)).strftime("%Y-%m-%d")
    print(f"  下载 {len(qtickers)} 个季度合约历史数据（从 {start_date} 起）...")

    spread_history = []
    try:
        hist_raw = yf.download(qtickers, start=start_date, auto_adjust=True, progress=False)

        if not hist_raw.empty:
            if isinstance(hist_raw.columns, pd.MultiIndex):
                hist_close = hist_raw["Close"].copy()
            else:
                hist_close = pd.DataFrame({qtickers[0]: hist_raw["Close"]})
            hist_close.index = pd.to_datetime(hist_close.index).tz_localize(None)

            # 按每周五生成日期序列
            end_dt   = pd.Timestamp(today)
            start_dt = pd.Timestamp(start_date)
            fridays  = pd.date_range(start=start_dt, end=end_dt, freq="W-FRI")

            for friday in fridays:
                # 取该周五当日或之前最近一个交易日的收盘价
                window = hist_close[hist_close.index <= friday]
                if window.empty:
                    continue
                latest_row = window.iloc[-1]

                # 收集该日有效价格、且尚未到期的季度合约
                valid = []
                for q in quarterly_meta:
                    if q["expiry"] <= friday:
                        continue   # 已到期，跳过
                    col = q["ticker"]
                    if col not in hist_close.columns:
                        continue
                    price = latest_row.get(col)
                    if price is None or pd.isna(price) or float(price) <= 0:
                        continue
                    valid.append({
                        "ticker":  col,
                        "expiry":  q["expiry"],
                        "price":   float(price),
                        "label":   col.replace(".CMX", "")
                    })

                valid.sort(key=lambda x: x["expiry"])

                if len(valid) < 2:
                    continue

                m1 = valid[0]
                m3 = valid[2] if len(valid) >= 3 else valid[-1]

                spread_history.append({
                    "date":        friday.strftime("%Y-%m-%d"),
                    "m1_price":    round(m1["price"], 4),
                    "m3_price":    round(m3["price"], 4),
                    "m1_contract": m1["label"],
                    "m3_contract": m3["label"],
                    "spread":      round(m1["price"] - m3["price"], 4)
                })

    except Exception as e:
        print(f"  价差历史获取失败: {e}")

    # 按日期去重并排序
    seen = set()
    spread_history = [
        r for r in spread_history
        if r["date"] not in seen and not seen.add(r["date"])
    ]
    spread_history.sort(key=lambda r: r["date"])

    print(f"  成功: 快照 {len(snapshot)} 个合约, 历史价差 {len(spread_history)} 周")
    return {"snapshot": snapshot, "spread_history": spread_history}


def fetch_shfe_copper_data(existing_inventory: list = None) -> dict:
    """
    获取上海期货交易所（SHFE）沪铜期货数据：
    - snapshot       ：当前活跃合约价格快照（期货曲线），单位 CNY/吨
    - spread_history ：季度合约（3/6/9/12月）近远月价差历史
      AKShare 可访问已到期 SHFE 合约，追溯至约 3 年前
    - inventory_history：SHFE 铜注册仓单量，每周追加一条（首次运行起积累）
    """
    print("\n正在获取沪铜（SHFE）期货数据...")
    today = datetime.now()
    if existing_inventory is None:
        existing_inventory = []

    # ── 1. 快照：当前活跃沪铜合约价格（使用 Sina 接口，更稳定）──────────────
    # SHFE 铜以每月 15 日为保守到期日，逐个下载 M1-M12 的最新收盘价
    snapshot = []
    snapshot_codes = []
    y, m = today.year, today.month
    for _ in range(14):
        expiry = datetime(y, m, 15)
        if expiry > today and len(snapshot_codes) < 12:
            snapshot_codes.append({
                "code":  f"CU{str(y)[-2:]}{m:02d}",
                "month": f"{y}-{m:02d}",
            })
        y, m = _next_month(y, m)

    for item in snapshot_codes:
        try:
            df = ak.futures_zh_daily_sina(symbol=item['code'])
            if df is not None and not df.empty:
                price = float(df['close'].iloc[-1])
                if price > 0:
                    snapshot.append({
                        "month":    item['month'],
                        "price":    price,
                        "contract": item['code']
                    })
        except Exception:
            pass
    snapshot.sort(key=lambda x: x['month'])
    print(f"  快照: {len(snapshot)} 个合约")

    # ── 2. 季度价差历史 ────────────────────────────────────────────────────────
    # 季度月：3, 6, 9, 12；AKShare 可访问已到期合约，约追溯 3 年
    quarterly_meta = []
    start_yr = today.year - 3
    end_dt   = today + timedelta(days=400)
    y = start_yr
    while True:
        for qm in [3, 6, 9, 12]:
            dt = datetime(y, qm, 1)
            if dt < datetime(start_yr, 1, 1) or dt > end_dt:
                continue
            quarterly_meta.append({
                "code":     f"CU{str(y)[-2:]}{qm:02d}",
                "delivery": dt
            })
        y += 1
        if y > today.year + 2:
            break

    print(f"  下载 {len(quarterly_meta)} 个季度合约历史...")
    price_cache = {}
    for q in quarterly_meta:
        try:
            df = ak.futures_zh_daily_sina(symbol=q['code'])
            if df is not None and not df.empty:
                df['date'] = pd.to_datetime(df['date'])
                price_cache[q['code']] = {
                    "series":    df.set_index('date')['close'],
                    "last_date": pd.Timestamp(df['date'].max()),
                    "delivery":  q['delivery']
                }
        except Exception:
            pass
    print(f"  成功获取 {len(price_cache)} 个合约数据")

    spread_history = []
    if len(price_cache) >= 2:
        fridays = pd.date_range(
            start=pd.Timestamp(start_yr, 1, 1),
            end=pd.Timestamp(today),
            freq='W-FRI'
        )
        for friday in fridays:
            valid = []
            for code, data in price_cache.items():
                # 合约已经结束交易（最后一个价格日超过10天前）则跳过
                if data['last_date'] < friday - pd.Timedelta(days=10):
                    continue
                window = data['series'][data['series'].index <= friday]
                if window.empty:
                    continue
                price = float(window.iloc[-1])
                if price > 0:
                    valid.append({
                        "code":     code,
                        "delivery": data['delivery'],
                        "price":    price
                    })

            valid.sort(key=lambda x: x['delivery'])
            if len(valid) < 2:
                continue

            m1 = valid[0]
            m3 = valid[2] if len(valid) >= 3 else valid[-1]

            spread_history.append({
                "date":        friday.strftime("%Y-%m-%d"),
                "m1_price":    m1['price'],
                "m3_price":    m3['price'],
                "m1_contract": m1['code'],
                "m3_contract": m3['code'],
                "spread":      round(m1['price'] - m3['price'], 0)
            })

        seen = set()
        spread_history = [
            r for r in spread_history
            if r['date'] not in seen and not seen.add(r['date'])
        ]
        spread_history.sort(key=lambda r: r['date'])
        print(f"  价差历史: {len(spread_history)} 周")

    # ── 3. 注册仓单（库存）：追加当周数据 ─────────────────────────────────────
    inventory_history = list(existing_inventory)
    try:
        wh    = ak.futures_shfe_warehouse_receipt()
        cu_wh = wh.get('铜', pd.DataFrame())
        if not cu_wh.empty:
            # 取"总计"行（WHABBRNAME='总计'），避免对小计行重复累加
            total_rows = cu_wh[cu_wh['WHABBRNAME'] == '总计']
            if total_rows.empty:
                # 备用：取 ROWSTATUS=2 的最后一行
                total_rows = cu_wh[cu_wh['ROWSTATUS'] == 2].tail(1)
            if total_rows.empty:
                raise ValueError("未找到总计行")
            total  = int(total_rows.iloc[-1]['WRTWGHTS'])
            change = int(total_rows.iloc[-1]['WRTCHANGE'])
            # 取本周五作为记录日期
            days_to_fri  = (4 - today.weekday()) % 7
            this_friday  = (today + timedelta(days=days_to_fri)).strftime('%Y-%m-%d')
            if not inventory_history or inventory_history[-1]['date'] != this_friday:
                inventory_history.append({
                    "date":   this_friday,
                    "total":  total,
                    "change": change
                })
                print(f"  仓单: {total:,} 吨 (变化 {change:+,} 吨) [{this_friday}]")
            else:
                print(f"  仓单: 已是最新 ({this_friday})")
    except Exception as e:
        print(f"  仓单获取失败: {e}")

    print(f"  完成: 快照 {len(snapshot)} 合约 | 价差 {len(spread_history)} 周 | 仓单 {len(inventory_history)} 条")
    return {
        "snapshot":          snapshot,
        "spread_history":    spread_history,
        "inventory_history": inventory_history
    }


def save_to_json(data: dict, filename: str = "cot_data.json"):
    """保存数据为JSON文件"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"数据已保存至: {filepath}")
    return filepath


def main():
    print("=" * 55)
    print("CFTC COT 数据获取程序")
    print("=" * 55)

    # 读取已有 JSON（保留沪铜仓单历史，避免每次覆盖）
    existing_fp = os.path.join(OUTPUT_DIR, "cot_data.json")
    existing_shfe_inventory = []
    if os.path.exists(existing_fp):
        try:
            with open(existing_fp, "r", encoding="utf-8") as f:
                old = json.load(f)
            existing_shfe_inventory = old.get("shfe_copper", {}).get("inventory_history", [])
        except Exception:
            pass

    result = {
        "commodities": {},
        "commodity_list": [],
        "tff_instruments": {},
        "tff_instrument_list": [],
        "copper_curve": {"snapshot": [], "spread_history": []},
        "shfe_copper":  {"snapshot": [], "spread_history": [], "inventory_history": []},
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # ── 1. COT Disaggregated 商品数据 ─────────────────────────────────────
    print("\n[1/6] 获取 COT Disaggregated 数据（商品）...")
    raw_df = fetch_cot_data()
    print(f"  共 {len(raw_df)} 条原始记录")

    print("\n[2/6] 处理商品品种...")
    for code, config in COMMODITIES.items():
        print(f"  {config['name']} ({code})...", end=" ")
        try:
            commodity_df = filter_commodity_data(raw_df, config['pattern'])
            if commodity_df.empty:
                print("未找到数据")
                continue
            records = process_commodity_data(commodity_df, weeks=156)
            if not records:
                print("处理失败")
                continue
            result["commodities"][code] = {
                "name": config['name'], "name_en": config['name_en'],
                "summary": calculate_summary(records), "weekly_data": records
            }
            result["commodity_list"].append({"code": code, "name": config['name'], "name_en": config['name_en']})
            print(f"{len(records)} 周")
        except Exception as e:
            print(f"错误: {e}")

    # ── 2. TFF 外汇 & 加密数据 ─────────────────────────────────────────────
    print("\n[3/6] 获取 TFF 数据（外汇 & 加密货币）...")
    try:
        tff_raw = fetch_tff_data()
        print(f"  共 {len(tff_raw)} 条原始记录")

        for code, config in FX_INSTRUMENTS.items():
            print(f"  {config['name']} ({code})...", end=" ")
            try:
                inst_df = filter_commodity_data(tff_raw, config['pattern'])
                if inst_df.empty:
                    print("未找到数据")
                    continue
                records = process_commodity_data(inst_df, weeks=156, col_map=TFF_COL_MAP)
                if not records:
                    print("处理失败")
                    continue
                result["tff_instruments"][code] = {
                    "name": config['name'], "name_en": config['name_en'],
                    "summary": calculate_summary(records), "weekly_data": records
                }
                result["tff_instrument_list"].append({"code": code, "name": config['name'], "name_en": config['name_en']})
                print(f"{len(records)} 周")
            except Exception as e:
                print(f"错误: {e}")
    except Exception as e:
        print(f"  TFF数据获取失败: {e}")

    # ── 3. COMEX 铜期货期限结构 ────────────────────────────────────────────
    print("\n[4/6] 获取 COMEX 铜期货期限结构...")
    result["copper_curve"] = fetch_copper_curve_data(weeks=156)

    # ── 4. 沪铜（SHFE）期货数据 ───────────────────────────────────────────
    print("\n[5/6] 获取沪铜（SHFE）期货数据...")
    result["shfe_copper"] = fetch_shfe_copper_data(existing_shfe_inventory)

    # ── 5. GVZ 数据 ────────────────────────────────────────────────────────
    gvz_records = fetch_gvz_data(start_year=2023)
    if gvz_records:
        result["gvz"] = gvz_records
    else:
        if os.path.exists(existing_fp):
            try:
                with open(existing_fp, "r", encoding="utf-8") as f:
                    old_gvz = json.load(f).get("gvz", [])
                result["gvz"] = old_gvz
                if old_gvz:
                    print(f"  使用旧 GVZ 数据（{len(old_gvz)} 条）")
            except Exception:
                result["gvz"] = []
        else:
            result["gvz"] = []

    # ── 6. 保存 ────────────────────────────────────────────────────────────
    print("\n[6/6] 保存数据...")
    save_to_json(result)

    print("\n" + "=" * 55)
    print(f"商品品种: {len(result['commodity_list'])} 个  |  TFF品种: {len(result['tff_instrument_list'])} 个")
    print("=" * 55)


if __name__ == "__main__":
    main()

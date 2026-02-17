"""
CFTC COT Report Data Fetcher
- Disaggregated Futures + Options：商品期货（金属、能源、农产品）
  核心关注：Managed Money（管理基金）持仓
- Traders in Financial Futures（TFF）：外汇 & 加密货币
  核心关注：Leveraged Funds（杠杆资金/对冲基金）持仓
"""

import json
import os
from datetime import datetime
import pandas as pd
import cot_reports as cot
import yfinance as yf


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

    result = {
        "commodities": {},
        "commodity_list": [],
        "tff_instruments": {},
        "tff_instrument_list": [],
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # ── 1. COT Disaggregated 商品数据 ─────────────────────────────────────
    print("\n[1/4] 获取 COT Disaggregated 数据（商品）...")
    raw_df = fetch_cot_data()
    print(f"  共 {len(raw_df)} 条原始记录")

    print("\n[2/4] 处理商品品种...")
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
    print("\n[3/4] 获取 TFF 数据（外汇 & 加密货币）...")
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

    # ── 3. GVZ 数据 ────────────────────────────────────────────────────────
    gvz_records = fetch_gvz_data(start_year=2023)
    if gvz_records:
        result["gvz"] = gvz_records
    else:
        existing_fp = os.path.join(OUTPUT_DIR, "cot_data.json")
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

    # ── 4. 保存 ────────────────────────────────────────────────────────────
    print("\n[4/4] 保存数据...")
    save_to_json(result)

    print("\n" + "=" * 55)
    print(f"商品品种: {len(result['commodity_list'])} 个  |  TFF品种: {len(result['tff_instrument_list'])} 个")
    print("=" * 55)


if __name__ == "__main__":
    main()

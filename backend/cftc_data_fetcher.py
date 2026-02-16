"""
CFTC COT Report Data Fetcher
获取多品种期货COT数据并输出JSON供前端使用
报告类型：Disaggregated Futures + Options（精细分类报告）
核心关注：Managed Money（管理基金）持仓 — 对冲基金/CTA/资管机构方向
"""

import json
import os
from datetime import datetime, timedelta
import pandas as pd
import cot_reports as cot
import yfinance as yf


# 支持的品种配置
COMMODITIES = {
    "gold": {
        "name": "黄金",
        "name_en": "GOLD (COMEX)",
        "pattern": r"^GOLD - COMMODITY EXCHANGE"
    },
    "silver": {
        "name": "白银",
        "name_en": "SILVER (COMEX)",
        "pattern": r"^SILVER - COMMODITY EXCHANGE"
    },
    "copper": {
        "name": "铜",
        "name_en": "COPPER (COMEX)",
        "pattern": r"^COPPER.* - COMMODITY EXCHANGE"
    },
    "platinum": {
        "name": "铂金",
        "name_en": "PLATINUM (NYMEX)",
        "pattern": r"^PLATINUM - NEW YORK MERCANTILE"
    },
    "palladium": {
        "name": "钯金",
        "name_en": "PALLADIUM (NYMEX)",
        "pattern": r"^PALLADIUM - NEW YORK MERCANTILE"
    },
    "micro_gold": {
        "name": "微型黄金",
        "name_en": "MICRO GOLD (COMEX)",
        "pattern": r"^MICRO GOLD - COMMODITY EXCHANGE"
    },
    "aluminum": {
        "name": "铝",
        "name_en": "ALUMINUM (COMEX)",
        "pattern": r"^ALUMINUM - COMMODITY EXCHANGE"
    },
    "cobalt": {
        "name": "钴",
        "name_en": "COBALT (COMEX)",
        "pattern": r"^COBALT - COMMODITY EXCHANGE"
    },
    "lithium": {
        "name": "氢氧化锂",
        "name_en": "LITHIUM HYDROXIDE (COMEX)",
        "pattern": r"^LITHIUM HYDROXIDE - COMMODITY EXCHANGE"
    }
}

# 输出路径
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def fetch_cot_data(years: list = None) -> pd.DataFrame:
    """
    获取COT Disaggregated Futures + Options报告数据
    """
    if years is None:
        current_year = datetime.now().year
        # 获取近4年数据以支持3年的时间范围
        years = [current_year - 3, current_year - 2, current_year - 1, current_year]

    all_data = []
    for year in years:
        try:
            print(f"正在获取 {year} 年数据...")
            df = cot.cot_year(year=year, cot_report_type="disaggregated_futopt")
            all_data.append(df)
        except Exception as e:
            print(f"获取 {year} 年数据失败: {e}")

    if not all_data:
        raise ValueError("未能获取任何数据")

    return pd.concat(all_data, ignore_index=True)


def filter_commodity_data(df: pd.DataFrame, pattern: str) -> pd.DataFrame:
    """
    根据正则表达式筛选特定品种数据
    """
    # 查找市场列名
    market_col = None
    for col in df.columns:
        if 'market' in col.lower() and 'exchange' in col.lower():
            market_col = col
            break

    if market_col is None:
        raise ValueError("未找到市场名称列")

    # 筛选数据
    mask = df[market_col].str.match(pattern, case=False, na=False)
    return df[mask].copy()


def get_column_value(row, possible_names, default=0):
    """
    从多个可能的列名中获取值
    """
    for name in possible_names:
        if name in row.index:
            val = row[name]
            if pd.notna(val):
                return int(val)
    return default


def process_commodity_data(df: pd.DataFrame, weeks: int = 52) -> list:
    """
    处理品种数据，返回周度数据列表
    使用 Disaggregated 报告字段：Managed Money / Producer/Merchant
    """
    # 查找日期列 - 优先使用YYYY-MM-DD格式
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

    # 确保日期格式正确
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col, ascending=False)

    # 取近N周数据
    df = df.head(weeks).copy()
    df = df.sort_values(date_col, ascending=True)

    # 列名映射（Disaggregated Futures + Options 格式）
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
        mm_long  = get_column_value(row, col_map['mm_long'])
        mm_short = get_column_value(row, col_map['mm_short'])
        prod_long  = get_column_value(row, col_map['prod_long'])
        prod_short = get_column_value(row, col_map['prod_short'])
        other_long  = get_column_value(row, col_map['other_long'])
        other_short = get_column_value(row, col_map['other_short'])

        record = {
            "date": row[date_col].strftime("%Y-%m-%d"),
            "mm_long":     mm_long,
            "mm_short":    mm_short,
            "mm_spreading": get_column_value(row, col_map['mm_spread']),
            "prod_long":   prod_long,
            "prod_short":  prod_short,
            "other_long":  other_long,
            "other_short": other_short,
            "open_interest": get_column_value(row, col_map['open_interest']),
            "mm_net":    mm_long - mm_short,
            "prod_net":  prod_long - prod_short,
            "other_net": other_long - other_short,
        }
        records.append(record)

    # 计算周度变化
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
    """
    计算汇总指标
    """
    if not records:
        return {}

    latest = records[-1]

    return {
        "latest_date": latest.get("date", ""),
        "mm_net":      latest.get("mm_net", 0),
        "prod_net":    latest.get("prod_net", 0),
        "open_interest": latest.get("open_interest", 0),
        "mm_net_change":   latest.get("mm_net_change", 0),
        "prod_net_change": latest.get("prod_net_change", 0),
        "oi_change":       latest.get("oi_change", 0),
        "long_short_ratio": round(latest.get("mm_long", 0) / max(latest.get("mm_short", 1), 1), 2),
    }


def fetch_gvz_data(start_year: int = 2023) -> list:
    """
    获取 CBOE Gold ETF Volatility Index (^GVZ) 与 SPDR GLD 成交量数据
    按周对齐：GVZ 取每周二收盘价，GLD 成交量取当周累计总量
    """
    print("\n正在获取 GVZ 与 GLD 成交量数据...")
    start = f"{start_year}-01-01"

    # 同时下载 GVZ 和 GLD
    gvz_df = yf.download("^GVZ", start=start, auto_adjust=True, progress=False)
    gld_df = yf.download("GLD",  start=start, auto_adjust=True, progress=False)

    if gvz_df.empty:
        print("  警告: GVZ 数据获取失败")
        return []

    # GVZ 收盘价
    gvz_close = gvz_df["Close"].squeeze()
    gvz_close.index = pd.to_datetime(gvz_close.index).tz_localize(None)

    # GLD 成交量，按周二重采样求和（W-TUE：当周三到本周二的累计量）
    gld_vol = pd.Series(dtype=float)
    if not gld_df.empty:
        gld_vol = gld_df["Volume"].squeeze()
        gld_vol.index = pd.to_datetime(gld_vol.index).tz_localize(None)
        gld_vol = gld_vol.resample("W-TUE").sum()

    # 生成所有周二日期
    start_dt = pd.Timestamp(start)
    end_dt = pd.Timestamp.today()
    tuesdays = pd.date_range(start=start_dt, end=end_dt, freq="W-TUE")

    records = []
    for tue in tuesdays:
        # GVZ：取当天或往前最近交易日
        window = gvz_close[gvz_close.index <= tue]
        if window.empty:
            continue
        gvz_val = round(float(window.iloc[-1]), 2)

        # GLD 成交量：取当周重采样值
        gld_val = None
        if tue in gld_vol.index:
            gld_val = int(gld_vol[tue])
        elif not gld_vol.empty:
            w = gld_vol[gld_vol.index <= tue]
            if not w.empty:
                gld_val = int(w.iloc[-1])

        records.append({
            "date": tue.strftime("%Y-%m-%d"),
            "close": gvz_val,
            "gld_volume": gld_val
        })

    print(f"  成功: {len(records)} 周数据，最新: {records[-1]['date'] if records else 'N/A'}")
    return records


def save_to_json(data: dict, filename: str = "cot_data.json"):
    """
    保存数据为JSON文件
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"数据已保存至: {filepath}")
    return filepath


def main():
    """
    主函数：获取、处理并保存多品种COT数据
    """
    print("=" * 50)
    print("CFTC COT 多品种数据获取程序（Disaggregated Futures + Options）")
    print("=" * 50)

    # 获取数据
    print("\n[1/3] 正在从CFTC获取COT数据...")
    raw_df = fetch_cot_data()
    print(f"获取到 {len(raw_df)} 条原始记录")

    # 处理各品种数据
    print("\n[2/3] 处理各品种数据...")
    result = {
        "commodities": {},
        "commodity_list": [],
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    for code, config in COMMODITIES.items():
        print(f"  处理 {config['name']} ({code})...")
        try:
            commodity_df = filter_commodity_data(raw_df, config['pattern'])
            if commodity_df.empty:
                print(f"    警告: 未找到 {config['name']} 数据")
                continue

            records = process_commodity_data(commodity_df, weeks=156)
            if not records:
                print(f"    警告: {config['name']} 数据处理失败")
                continue

            summary = calculate_summary(records)

            result["commodities"][code] = {
                "name": config['name'],
                "name_en": config['name_en'],
                "summary": summary,
                "weekly_data": records
            }
            result["commodity_list"].append({
                "code": code,
                "name": config['name'],
                "name_en": config['name_en']
            })
            print(f"    成功: {len(records)} 周数据")

        except Exception as e:
            print(f"    错误: {e}")

    # 获取 GVZ 数据（失败时保留旧数据）
    gvz_records = fetch_gvz_data(start_year=2023)
    if gvz_records:
        result["gvz"] = gvz_records
    else:
        # 尝试从已有 JSON 中保留旧的 GVZ 数据
        existing_filepath = os.path.join(OUTPUT_DIR, "cot_data.json")
        if os.path.exists(existing_filepath):
            try:
                with open(existing_filepath, "r", encoding="utf-8") as f:
                    existing = json.load(f)
                old_gvz = existing.get("gvz", [])
                if old_gvz:
                    result["gvz"] = old_gvz
                    print(f"  使用旧 GVZ 数据（{len(old_gvz)} 条）")
                else:
                    result["gvz"] = []
            except Exception:
                result["gvz"] = []
        else:
            result["gvz"] = []

    # 保存JSON
    print("\n[3/3] 保存数据...")
    save_to_json(result)

    # 打印汇总
    print("\n" + "=" * 50)
    print("数据汇总")
    print("=" * 50)
    for item in result["commodity_list"]:
        code = item["code"]
        data = result["commodities"][code]
        s = data["summary"]
        print(f"\n{data['name']} ({data['name_en']}):")
        print(f"  最新日期: {s['latest_date']}")
        print(f"  管理基金净持仓: {s['mm_net']:,}")
        print(f"  生产商净持仓:   {s['prod_net']:,}")
        print(f"  数据周数: {len(data['weekly_data'])}")


if __name__ == "__main__":
    main()

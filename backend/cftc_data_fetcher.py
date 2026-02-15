"""
CFTC COT Report Data Fetcher
获取多品种期货COT数据并输出JSON供前端使用
"""

import json
import os
from datetime import datetime
import pandas as pd
import cot_reports as cot


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
    "crude_oil": {
        "name": "原油",
        "name_en": "CRUDE OIL (NYMEX)",
        "pattern": r"^CRUDE OIL, LIGHT SWEET - NEW YORK MERCANTILE"
    },
    "natural_gas": {
        "name": "天然气",
        "name_en": "NATURAL GAS (NYMEX)",
        "pattern": r"^NATURAL GAS - NEW YORK MERCANTILE"
    }
}

# 输出路径
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def fetch_cot_data(years: list = None) -> pd.DataFrame:
    """
    获取COT Legacy Futures报告数据
    """
    if years is None:
        current_year = datetime.now().year
        # 获取近4年数据以支持3年的时间范围
        years = [current_year - 3, current_year - 2, current_year - 1, current_year]

    all_data = []
    for year in years:
        try:
            print(f"正在获取 {year} 年数据...")
            df = cot.cot_year(year=year, cot_report_type="legacy_fut")
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
    获取足够多的周数以支持时间范围选择
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

    # 列名映射
    col_map = {
        'open_interest': ['Open Interest (All)', 'Open_Interest_All'],
        'noncomm_long': ['Noncommercial Positions-Long (All)', 'NonComm_Positions_Long_All'],
        'noncomm_short': ['Noncommercial Positions-Short (All)', 'NonComm_Positions_Short_All'],
        'noncomm_spread': ['Noncommercial Positions-Spreading (All)', 'NonComm_Positions_Spread_All'],
        'comm_long': ['Commercial Positions-Long (All)', 'Comm_Positions_Long_All'],
        'comm_short': ['Commercial Positions-Short (All)', 'Comm_Positions_Short_All'],
    }

    records = []
    for _, row in df.iterrows():
        noncomm_long = get_column_value(row, col_map['noncomm_long'])
        noncomm_short = get_column_value(row, col_map['noncomm_short'])
        comm_long = get_column_value(row, col_map['comm_long'])
        comm_short = get_column_value(row, col_map['comm_short'])

        record = {
            "date": row[date_col].strftime("%Y-%m-%d"),
            "noncomm_long": noncomm_long,
            "noncomm_short": noncomm_short,
            "noncomm_spreading": get_column_value(row, col_map['noncomm_spread']),
            "comm_long": comm_long,
            "comm_short": comm_short,
            "open_interest": get_column_value(row, col_map['open_interest']),
            "noncomm_net": noncomm_long - noncomm_short,
            "comm_net": comm_long - comm_short,
        }
        records.append(record)

    # 计算周度变化
    for i in range(1, len(records)):
        records[i]["noncomm_net_change"] = records[i]["noncomm_net"] - records[i-1]["noncomm_net"]
        records[i]["comm_net_change"] = records[i]["comm_net"] - records[i-1]["comm_net"]
        records[i]["oi_change"] = records[i]["open_interest"] - records[i-1]["open_interest"]

    if records:
        records[0]["noncomm_net_change"] = 0
        records[0]["comm_net_change"] = 0
        records[0]["oi_change"] = 0

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
        "noncomm_net": latest.get("noncomm_net", 0),
        "comm_net": latest.get("comm_net", 0),
        "open_interest": latest.get("open_interest", 0),
        "noncomm_net_change": latest.get("noncomm_net_change", 0),
        "comm_net_change": latest.get("comm_net_change", 0),
        "oi_change": latest.get("oi_change", 0),
        "long_short_ratio": round(latest.get("noncomm_long", 0) / max(latest.get("noncomm_short", 1), 1), 2),
    }


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
    print("CFTC COT 多品种数据获取程序")
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
        print(f"  非商业净持仓: {s['noncomm_net']:,}")
        print(f"  数据周数: {len(data['weekly_data'])}")


if __name__ == "__main__":
    main()

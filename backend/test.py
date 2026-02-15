import cot_reports as cot

# 获取Disaggregated报告（包含Managed Money分类）
df = cot.cot_year(year=2026, cot_report_type='legacy_fut')

# 筛选黄金数据
# 如何打印

# 指定sheet名称
df.to_excel('gold_cot_data.xlsx', sheet_name='黄金COT数据', index=False)
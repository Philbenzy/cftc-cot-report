import cot_reports as cot

# 获取Disaggregated报告（包含Managed Money分类）
df = cot.cot_year(year=2026, cot_report_type='traders_in_financial_futures_futopt')

# 筛选黄金数据
# 如何打印

# 指定sheet名称
df.to_excel('ttf.xlsx', sheet_name='TTF', index=False)
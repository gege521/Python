import xlsxwriter
#generate a new excel, later save your dataframe into
writer = pd.ExcelWriter(f"exp_monitor_export_keyindex_{qry.date2}.xlsx", engine='xlsxwriter')
exp_monitor_export_keyindex.to_excel(writer, sheet_name='Monitor')
workbook = writer.book
worksheet = writer.sheets['Monitor']
worksheet.set_zoom(80)

#set cells format
percent_fmt1 =  workbook.add_format({'num_format': '0.0%','font_name':'微软雅黑' , 'font_size': 10 ,'bg_color':'#FDFEFE','border':0})
percent_fmt2 =  workbook.add_format({'num_format': '0.00%','font_name':'微软雅黑' , 'font_size': 10 ,'bg_color':'#FDFEFE','border':0})
int_fmt =  workbook.add_format({'num_format': '#,##0','font_name':'微软雅黑' , 'font_size': 10 ,'bg_color':'#FDFEFE','border':0})
string =  workbook.add_format({'num_format':'General','font_name':'微软雅黑' , 'font_size': 10 ,'bg_color':'#FDFEFE','border':0})
worksheet.set_column('A:D', 15,string )
worksheet.set_column('E:H', 15, int_fmt)
worksheet.set_column('I:S', 15, percent_fmt1)
worksheet.set_column('T:U', 15, int_fmt)
worksheet.set_column('V:V', 15, percent_fmt1)
worksheet.set_column('W:AF', 15, int_fmt)
worksheet.set_column('AG:AH', 15, percent_fmt2)
worksheet.set_column('AJ:AM', 15, percent_fmt2)
worksheet.set_column('AI:AI', 15, int_fmt)
worksheet.set_column('AN:AN', 15, int_fmt)
writer.close()


import dateheader
from report import Report 
import sys
import os
os.environ['NLS_LANG'] = 'American_America.AL32UTF8'

args = sys.argv
dateHeader = dateheader.dateHeader(args)
start_date, end_date = dateHeader.validateArgs()
if start_date is False and end_date is False:
    sys.exit("Error in arguments, use correct datetime format dd/mm/yyy")
print(start_date, end_date)
column_names = ['dt','user_type','operator','connection_type','amount','seconds','minutes','dollars']
constant_columns = ['dt','user_type','operator','connection_type']
incoming_report = Report(start_date, end_date, sql_path='incoming.sql', column_names=column_names )
df = incoming_report.get_df()
incoming_report.insertDB(df, dbname="incoming", constant_columns = constant_columns)

# insert to DB
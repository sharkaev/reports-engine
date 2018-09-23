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
column_names = ['dt', 'tariff_name', 'value']
traffic_report = Report(start_date, end_date, sql_path='traffic.sql', column_names=column_names )
df = traffic_report.get_df()
traffic_report.insertDB(df, dbname="traffic", constant_columns = ['contract_type_name_en', 'direction_name_ru', 'location_type_name_ru', 'connection_type_name_en', 'dop_connection_type', 'tariff_name_ru', 'region_name_ru', 'dt', 'service_class_name_en'])

# insert to DB
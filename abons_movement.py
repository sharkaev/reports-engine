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
column_names = ['dt', 'tariff_name_ru', 'value']
constant_columns = ['dt','tariff_name_ru']

abons_movement = Report(start_date, end_date, sql_path='abons_movement.sql', column_names=column_names )
df = abons_movement.get_df()
abons_movement.insertDB(df, dbname="abons_movement", constant_columns = constant_columns)

# insert to DB
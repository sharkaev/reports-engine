import cx_Oracle
import config
import os
import pandas as pd
import logger
import psycopg2

os.environ['NLS_LANG'] = 'American_America.AL32UTF8'

class Report:
    def __init__(self, start_date, end_date, sql_path, column_names):
        self.connection = cx_Oracle.connect(config.CONNECT_STRING)
        self.cursor = self.connection.cursor()

        self.column_names = column_names
        self.start_date = start_date
        self.end_date = end_date
        
        self.sql = self.modify_sql(sql_path)
        print("Collecting data")
        self.cursor.execute(self.sql)
        self.data = self.cursor.fetchall()
        if self.connection is not None:
            self.connection.close()
        self.df = pd.DataFrame(data=self.data )
        self.df.columns = self.column_names


    def get_df(self):
        return self.df
    
    def modify_sql(self, sql_path):
        file = open(os.path.join(config.SQL_SCRIPTS, sql_path), 'r')
        sql = s = " ".join(file.readlines())
        sql = sql.replace('START_DATE', self.start_date).replace('END_DATE', self.end_date)
        
        return sql
    
    def insert_row (self, cursor, conn,  dbname, row_as_dic ):
        values = row_as_dic.values()
        values_as_string = ""
        i = 1
        len_of_values = len(values)
        for value in values:
            if i!=len_of_values:
                values_as_string += f"'{value}', "
            else:
                values_as_string += f"'{value}'"
            i+=1
        insert_sql = f"INSERT INTO {dbname} ({','.join(row_as_dic.keys() )}) VALUES ({values_as_string})"
        cursor.execute(insert_sql)
        conn.commit()     

    def update_row( self, cursor, conn, dbname, row_as_dic, select_sql_where):
        update_sql_set = ""
        i = 1
        len_of_column_names = len(row_as_dic.keys())
        for column_name in row_as_dic.keys():
            if i == len_of_column_names:
                update_sql_set += f" {column_name } = '{row_as_dic[column_name]}' "
            else:
                update_sql_set += f" {column_name } = '{row_as_dic[column_name]}', "
            i+=1
        update_sql = f"UPDATE {dbname} SET { update_sql_set  } WHERE {select_sql_where}"
        cursor.execute(update_sql)
        conn.commit()
    
    def select_row(self, cursor, conn, dbname, all_columns, select_sql_where):
        select_sql = f"SELECT {','.join(all_columns)} from {dbname} where {select_sql_where}"
        cursor.execute(select_sql)
        result = cursor.fetchone()
        if result is None:
            return None
        else:
            result_as_dict = {}
            i = 0
            
            for column in all_columns:
                result_as_dict[column] = str( result[i] )
                i+=1
            return result_as_dict


    def master(self, constant_columns, row, all_columns):
        row_as_dic = {}
        select_sql_where = ""
        for column in all_columns:
            single_value = str( getattr(row, column) )
            single_value = single_value.replace('\'','')
            single_value_with_quotes = str(single_value)
            row_as_dic[column] = single_value_with_quotes
        i = 0
        for column in constant_columns:
            if i == 0:
                select_sql_where += f"{column} = '{row_as_dic[column]}' "
            else:
                select_sql_where += f" and {column} = '{row_as_dic[column]}'"
            i += 1
        
        return row_as_dic, select_sql_where

        



    def insertDB(self, df, dbname, constant_columns ):
        new_rows = equal_rows = updated_rows = 0
        postgre_conn = psycopg2.connect(config.POSTGRE_STRING)
        postgre_cursor = postgre_conn.cursor()
        all_columns = df.columns
        df['dt'] = df['dt'].astype(str)
        # tariff manipulation
        if 'tariff_name_ru' in df.columns:
            df_names = pd.read_csv('L:\\Statistics and Analysis\\human_names_of_tariffs\\names_2.csv', delimiter=';', encoding='ansi', names=['as_is', 'to_be'])
            dic = df_names.set_index('as_is')['to_be'].to_dict()
            df['tariff_name_ru'] = df['tariff_name_ru'].apply(lambda x: dic[x] if x in dic else x)
            agg_info = {}
            for column in all_columns:
                if column not in constant_columns:
                    agg_info[column] = 'sum'
                else:
                    agg_info[column] = 'first'
            print(agg_info)
            df = df.groupby(constant_columns).agg(agg_info).reset_index(drop=True)

        
        for row in df.itertuples():
            # dictionary from tuple
            
            row_as_dic, select_sql_where = self.master(constant_columns=constant_columns, row=row, all_columns=all_columns )

            result = self.select_row(cursor=postgre_cursor, conn=postgre_conn, dbname=dbname, all_columns=all_columns, select_sql_where=select_sql_where) 
            if result is not None:
                
                if result == row_as_dic:
                   equal_rows += 1
                else:
                    self.update_row(conn=postgre_conn, cursor=postgre_cursor, dbname=dbname, row_as_dic=row_as_dic, select_sql_where=select_sql_where)
                    logger.Logger(result, row_as_dic, dbname)
                    updated_rows += 1
            else:
                self.insert_row(conn=postgre_conn, cursor=postgre_cursor, dbname=dbname, row_as_dic=row_as_dic)
                new_rows += 1
                 
        postgre_conn.close()
        print("updated_rows", updated_rows)
        print("new_rows", new_rows)
        print("equal_rows", equal_rows)
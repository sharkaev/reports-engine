import config
import psycopg2
import datetime
import json
class Logger:
    def __init__(self, old_data, new_data, table_name):
        postgre_conn = psycopg2.connect(config.POSTGRE_STRING)
        postgre_cursor = postgre_conn.cursor()
        postgre_cursor.execute("INSERT INTO logs (dt, old_data, new_data, table_name) values (%s, %s, %s, %s)", (datetime.datetime.now(), json.dumps(old_data, ensure_ascii=False), json.dumps(new_data, ensure_ascii=False, use_decimal=True), table_name))
        postgre_conn.commit()
        print('Inserted to logs', old_data, new_data, table_name)

        
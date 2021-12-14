import accountbook as acb
import pymysql 
import pandas as pd

kargv = acb.ReadSetting()
conn = pymysql.connect(**kargv, charset='utf8', db='stockdata')

cursor = conn.cursor() 

sql = '''
        select column_name 
        from information_schema.columns
        where table_name = 'codelist'
      '''

cursor.execute(sql) 
rows = pd.DataFrame(cursor.fetchall())
rows.columns = list(map(lambda x: x[0], cursor.description))
print(rows)

conn.close() 

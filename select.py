import accountbook as acb
import pymysql 
import pandas as pd

kargv = acb.ReadSetting()
conn = pymysql.connect(**kargv, charset='utf8', db='stockdata')

cursor = conn.cursor() 

sql = "SELECT COLUMN_NAME, COLUMN_TYPE, COLUMN_KEY, IS_NULLABLE, EXTRA FROM information_schema.COLUMNS WHERE TABLE_NAME='accountbook'"
#sql = "SELECT COLUMN_NAME, COLUMN_TYPE, COLUMN_KEY, IS_NULLABLE, EXTRA FROM information_schema.COLUMNS WHERE TABLE_NAME='codelist'"

cursor.execute(sql) 
rows = pd.DataFrame(cursor.fetchall())
rows.columns = list(map(lambda x: x[0], cursor.description))
print(rows)

conn.close() 

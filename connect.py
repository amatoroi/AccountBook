import pymysql 
import pandas as pd

conn = pymysql.connect(host='localhost', port=4306, user='amatoroi', password='1234', charset='utf8', db='stockdata') 
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

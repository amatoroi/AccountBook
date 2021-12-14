import pymysql 

conn = pymysql.connect(host='localhost', port=4306, user='amatoroi', password='1234', charset='utf8', db='stockdata') 
cursor = conn.cursor() 

lcls_cd  = "trnsc_type_detl"
comcd    = "9902"
comcd_nm = "무상출금(고)"
comcd_detl = '''
                거래형태: 배당, 유무상증자, 주식병합, 분할 등 거래자의 action없이 잔고 변동
             '''

sql = f'''
    INSERT INTO codelist (lcls_cd, comcd, comcd_nm, comcd_detl)
    values ('{lcls_cd}', '{comcd}', '{comcd_nm}', '{comcd_detl}')
    ''' 
cursor.execute(sql) 
conn.commit() 


conn.close() 

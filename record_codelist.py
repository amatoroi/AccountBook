import pymysql 
import accountbook as acb

kargv = acb.ReadSetting()
conn = pymysql.connect(**kargv, charset='utf8', db='stockdata')
cursor = conn.cursor() 

lcls_cd  = "agent"
comcd    = "200"
comcd_nm = "KINS"
comcd_detl = comcd_nm

sql = f'''
    INSERT INTO codelist (lcls_cd, comcd, comcd_nm, comcd_detl)
    values ('{lcls_cd}', '{comcd}', '{comcd_nm}', '{comcd_detl}')
    ''' 
#cursor.execute(sql) 
conn.commit() 
conn.close() 

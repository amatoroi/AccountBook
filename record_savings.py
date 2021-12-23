import accountbook as acb
import pymysql
import pandas as pd
import os
os.system('clear')

kargv = acb.ReadSetting()
conn = pymysql.connect(**kargv, charset='utf8', db='stockdata')
cursor = conn.cursor() 

# 날짜 입력 부분
while True:
    try:
        date = input("(1/5) 날짜(YYYYMMDD):")
        pd.to_datetime(date, format = '%Y%m%d')
        os.system('clear')
        break
    except ValueError:
        os.system('clear')
        print("   *** 에러: 정상적인 날짜가 아닙니다 *** ")

# 거래기관 코드 입력 부분
sql = "select comcd 코드, comcd_nm 코드명 from codelist where lcls_cd = 'agent'"
cursor.execute(sql)
rows = pd.DataFrame(cursor.fetchall())
rows.columns = list(map(lambda x: x[0], cursor.description))
while True:
    print(rows)
    agent = input("(2/5) 거래 은행 코드 입력:")
    if agent in rows['코드'].values:
        os.system('clear')
        break
    else:
        os.system('clear')
        print(" *** 에러: 정상적인 코드가 아닙니다. *** ")

# 거래기관 코드 입력 부분
sql = "select comcd 코드, comcd_nm 코드명 from codelist where lcls_cd = 'agent'"
cursor.execute(sql)
rows = pd.DataFrame(cursor.fetchall())
rows.columns = list(map(lambda x: x[0], cursor.description))
while True:
    print(rows)
    tgt_agent = input("(3/5) 상대 금융사 코드 입력:")
    if tgt_agent in rows['코드'].values:
        os.system('clear')
        break
    else:
        os.system('clear')
        print(" *** 에러: 정상적인 코드가 아닙니다. *** ")


# 거래 종류 대분류 코드 입력 부분
sql = "select comcd 코드, comcd_nm 코드명 from codelist where lcls_cd = 'trnsc_reason'"
cursor.execute(sql)
rows = pd.DataFrame(cursor.fetchall())
rows.columns = list(map(lambda x: x[0], cursor.description))
while True:
    print(rows)
    trnsc_reason = input("(4/5) 입출금사유:")
    if trnsc_reason in rows['코드'].values:
        os.system('clear')
        break
    else:
        os.system('clear')
        print(" *** 에러: 정상적인 코드가 아닙니다. *** ")

# 거래량(금액) 입력 부분
while True:
    try:
        trnsc_amnt = input("(5/5) 거래금액 입력:")
        float(trnsc_amnt)
        os.system('clear')
        break
    except ValueError:
        os.system('clear')
        print(" *** 에러: 숫자만 입력하여야 합니다. *** ")

sql = f'''
    INSERT INTO savings (date, agent, tgt_agent, trnsc_reason, trnsc_amnt)
    values ('{date}', '{agent}', '{tgt_agent}', '{trnsc_reason}', {trnsc_amnt})
    ''' 

print(sql)

#cursor.execute(sql) 
#conn.commit() 


#conn.close() 

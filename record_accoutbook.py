import accountbook as acb
import pymysql
import pandas as pd
import os
os.system('clear')

kargv = acb.ReadSetting()
conn = pymysql.connect(**kargv, charset='utf8', db='stockdata')
cursor = conn.cursor() 

# 연관 SEQ 입력부분
while True:
    try:
        rel_seq = input("(1/7) 연관SEQ 입력(NULL일 경우 엔터): ")
        if not rel_seq:
            rel_seq = 'null'
            os.system('clear')
            break
        int(rel_seq)
        os.system('clear')
        break
    except ValueError:
        os.system('clear')
        print("   *** 숫자만 입력하거나, 미입력하여야 합니다. ***")

# 날짜 입력 부분
while True:
    try:
        date = input("(2/7) 날짜(YYYYMMDD):")
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
    agent = input("(3/7) 거래 증권사 코드 입력:")
    if agent in rows['코드'].values:
        os.system('clear')
        break
    else:
        os.system('clear')
        print(" *** 에러: 정상적인 코드가 아닙니다. *** ")

# 거래 종류 대분류 코드 입력 부분
sql = "select comcd 코드, comcd_nm 코드명 from codelist where lcls_cd = 'trnsc_type'"
cursor.execute(sql)
rows = pd.DataFrame(cursor.fetchall())
rows.columns = list(map(lambda x: x[0], cursor.description))
while True:
    print(rows)
    trnsc_type = input("(4/7) 거래종류 대분류 코드 입력:")
    if trnsc_type in rows['코드'].values:
        os.system('clear')
        break
    else:
        os.system('clear')
        print(" *** 에러: 정상적인 코드가 아닙니다. *** ")

# 거래 종류 중분류 코드 입력 부분
sql = "select comcd 코드, comcd_nm 코드명 from codelist where lcls_cd = 'trnsc_type_sub'"
cursor.execute(sql)
rows = pd.DataFrame(cursor.fetchall())
rows.columns = list(map(lambda x: x[0], cursor.description))
while True:
    print("주식거래일 경우, 종목코드를 현금거래일 경우에는 아래의 통화코드를 입력하세요")
    print(rows)
    trnsc_type_sub = input("(5/7) 거래종류 중분류 코드 입력:")
    os.system('clear')
    break


# 거래 종류 소분류 코드 입력 부분
sql = "select comcd 코드, comcd_nm 코드명 from codelist where lcls_cd = 'trnsc_type_detl'"
cursor.execute(sql)
rows = pd.DataFrame(cursor.fetchall())
rows.columns = list(map(lambda x: x[0], cursor.description))
while True:
    print(rows)
    trnsc_type_detl = input("(6/7) 거래종류 상세분류 코드 입력:")
    if trnsc_type_detl in rows['코드'].values:
        os.system('clear')
        break
    else:
        os.system('clear')
        print(" *** 에러: 정상적인 코드가 아닙니다. *** ")

# 거래량(금액) 입력 부분
while True:
    try:
        trnsc_amnt = input("(7/7) 거래금액(수량) 입력:")
        float(trnsc_amnt)
        os.system('clear')
        break
    except ValueError:
        os.system('clear')
        print(" *** 에러: 숫자만 입력하여야 합니다. *** ")

sql = f'''
    INSERT INTO accountbook (rel_seq, date, agent, trnsc_type, trnsc_type_sub, trnsc_type_detl, trnsc_amnt)
    values ({rel_seq}, '{date}', '{agent}', '{trnsc_type}', '{trnsc_type_sub}','{trnsc_type_detl}', {trnsc_amnt})
    ''' 

print(sql)

cursor.execute(sql) 
conn.commit() 


conn.close() 

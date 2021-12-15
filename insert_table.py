import accountbook as acb
import pymysql
import pandas as pd

kargv = acb.ReadSetting()
conn = pymysql.connect(**kargv, charset='utf8', db='stockdata')
cursor = conn.cursor() 

# 연관 SEQ 입력부분
while True:
    try:
        rel_seq = input("연관SEQ 입력(NULL일 경우 엔터): ")
        if not rel_seq:
            rel_seq = None
            break
        int(rel_seq)
        break
    except ValueError:
        print("   *** 숫자만 입력하거나, 미입력하여야 합니다. ***")

# 날짜 입력 부분
while True:
    try:
        date = input("날짜(YYYYMMDD):")
        pd.to_datetime(date, format = '%Y%m%d')
        break
    except ValueError:
        print("   *** 에러: 정상적인 날짜가 아닙니다 *** ")

# 거래기관 코드 입력 부분
sql = "select comcd 코드, comcd_nm 코드명 from codelist where lcls_cd = 'agent'"
cursor.execute(sql)
rows = pd.DataFrame(cursor.fetchall())
rows.columns = list(map(lambda x: x[0], cursor.description))
while True:
    print(rows)
    agent = input("거래 증권사 코드 입력:")
    if agent in rows['코드'].values:
        break
    else:
        print(" *** 에러: 정상적인 코드가 아닙니다. *** ")

# 거래 종류 대분류 코드 입력 부분
sql = "select comcd 코드, comcd_nm 코드명 from codelist where lcls_cd = 'trnsc_type'"
cursor.execute(sql)
rows = pd.DataFrame(cursor.fetchall())
rows.columns = list(map(lambda x: x[0], cursor.description))
while True:
    print(rows)
    trnsc_type = input("거래종류 대분류 코드 입력:")
    if trnsc_type in rows['코드'].values:
        break
    else:
        print(" *** 에러: 정상적인 코드가 아닙니다. *** ")

# 거래 종류 소분류 코드 입력 부분
sql = "select comcd 코드, comcd_nm 코드명 from codelist where lcls_cd = 'trnsc_type_detl'"
cursor.execute(sql)
rows = pd.DataFrame(cursor.fetchall())
rows.columns = list(map(lambda x: x[0], cursor.description))
while True:
    print(rows)
    trnsc_type_detl = input("거래종류 상세분류 코드 입력:")
    if trnsc_type_detl in rows['코드'].values:
        break
    else:
        print(" *** 에러: 정상적인 코드가 아닙니다. *** ")

# 거래량(금액) 입력 부분
while True:
    try:
        trnsc_amnt = input("거래금액(수량) 입력:")
        int(trnsc_amnt)
        break
    except ValueError:
        print(" *** 에러: 숫자만 입력하여야 합니다. *** ")

sql = f'''
    INSERT INTO accountbook (rel_seq, date, agent, trnsc_type, trnsc_type_detl, trnsc_amnt)
    values ({rel_seq}, '{date}', '{agent}', '{trnsc_type}', '{trnsc_type_detl}', {trnsc_amnt})
    ''' 

print(sql)

#cursor.execute(sql) 
#conn.commit() 


#conn.close() 

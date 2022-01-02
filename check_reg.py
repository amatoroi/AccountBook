import accountbook as acb
import pymysql 
import pandas as pd

kargv = acb.ReadSetting()
conn = pymysql.connect(**kargv, charset='utf8', db='stockdata')

cursor = conn.cursor() 
# 주식계좌 현금잔고
sql = '''
    select 
    원화입금합계 - 원화출금합계 as 원화잔액,
    외화입금합계 - 외화출금합계 as 외화잔액
    from (
    select 
    ( SELECT sum(trnsc_amnt) from accountbook where agent = '001' and trnsc_type_sub = 'C010' and trnsc_type_detl in ('0201', '9901') ) as 원화입금합계,
    ( SELECT sum(trnsc_amnt) from accountbook where agent = '001' and trnsc_type_sub = 'C010' and trnsc_type_detl in ('0202', '9902') ) as 원화출금합계,
    ( SELECT sum(trnsc_amnt) from accountbook where agent = '001' and trnsc_type_sub = 'C020' and trnsc_type_detl in ('0201', '0211', '9901') ) as 외화입금합계,
    ( SELECT sum(trnsc_amnt) from accountbook where agent = '001' and trnsc_type_sub = 'C020' and trnsc_type_detl in ('0202', '0212', '9902') ) as 외화출금합계
    from dual) a;
      '''
cursor.execute(sql) 
rows = pd.DataFrame(cursor.fetchall())
rows.columns = list(map(lambda x: x[0], cursor.description))
print('현금잔액')
print(rows)

## lambda 로 cash에 대한 df를 별도로 만들어서 관리하는 것이 제일 좋을 듯 날짜 계산만 새로 하면 되니까
cursor.execute('select * from accountbook')
df = pd.DataFrame(cursor.fetchall())
df.columns = list(map(lambda x: x[0], cursor.description))

print( \
    (df[ (df['agent']=='001') & (df['trnsc_type_sub']=='C010') & (df['trnsc_type_detl'].isin(['0201','9901'])) ].loc[:,['trnsc_amnt']].sum() - \
    df[ (df['agent']=='001') & (df['trnsc_type_sub']=='C010') & (df['trnsc_type_detl'].isin(['0202','9902'])) ].loc[:,['trnsc_amnt']].sum()).values[0] )
print( \
    (df[ (df['agent']=='001') & (df['trnsc_type_sub']=='C020') & (df['trnsc_type_detl'].isin(['0201','0211','9901'])) ].loc[:,['trnsc_amnt']].sum() - \
    df[ (df['agent']=='001') & (df['trnsc_type_sub']=='C020') & (df['trnsc_type_detl'].isin(['0202','0212','9902'])) ].loc[:,['trnsc_amnt']].sum()).values[0] )



# 주식계좌 주식잔고
sql2 = '''
        select scode, sum(amnt) from (
        select 
        trnsc_type_sub as scode,
        date,
        case 
            when trnsc_type_detl = '0101'
            then trnsc_amnt
            when trnsc_type_detl = '0102'
            then -1*trnsc_amnt
        end as amnt
        from accountbook where trnsc_type_detl in ('0101' , '0102') order by date ) a
        group by scode
       '''

cursor.execute(sql2) 
rows = pd.DataFrame(cursor.fetchall())
rows.columns = list(map(lambda x: x[0], cursor.description))
print('\n주식잔고')
print(rows)

sql3 = '''
        select * from accountbook where date <> '20211201'
       '''

cursor.execute(sql3) 
df = pd.DataFrame(cursor.fetchall())
df.columns = list(map(lambda x: x[0], cursor.description))
print('\nCHECK TEST: 주식이나 외화를 매수한 경우에, 현금출금이 있어야 함')
con = [ ['0101','0211'], ['0102','0212'] ]
typ = ['0202','0201']
sr1 = ['매수','매도']
sr2 = ['출금','입금']
for i in range(2):
    rows = df[ df['trnsc_type_detl'].isin(con[i]) ]
    suc_str = f'  Success: 모든 주식 및 외화 {sr1[i]}가 현금 {sr2[i]}과 1:1로 대응됩니다.'
    err_str = f'    Error: 주식 및 외화 {sr1[i]}가 현금 {sr2[i]}과 1:1로 대응되지 않아요.'
    try:
        test = pd.merge(left = rows, right = df[ df['trnsc_type_detl'].isin([typ[i]]) ], \
                        how='left', left_on='seq', right_on ='rel_seq')
        ref = test[test['rel_seq_y'].isna()].loc[:,['seq_x','date_x','agent_x','trnsc_type_x','trnsc_type_sub_x','trnsc_type_detl_x','trnsc_amnt_x']] 
        if len(ref) == 0:
            print(suc_str)
        else:
            print(err_str, '아래참고')
            print(ref)
    except:
        print('!!!!!!! 몰라!! 뭔가 문제 생김.')
conn.close() 

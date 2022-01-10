from dash import html

import ast
import accountbook as acb
import pymysql
import pandas as pd

def ReadSetting():
    file = open('./setting', 'r')
    contents = file.read()
    dictionary = ast.literal_eval(contents)
    return dictionary

def genTable(dataframe, max_rows=10):
    return html.Table([
             html.Thead(
               html.Tr([html.Th(col) for col in dataframe.columns])
             ),
             html.Tbody([
               html.Tr([
                 html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
               ]) for i in range(min(len(dataframe), max_rows))
             ])
           ])

def readCodes(cons=None):
    if cons is None:
        cons = 'agent'

    kargv = ReadSetting()
    conn = pymysql.connect(**kargv, charset='utf8', db='stockdata')
    cursor = conn.cursor()

    sql = f'''
            select comcd_nm as label, comcd as value from codelist where lcls_cd = '{cons}'
           '''
    cursor.execute(sql)
    df = pd.DataFrame(cursor.fetchall())
    df.columns = list(map(lambda x: x[0], cursor.description))
    conn.close()

    cd_dict = df.to_dict('records')
    return cd_dict

def rcrdAccntBk(*vals):
    kargv = ReadSetting()
    conn = pymysql.connect(**kargv, charset='utf8', db='stockdata')
    cursor = conn.cursor()

    rel_seq    = val[0]
    date       = val[1]
    agent      = val[2]
    trnsc_type = val[3]
    trnsc_type_sub  = val[4]
    trnsc_type_detl = val[5]
    trnsc_amnt      = val[6]

    sql = f'''
            INSERT INTO accountbook (rel_seq, date, agent, 
                                     trnsc_type, trnsc_type_sub, 
                                     trnsc_type_detl, trnsc_amnt)
            values ({rel_seq}, '{date}', '{agent}', 
                    '{trnsc_type}', '{trnsc_type_sub}','{trnsc_type_detl}', {trnsc_amnt})
           '''
    cursor.execute(sql)
    conn.commit()
    conn.close()

def readData():
    kargv = ReadSetting()
    conn = pymysql.connect(**kargv, charset='utf8', db='stockdata')
    cursor = conn.cursor() 

    sql = '''
            select 
                ta.seq as 순번,
                ta.date as 날짜,
                (select comcd_nm from codelist where lcls_cd = 'agent' and comcd = ta.agent) as 거래처,
                (select comcd_nm from codelist where lcls_cd = 'trnsc_type' and comcd = ta.trnsc_type) as 거래수단,
                case
                    when ta.trnsc_type_sub = 'C010'
                    then '원화'
                    when ta.trnsc_type_sub = 'C020'
                    then '달러화'
                    else ta.trnsc_type_sub
                end as 거래대상,
                (select comcd_nm from codelist where lcls_cd = 'trnsc_type_detl' and comcd = ta.trnsc_type_detl) as 거래방법,
                case 
                    when substr(ta.trnsc_type_detl, -1, 1) = '1'
                    then ta.trnsc_amnt 
                    when substr(ta.trnsc_type_detl, -1, 1) = '2'
                    then -1 * ta.trnsc_amnt 
                end as 거래량,
                (select comcd_nm from codelist where lcls_cd = 'trnsc_type' and comcd = tb.trnsc_type) as 매수도수단,
                case
                    when tb.trnsc_type_sub = 'C010'
                    then '원화'
                    when tb.trnsc_type_sub = 'C020'
                    then '달러화'
                    else tb.trnsc_type_sub
                end as 매수도대상,
                (select comcd_nm from codelist where lcls_cd = 'trnsc_type_detl' and comcd = tb.trnsc_type_detl) as 매수도방법,
                case 
                    when substr(tb.trnsc_type_detl, -1, 1) = '1'
                    then tb.trnsc_amnt 
                    when substr(tb.trnsc_type_detl, -1, 1) = '2'
                    then -1 * tb.trnsc_amnt 
                end as 매수도대금
            from (
                select * 
                from accountbook where rel_seq is null
                ) ta
            left join (select * from accountbook where rel_seq is not null) tb on ta.seq = tb.rel_seq
          '''
    cursor.execute(sql)
    df = pd.DataFrame(cursor.fetchall())
    df.columns = list(map(lambda x: x[0], cursor.description))
    df.sort_values(by=['날짜', '순번'], inplace=True)
    #df.drop('순번', axis = 1,  inplace=True)
    #df.insert(0, '순번', [ x + 1 for x in range(len(df)) ] )

    conn.close() 

    return df.tail(10)

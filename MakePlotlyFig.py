# -*- coding:UTF-8 -*-
import pymysql
import pandas as pd
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime
import re

import sys
sys.path.insert(1, '/home/amatoroi/Documents/ProjectBullMarket/')
import accountbook as acb
import ProjBullMrkt as bmk

import time


def GetChart(stddt = '20211210'):
    #   시작날짜 부터 오늘까지 날짜데이터 추출
    oday = pd.to_datetime('20211201', format='%Y%m%d')
    sday = pd.to_datetime(stddt, format='%Y%m%d')
    tday = pd.to_datetime('today') #-pd.Timedelta(1, unit='day')
    df = pd.DataFrame(pd.date_range(start=sday, end= tday, freq='1D', closed='right'))
    #############   string type 날짜가 필요할지 몰라서 일단 갖고 있기
    df.columns = ['Date']
    df.set_index('Date', inplace = True)

    #   기록된 모든 자산정보 데이터 획득
    kargv = acb.ReadSetting()
    conn = pymysql.connect(**kargv, charset='utf8', db='stockdata')
    cursor = conn.cursor()
    ##  자산정보 데이터 획득
    cursor.execute('select * from accountbook')
    raw = pd.DataFrame(cursor.fetchall())
    raw.columns = list(map(lambda x: x[0], cursor.description))
    raw['date_dt'] = pd.to_datetime(raw['date'])
    raw = raw[raw['date_dt'].between(oday, tday, 'both')].copy()
    for idx, row in raw.iterrows():
        if row['trnsc_type_detl'] not in ['0101','0201','0211','9901']:
            raw.loc[idx, 'trnsc_amnt'] = row['trnsc_amnt']*-1
    ##  자산 중 외환과 원화에 대한 구분 값 확득 
    lcode = raw['trnsc_type_sub'].unique().tolist() #################### 핵심ㅑ
    conn.close()

    #   자산별 날짜별 정보 삽입
    dfa = df.copy()
    for idx, row in dfa.iterrows():
        for cd in lcode:
            dfa.loc[idx, cd] =  raw[raw['date_dt'].between(oday, idx) & raw['trnsc_type_sub'].isin([cd])]['trnsc_amnt'].sum()

    start = time.time()

    #   자산정보 데이터로 부터 데이터 수집이 필요한 종목 또는 외환종류 수집
    for i in range( len(lcode) ):
        if   lcode[i] == 'C010': lcode[i] = 'KRW'
        elif lcode[i] == 'C020': lcode[i] = 'USDKRW=X'
        elif len(lcode[i]) == 6 and re.match('^([0-9]+)',lcode[i]): continue
        elif re.match('([A-Z]+):([A-Z]+)',lcode[i]):
            lcode[i] = re.split(':',lcode[i])[1]
    dfa.columns = lcode
    ##  자산평가를 위한 종목 및 외환 날짜별 정보 추출
    dfm = df.copy()
    dfp = pd.DataFrame(pd.date_range(start=oday, end=tday, freq='1D'))
    dfp.columns = ['Date']
    dfp.set_index('Date', inplace = True)

    for cd in lcode:
        if cd == 'KRW': continue
        elif len(cd) == 6 and re.match('^([0-9]+)', cd):
            tmp = bmk.GetPriceList(cd)['Close']
            dfp[cd] = tmp[dfp.index.min(): dfp.index.max()]
        else:
            dfp[cd] = yf.Ticker(cd).history(start = oday, end = tday, interval='1d')['Close']

    for idx, row in dfm.iterrows():
        for cd in lcode:
            if cd == 'KRW':
                dfm.loc[idx, cd] = 1
            else:
                tmp = dfp[cd].dropna()
                tmp = tmp[oday: idx]
                dfm.loc[idx, cd] = tmp[tmp.index == tmp.index.max()].values[0]

    print("YahooFinance Scraping time:", time.time()-start)

    #   자산정보 데이터와 종목 및 외환 날짜별 정보의 곱으로 최종 데이터 만들기
    for idx, row in df.iterrows():
        for cd in lcode:
            if cd in ('KRW', 'USDKRW=X'):
                df.loc[idx, cd] = dfm.loc[idx,cd] * dfa.loc[idx,cd]
            elif len(cd) == 6 and re.match('^([0-9]+)', cd):
                df.loc[idx, cd] = dfm.loc[idx,cd] * dfa.loc[idx,cd]
            else:
                df.loc[idx, cd] = dfm.loc[idx,'USDKRW=X'] * dfm.loc[idx,cd] * dfa.loc[idx,cd]

    # 자산정보 Normalization
    df = df.div(df.sum(axis=1), axis =0)


    # 데이터 정리
    plotdata = pd.DataFrame(columns= ['Date', 'Category', 'Code', 'Amount'])
    for idx, value in df.iterrows():
        for cd in lcode:
            if cd in ('KRW', 'USDKRW=X'):
                c = '현금'
                if cd == 'USDKRW=X': cn = 'USD'
                else: cn = cd
            elif len(cd) == 6 and re.match('^([0-9]+)', cd):
                c = '한국주식'
                cn = cd
            else:
                c = '미국주식'
                cn = cd
            plotdata = pd.concat([plotdata, \
                                  pd.DataFrame(data = [[idx, c, cn, df.loc[idx,cd]]], \
                                               columns=['Date', 'Category','Code', 'Amount'])])

    print(plotdata)

    # chart용 색상 만들기
    key = plotdata[plotdata['Date'] == pd.to_datetime('20220101',format='%Y%m%d'    )].groupby(by='Category')['Amount'].sum().index.tolist()
    pcolr = pd.DataFrame([{'한국주식':'rgb(110,17,1)','미국주식':'rgb(10,125,0)','현금':'rgb(0,0,0)'}])
    pie_colors = pcolr[key].loc[0,:].tolist()

    lcode = plotdata['Code'].unique().tolist()
    lcode.sort()
    no_k = 0
    no_e = 0
    for i in range(len(lcode)):
        if lcode[i] == 'KRW':
            del lcode[i]
            lcode.insert(0, 'KRW')
        elif lcode[i] == 'USD':
            del lcode[i]
            lcode.insert(0, 'USD')
        else:
            if len(lcode[i]) == 6 and re.match('^([0-9]+)', lcode[i]):
                no_k = no_k + 1
            else:
                no_e = no_e + 1


## 그래프 그리기
    fig = make_subplots(
        rows=2, cols=3,
        specs=[ [{'type':'xy', 'colspan':2}, None,  {'type':'domain'}],
                [{'type':'xy'}, {'type':'domain'}, {'type':'domain'}] ]
        , column_widths = [1.0, 1.0, 1.0]
        , row_heights =   [1.0, 1.0]
        , horizontal_spacing = 0.05
        , vertical_spacing = 0.1
        , subplot_titles = ['자산변동', '자산비중']
        )

    init_k = 60
    init_r = 0
    init_g = 0
    for cd in lcode:
        if cd in ('KRW', 'USD'):
            ccode = f'rgb({init_k},{init_k},{init_k})'
            init_k = init_k + 60
        elif len(cd) == 6 and re.match('^([0-9]+)', cd): 
            ccode = plotly.colors.find_intermediate_color('rgb(255,170,156)',
                                                          'rgb(110,17,1)',
                                                           init_r, 
                                                           colortype='rgb')
            init_r = init_r + 1/no_k
        else: 
            ccode = plotly.colors.find_intermediate_color('rgb(136,207,130)',
                                                          'rgb(10,125,0)',
                                                           init_g, 
                                                           colortype='rgb')
            init_g = init_g + 1/no_e
        fig.add_trace(go.Scatter(x=plotdata[plotdata['Code'] == cd].loc[:,'Date'], 
                                 y=plotdata[plotdata['Code'] == cd].loc[:,'Amount'],
                                 #hoveron = 'points+fills',
                                 #hoverinfo = 'text+x+y',
                                 name=cd, 
                                 legendgroup=plotdata[plotdata['Code'] == cd].loc[:,'Category'].values[0],
                                 stackgroup = 'one',
                                 mode='lines',
                                 line=dict(width=0.0, color=ccode),
                                 fillcolor= ccode
                                ),
                      row=1, col=1)


    fig.add_trace(go.Pie(
                          labels = plotdata[plotdata['Date'] == pd.to_datetime('20220101',format='%Y%m%d')].groupby(by='Category')['Amount'].sum().index,
                          values = plotdata[plotdata['Date'] == pd.to_datetime('20220101',format='%Y%m%d')].groupby(by='Category')['Amount'].sum(),
                          showlegend=False,
                          hole=0.3,
                          textinfo='label+percent',
                          marker_colors = pie_colors
                        ),
                 row=1, col=3)


    fig.update_layout(
                      legend=dict(
                          orientation="h",
                          yanchor="bottom",
                          y=1.0,
                          xanchor="left",
                          x=0.01)
                       ,autosize = True
                       ,width = 1000
                      , height = 800
                      , margin=dict( l=20, r=20, b=30, t=50)
#                      , yaxis=dict(
#                          type='log'
#                        )
                     )
    return fig

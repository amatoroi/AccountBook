# -*- coding: utf-8 -*-
import dash
from dash import dcc, html, dash_table as dt
from dash.dependencies import Input, Output, State
from datetime import date, datetime

import CtrlMyDB as cmdb

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
    dcc.Markdown('''
        # 거래내역 입력
    ''')
    , dt.DataTable(
        id='tb', data = cmdb.readData().to_dict('records'),
        columns=[{'name': i, 'id': i} for i in cmdb.readData().columns],
        )
    #, cmdb.genTable(cmdb.readData(),5)
    , html.Br()

    ,html.Div([
          html.Button(children='DB에 기록', id='submit-button-state', n_clicks=0)
        , html.Br()
        , html.Div([
            dcc.Input(id='input_rel_seq', type='number', value=0,
                      style={#'margin-left':'35%',
                             'width':'450px',
                             'height':'45px',
                             'padding':'10px',
                             #'margin-top':'60px', 
                             'font-size':'16px',
                             'border-width':'3px',
                             'border-color':'#a0a3a2'
                            }
                     ),
          ])
        , dcc.DatePickerSingle(
            id='input_date'
            , initial_visible_month = date.today()
            , date = date.today()
#            , style={#'margin-left':'35%',
#                     'width':'450px',
#                     'height':'45px',
#                     'padding':'10px',
#                     #'margin-top':'60px', 
#                     'font-size':'16px',
#                     'border-width':'3px',
#                     'border-color':'#a0a3a2'
#                    }
          ), html.Br()
        , dcc.Dropdown(
            id='input_agent'
            , options = cmdb.readCodes('agent'), placeholder='거래증권사를 고르시오' #value = '001'
            , style={#'margin-left':'35%',
                     'width':'450px',
                     #'height':'45px',
                     'padding':'10px',
                     #'margin-top':'60px', 
                     'font-size':'16px',
                     'border-width':'3px',
                     'border-color':'#a0a3a2'
                    }
          ), html.Br()
        , dcc.Dropdown(
            id='input_trnsc_type'
            , options = cmdb.readCodes('trnsc_type'), placeholder='거래대상대분류'
            , style={#'margin-left':'35%',
                     'width':'450px',
                     #'height':'45px',
                     'padding':'10px',
                     #'margin-top':'60px', 
                     'font-size':'16px',
                     'border-width':'3px',
                     'border-color':'#a0a3a2'
                    }
          ), html.Br()
        , dcc.Input(
            id='input_trnsc_type_sub', placeholder='거래대상상세(한화:C010, 외화:C020, 종목코드)'
            , style={#'margin-left':'35%',
                     'width':'450px',
                     'height':'45px',
                     'padding':'10px',
                     #'margin-top':'60px', 
                     'font-size':'16px',
                     'border-width':'3px',
                     'border-color':'#a0a3a2'
                    }
          ), html.Br()
        , dcc.Dropdown(
            id='input_trnsc_type_detl'
            , options = cmdb.readCodes('trnsc_type_detl'), placeholder='거래종류'
            , style={#'margin-left':'35%',
                     'width':'450px',
                     #'height':'45px',
                     'padding':'10px',
                     #'margin-top':'60px', 
                     'font-size':'16px',
                     'border-width':'3px',
                     'border-color':'#a0a3a2'
                    }
          ), html.Br()
        , dcc.Input(id='input_trnsc_amnt', type='number', placeholder='거래금액(수량)을 입력하시오'
                  , style={#'margin-left':'35%',
                           'width':'450px',
                           'height':'45px',
                           'padding':'10px',
                           #'margin-top':'60px', 
                           'font-size':'16px',
                           'border-width':'3px',
                           'border-color':'#a0a3a2'
                          })
        , html.P(id='output-string'), html.P(id='output-err', style = {'color':'red'})
    ])
])


@app.callback(
    Output('output-err', 'children'),
    Output('output-string', 'children'),
    Input('submit-button-state','n_clicks'),
    State('input_rel_seq', 'value'),
    State('input_date', 'date'),
    State('input_agent', 'value'),
    State('input_trnsc_type', 'value'),
    State('input_trnsc_type_sub', 'value'),
    State('input_trnsc_type_detl', 'value'),
    State('input_trnsc_amnt', 'value')
    , prevent_initial_call=True
    )
def prepare_accoutbook_data(n_clck, rel_seq, i_date, agent, t_type, t_sub, t_detl, t_amnt):
    val = []
    if rel_seq == 0:
        rel_seq = 'null'
    else:
        rel_seq = rel_seq

    if i_date is not None:
        date_object = date.fromisoformat(i_date)
        date_string = date_object.strftime('%Y%m%d')
    else:
        return '날짜 입력에 오류가 있습니다.', dash.no_update

    if agent is None:
        return '거래처를 입력해주세요.', dash.no_update

    if t_type is None:
        return '거래대분류를 입력해주세요.', dash.no_update

    if t_sub is None:
        return '거래상세를 입력해주세요.', dash.no_update

    if t_detl is None:
        return '거래종류를 입력해주세요.', dash.no_update

    if t_amnt is None:
        return '거래량을 입력해주세요.', dash.no_update

    val.append(rel_seq)
    val.append(date_string)
    val.append(agent)
    val.append(t_type)
    val.append(t_sub)
    val.append(t_detl)
    val.append(t_amnt)
    print(val)
    cmdb.rcrdAccntBk(val)
    return '', ''

if __name__ == '__main__':
    app.run_server(debug=True, port=3000, host='0.0.0.0')

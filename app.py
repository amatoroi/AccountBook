# -*- coding: utf-8 -*-
import dash
from dash import dcc, html, dash_table as dt
from dash.dependencies import Input, Output, State

import MakePlotlyFig as mpf

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Markdown('''
        # 자산관리
        ## 대상기간(시작일) 입력
    '''),
    dcc.Input(id='input-date', type='text', value='20211210'),
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
    html.P(id='error', style={'color':'red'}),
    dcc.Graph(id='graphs-of-account')
])


@app.callback(
    Output('graphs-of-account', 'figure'),
    Input('submit-button-state','n_clicks'),
    State('input-date','value'))
def update_graph(n_clicks, stddate):
    fig = mpf.GetChart(stddate)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=4000, host='0.0.0.0')

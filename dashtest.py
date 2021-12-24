# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import ast


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
def serve_layout():
    df = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })
    file = open('./testdata', 'r')
    contents = file.read()
    nd = ast.literal_eval(contents)
    df['Amount'] = nd

    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

    return html.Div(children=[
        html.H1(children='Hello Dash'),
        html.Div(children='''
                        Dash: A web application framework for your data.
        '''),
        dcc.Graph(
                id='example-graph',
                figure=fig
                )
        ])

app = dash.Dash(__name__)
app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True, port=3000, host='0.0.0.0')

# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html

from plots import get_reasons_not_reported, get_reporting_trends

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

def get_layout():
    return html.Div(children=[
    html.Div(children=[
        dcc.Graph(
            id='reporting-trends',
            figure=get_reporting_trends()
        ),
        html.P(
            id='reporting-trends-label',
            children='Trend over time of whether cases reported to DDPO\'s are also reported to the police.'
        ),
    ]),

    html.Div(children=[
        dcc.Graph(
            id='reasons-not-reported',
            figure=get_reasons_not_reported()
        ),

        html.P(
            id='reasons-not-reported-label',
            children='The reasons why cases weren\'t reported to the police'
        ),
    ])

])
app.layout = get_layout

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0')

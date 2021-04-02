"""dashBoard module

-*- coding: utf-8 -*-

Run this app with `python app.py` and
visit http://127.0.0.1:8050/ in your web browser.

Copyright (c) 2021 Brian Lecarpentier
All Rights Reserved
Released under the MIT license
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import requests
import json


def get_datas_by_agent_category(agent, category, start_time=2, start_unit="d"):
    """
    Retrieve data from agent and category selected
    :param start_unit:
    :param start_time:
    :param agent:
    :param category:
    :return:
    """

    OUR_API_URL = f"http://127.0.0.1:5000/get/{category}?agent={agent}&start_time={start_time}&start_unit={start_unit}"

    response = requests.get(OUR_API_URL)
    content = json.loads(response.content.decode('utf-8'))

    if len(content) > 0:
        print(content)

        hardwareTab = []
        valuesTab = []
        time_tab = []

        for hardware in content:
            for hardware_key, value in hardware.items():
                hardwareTab.append(hardware_key)
                for time_val, value_val in value.items():
                    time_tab.append(time_val)
                    valuesTab.append(value_val)

        hardwareInfo = {
            "Time": time_tab,
            "Value": valuesTab,
            "Hardware": hardwareTab,
        }

        print(hardwareInfo)
    else:
        hardwareInfo = {
            "Time": [""],
            "Value": [0],
            "Hardware": ["PC"]
        }

    return hardwareInfo


def get_all_agents_from_api():
    """
    Get all agent in InfluxDB
    :return:
    """
    OUR_API_URL = " http://127.0.0.1:5000/get/agents"

    response = requests.get(OUR_API_URL)
    content = json.loads(response.content.decode('utf-8'))

    tab_agent = []

    for agent in content:
        tab_agent.append({'label': agent, 'value': agent})

    return tab_agent


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

df = pd.DataFrame({
    "Time": [],
    "Value": [],
    "Hardware": []
})

fig = px.line(df, x="Hardware", y="Value")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='PythonDashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='PythonDashboard for Groupe 3.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Div(
        [
            html.I("Choose start time before now in minutes / day or hours (Ex : 5 h"),
            html.Br(),
            dcc.Input(id="start", type="text", placeholder="Start Time in day / second / minutes or hours (Ex : 5)", debounce=True, size="50"),
            dcc.Input(id="end", type="text", placeholder="Time unit : d = day , h = hours , m = minutes (Ex : h)", debounce=True, size="50")
        ]
    ),

    html.Label('Agents'),
    dcc.Dropdown(
        options=get_all_agents_from_api(),
        value='',
        id='select_agent'
    ),

    html.Label('Hardware Category'),
    dcc.Dropdown(
        options=[
            {'label': 'cpu', 'value': 'cpu'},
            {'label': 'memory', 'value': 'memory'},
            {'label': 'disk', 'value': 'disk'},
            {'label': 'network', 'value': 'network'}
        ],
        value='',
        id='select_hardware'
    ),

    html.Button('Submit', id='submit-val', n_clicks=0),

    html.Div(id='container-button-basic'),

    dcc.Graph(
        id='example-graph-2',
        figure=fig
    )
])


@app.callback(
    dash.dependencies.Output('example-graph-2', 'figure'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.Input('start', 'value')],
    [dash.dependencies.Input('end', 'value')],
    [dash.dependencies.State('select_agent', 'value')],
    [dash.dependencies.State('select_hardware', 'value')])
def update_output(n_clicks, start_time, start_unit, value_agent, value_hardware):
    """
    test
    :param start_time:
    :param start_unit:
    :param value_agent:
    :param n_clicks:
    :param value_hardware:
    :return:
    """

    df = pd.DataFrame({
        "Time": [""],
        "Value": [0],
        "Hardware": ["PC"]
    })

    fig = px.line(df, x="Time", y="Value", color="Hardware", title=f"Agent : {value_agent}")

    if value_agent != "" and value_hardware != "":

        if start_time != "" and start_unit != "":
            df = pd.DataFrame(get_datas_by_agent_category(value_agent, value_hardware, start_time, start_unit))
        else:
            df = pd.DataFrame(get_datas_by_agent_category(value_agent, value_hardware))

        fig = px.line(df, x="Time", y="Value", color="Hardware")

        fig.update_layout(
            title={
                'text': f"Agent : {value_agent} - {value_hardware}",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

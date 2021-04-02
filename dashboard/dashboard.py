"""dashBoard module

Need to use pip install dash
Need to use pip install requests


Run this app with `python app.py` and
visit http://127.0.0.1:8050/ in your web browser.

-*- coding: utf-8 -*-

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
from api.api import API_URL


class DashBoard:
    """
    Dashboard class
    """
    data = {}
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    def __init__(self):
        self.colors = {'background': '#111111', 'text': '#7FDBFF'}
        self.df = pd.DataFrame(self.create_data_for_graph([], [], []))
        self.fig = px.line(self.df, x="Hardware", y="Value")
        self.fig.update_layout(
            plot_bgcolor=self.colors['background'],
            paper_bgcolor=self.colors['background'],
            font_color=self.colors['text']
        )
        self.agent_callback()
        self._create_app_layout()

    # region component generation

    def _create_app_layout(self):
        """
        Create our app layout
        """
        self.app.layout = html.Div(style={'backgroundColor': self.colors['background']}, children=[
            self._create_component_title(),

            self._create_component_subtitle(),

            self._create_component_time_chooser(),

            html.Label('Agents'),
            self._create_component_agent_chooser(),

            html.Label('Hardware Category'),
            self._create_component_category_chooser(),

            html.Button('Submit', id='submit-val', n_clicks=0),

            html.Div(id='container-button-basic'),

            dcc.Graph(
                id='example-graph-2',
                figure=self.fig
            )
        ])

    def _create_component_title(self):
        """
        Create the title of the page.
        Children is the text displayed on navigator
        """
        return html.H1(
            children='PythonDashboard',
            style={
                'textAlign': 'center',
                'color': self.colors['text']
            }
        )

    def _create_component_subtitle(self):
        """
        Create the subtitle div of the page.
        Children is the text displayed on navigator
        """
        return html.Div(
            children='PythonDashboard for Groupe 3.',
            style={
                'textAlign': 'center',
                'color': self.colors['text']
            }
        )

    def _create_component_time_chooser(self):
        """
        Create the time chooser component , with 2 text field.
        The first one for time value, the other for time unit.
        """
        return html.Div(
            [
                html.I("Choose start time before now in minutes / day or hours (Ex : 5 h"),
                html.Br(),
                dcc.Input(id="start", type="text", placeholder="Start Time in day / second / minutes or hours (Ex : 5)", debounce=True, size="50"),
                dcc.Input(id="unit", type="text", placeholder="Time unit : d = day , h = hours , m = minutes (Ex : h)", debounce=True, size="50")
            ]
        )

    def _create_component_agent_chooser(self):
        """
        Create the agent chooser chooser component, using a dropdown.
        Options should be an array of dict with 2 key : value and label
        """
        return dcc.Dropdown(
            options=self.get_all_agents_from_api(),
            value='',
            id='select_agent'
        )

    def _create_component_category_chooser(self):
        """
        Create the category chooser component.
        Options should be an array of dict with 2 key : value and label
        """
        return dcc.Dropdown(
            options=[
                {'label': 'cpu', 'value': 'cpu'},
                {'label': 'memory', 'value': 'memory'},
                {'label': 'disk', 'value': 'disk'},
                {'label': 'network', 'value': 'network'}
            ],
            value='',
            id='select_hardware'
        )

    # endregion

    def create_data_for_graph(self, time_tab, values_tab, hardware_tab):
        """
        Get a dict designed to be used in data frame to draw graphics.
        :param time_tab: a list of time (string)
        :type time_tab: list
        :param values_tab: a list of values (int)
        :type values_tab: list
        :param hardware_tab: a list of hardware key (string)
        :type hardware_tab: list
        :return: a dict containing list
        """
        return {
            "Time": time_tab,
            "Value": values_tab,
            "Hardware": hardware_tab,
        }

    def get_data_by_agent_category(self, agent, category, start_time=2, start_unit="d"):
        """
        Retrieve data from agent and category selected
        :param agent: agent number tag value
        :type agent: str
        :param category: searched data category tag
        :type category: str
        :param start_time: time value
        :type start_time: int
        :param start_unit: time unit (s, m, h, d ...)
        :type start_unit: str
        :return: a dict with 3 key : Time, Value, Hardware
        """

        our_api_url = f"{API_URL}/get/{category}?agent={agent}&start_time={start_time}&start_unit={start_unit}"
        response = requests.get(our_api_url)
        content = json.loads(response.content.decode('utf-8'))

        if len(content) > 0:
            print(content)

            hardware_tab = []
            values_tab = []
            time_tab = []

            for hardware in content:
                for hardware_key, value in hardware.items():
                    hardware_tab.append(hardware_key)
                    for time_val, value_val in value.items():
                        time_tab.append(time_val)
                        values_tab.append(value_val)

            hardware_info = self.create_data_for_graph(time_tab, values_tab, hardware_tab)
            print(hardware_info)
        else:
            hardware_info = self.create_data_for_graph([""], [0], ["PC"])

        return hardware_info

    def get_all_agents_from_api(self):
        """
        Get all agent from InfluxDB
        :return: a list of dict containing a label and value for agent
        """
        our_api_url = f"{API_URL}/get/agents"
        response = requests.get(our_api_url)
        content = json.loads(response.content.decode('utf-8'))

        tab_agent = []

        # the label is the content displayed in our dropdown, value is the value that could be used for other request
        for agent in content:
            tab_agent.append({'label': agent, 'value': agent})

        return tab_agent

    def agent_callback(self):
        """
        Launch a callback to get all agent data matching inputs values from DB
        and update graphic displayed
        """

        @self.app.callback(
            dash.dependencies.Output('example-graph-2', 'figure'),
            [dash.dependencies.Input('submit-val', 'n_clicks')],
            [dash.dependencies.Input('start', 'value')],
            [dash.dependencies.Input('unit', 'value')],
            [dash.dependencies.State('select_agent', 'value')],
            [dash.dependencies.State('select_hardware', 'value')])
        def update_output(n_clicks, start_time, start_unit, value_agent, value_hardware):
            """
            launch as a callback to get agent data and update the displayed graph
            :param start_time: start time wanted by user
            :type start_time: int
            :param start_unit: start unit wanted by user
            :type start_unit: str
            :param value_agent: agent wanted by user
            :type value_agent: str
            :param n_clicks:
            :param value_hardware: data category wanted by user
            :type value_hardware: str
            :return: an updated graphic component
            """
            if value_agent != "" and value_hardware != "":

                # if start_time and start_unit are not empty, we search with custom time value
                # else, the time values searched will be default values
                if start_time != "" and start_unit != "":
                    data_frame = pd.DataFrame(self.get_data_by_agent_category(value_agent, value_hardware, start_time, start_unit))
                else:
                    data_frame = pd.DataFrame(self.get_data_by_agent_category(value_agent, value_hardware))
                self.fig = px.line(data_frame, x="Time", y="Value", color="Hardware")

                self.fig.update_layout(
                    title={
                        'text': f"Agent : {value_agent} - {value_hardware}",
                        'y': 0.9,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    }
                )
                return self.fig
            else:
                data_frame = pd.DataFrame(self.create_data_for_graph([""], [0], ["PC"]))
                return px.line(data_frame, x="Time", y="Value", color="Hardware", title=f"Agent : {value_agent}")


if __name__ == '__main__':
    dashboard = DashBoard()
    dashboard.app.run_server(debug=True)
    #app.run_server(debug=True)

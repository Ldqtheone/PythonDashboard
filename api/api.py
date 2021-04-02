"""api module

Need to use pip install flask

-*- coding: utf-8 -*-

Copyright (c) 2021 Alyssia Prevote-Hauguel
All Rights Reserved
Released under the MIT license
"""

from flask import Flask, jsonify, request
from utils.database import Database
from utils.config.parser import *


app = Flask(__name__)
db = Database()

HOST = "127.0.0.1"
PORT = 5000

API_URL = f"http://{HOST}:{PORT}"
get_routes = {
    "get_agents": {"path": "/get/agents", "label": "recupération des agents", "example_args": ""},
    "get_data": {"path": "/get/data", "label": "recupération de données par agent et catégorie", "example_args": "?agent=PC98&category=cpu"},
    "get_all_data": {"path": "/get/all_data", "label":  "recupération de toutes les données par agent", "example_args": "?agent=PC98"},
}
for el in Interval:
    get_routes.update({f"get_{el.name}": {"path": f"/get/{el.name}", "label": f"recupération de toutes les données {el.name} par agent", "example_args": "?agent=PC98"}})


# region helpers

def is_set_and_not_empty(arg):
    """
    Check if an argument exist in the request args and if it's not empty
    :param arg: checked argument
    :type arg: str
    :return: a boolean, True if arg exist and isn't empty
    """
    return arg in request.args and request.args[arg]


def search_with_start_values(agent, category):
    """
    Used to get data from DB depending on agent and category.
    Check if are set, not empty start_time and start_unit arguments in URI.
    Also check if start_time is an int, in order to custom request for start in flux request.
    If all is good, send a custom request to influxDB.
    Else, return a default start time request to influxDb.

    :param agent: searched agent
    :type agent: str
    :param category: searched category
    :type category: str
    :return: a dict containing data from DB
    """
    if is_set_and_not_empty("start_time") and is_set_and_not_empty("start_unit"):
        # check if start_time args is an int, to make a nice request to DB.
        # Seems to be the best way to check this
        # If not, use default start_time and start_unit values
        try:
            print(int(request.args["start_time"]))
        except:
            print("time given is not an int")
            return db.get_data_by_category_query(agent, category)
        else:
            print("can use time given")
            return db.get_data_by_category_query(agent, category, int(request.args["start_time"]), str(request.args["start_unit"]))
    else:
        return db.get_data_by_category_query(agent, category)


def search_category_if_agent_exist(category):
    """
    Used to get data from DB when an agent is given (to get the good data).
    Also need a category to select each data category to return.
    :param category: searched category
    :type category: str
    :return: a json OR an error message
    """
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if is_set_and_not_empty("agent"):
        # Use the jsonify function from Flask to convert our list of
        # Python dictionaries to the JSON format.
        return jsonify(search_with_start_values(str(request.args["agent"]), category))

    else:
        return "Error: No agent field provided. Please specify an agent."


def create_home_api_url_list():
    """
    Create and return a list of link to display on a page to use api.
    It depends on the routes dict
    :return: a string containing the url list
    """
    url_list = "<ul>"
    for route in get_routes.values():
        url_list += "<li>" + create_link_from_route(route) + "</li>"
    url_list += "</ul>"
    return url_list


def create_link_from_route(route, extra_args=""):
    """
    Return a html link, with href to allow user to click on it and
    see quickly what does one of our route.
    It depends on the route dict structure
    :param route: one route element
    :type route: dict
    :param extra_args: extra arguments to add in api url
    :type extra_args: str
    :return: a string containing the html link
    """
    return f""" <a href='{API_URL}{route["path"]}{route["example_args"]}{extra_args}'>{route["label"]}</a>"""
# endregion


@app.route("/")
def home():
    """
    This route could be used to display a web page.
    Could be nice to explain how to use the API this way
    :return: a raw html structure to display on web navigator
    """
    return f"Ceci est la page principale de notre API.<br>\
            Voici une liste des requetes que vous pouvez effectuer: " + create_home_api_url_list() + f"\
            En précisant le start_time (int) et le start_unit (str), on peut modifier l'intervale de temps\
            pour lequel on recupere les données.<br> \
            exemple :<br>" + create_link_from_route(get_routes["get_cpu"], "&start_time=2&start_unit=d")


@app.route(get_routes["get_agents"]["path"], methods=["GET"])
def get_agents():
    """
    This route get all agents in DB.
    :return: a json
    """
    return jsonify(db.get_agent_query())


@app.route(get_routes["get_data"]["path"], methods=["GET"])
def get_data_by_agent_category():
    """
    This route get agent data corresponding to one category in database.
    :return: a json or an error message
    """
    if is_set_and_not_empty("agent") and is_set_and_not_empty("category"):
        return jsonify(search_with_start_values(str(request.args["agent"]), str(request.args["category"])))
    else:
        return "Error: No agent or category field provided. Please specify an agent and category."


@app.route(get_routes["get_all_data"]["path"], methods=["GET"])
def get_all_data_by_agent():
    """
    This route get all agent data in database.
    :return: a json or an error message
    """
    if is_set_and_not_empty("agent"):
        return jsonify(db.get_all_by_agent(str(request.args["agent"])))
    else:
        return "Error: No agent provided. Please specify an agent."


# region get one category

@app.route(get_routes[f"get_{Interval.cpu.name}"]["path"], methods=["GET"])
def get_cpu():
    """
    This route get all agent cpu data in database.
    :return: a json or an error message
    """
    return search_category_if_agent_exist(Interval.cpu.name)


@app.route(get_routes[f"get_{Interval.memory.name}"]["path"], methods=["GET"])
def get_memory():
    """
    This route get all agent memory data in database.
    :return: a json or an error message
    """
    return search_category_if_agent_exist(Interval.memory.name)


@app.route(get_routes[f"get_{Interval.disk.name}"]["path"], methods=["GET"])
def get_disk():
    """
    This route get all agent disk data in database.
    :return: a json or an error message
    """
    return search_category_if_agent_exist(Interval.disk.name)


@app.route(get_routes[f"get_{Interval.network.name}"]["path"], methods=["GET"])
def get_network():
    """
    This route get all agent network data in database.
    :return: a json or an error message
    """
    return search_category_if_agent_exist(Interval.network.name)


@app.route(get_routes[f"get_{Interval.sensor.name}"]["path"], methods=["GET"])
def get_sensor():
    """
    This route get all agent sensor data in database.
    :return: a json or an error message
    """
    return search_category_if_agent_exist(Interval.sensor.name)

# endregion


if __name__ == "__main__":
    app.run()


"""
Monitoring data with api
"""

from flask import Flask, jsonify, request
from Utils.database import Database
from Utils.Config.parser import *

app = Flask(__name__)
db = Database()


def search_category_if_agent_exist(category):
    """
    Used to get data from DB when an agent is given (to get the good data).
    Also need a category to select each data category to return.
    :param category: searched category
    :type category: str
    """
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'agent' in request.args:
        # Use the jsonify function from Flask to convert our list of
        # Python dictionaries to the JSON format.
        return jsonify(db.get_data_by_category_query(str(request.args['agent']), category))
    else:
        return "Error: No agent field provided. Please specify an agent."


@app.route('/')
def hello_world():
    """
    This route could be used to display a web page.
    Could be nice to explain how to use the API this way
    """
    return "Ceci est la page principale de notre API.<br>" \
           "Pour chercher des données par rapport a un agent, " \
           "utilisé par exemple: " \
           "<ul>" \
           "<li> /get/cpu?agent=PC7</li>" \
           "<li> /get/memory?agent=PC7</li>" \
           "<li> /get/disk?agent=PC7</li>" \
           "<li> /get/data?agent=PC7&category=network</li>" \
            "</ul>" \
           "Il est également possible de chercher tout les agents via l'url" \
           "/get/agents" \
           "" \
           "" \
           ""


@app.route('/get/agents')
def get_agents():
    """
    This route get all agents in DB.
    """
    return jsonify(db.get_agent_query(3))


@app.route('/get/data', methods=['GET'])
def get_data_by_agent_category():
    """
    This route get agent data corresponding to one category in database.
    """
    if 'agent' in request.args and 'category' in request.args:
        return jsonify(db.get_data_by_category_query(str(request.args['agent']), str(request.args['category'])))
    else:
        return "Error: No agent or category field provided. Please specify an agent."


@app.route('/get/cpu', methods=['GET'])
def get_cpu():
    """
    This route get all agent cpu data in database.
    """
    return search_category_if_agent_exist(Interval.cpu.name)


@app.route('/get/memory', methods=['GET'])
def get_memory():
    """
    This route get all agent memory data in database.
    """
    return search_category_if_agent_exist(Interval.memory.name)


@app.route('/get/disk', methods=['GET'])
def get_disk():
    """
    This route get all agent disk data in database.
    """
    return search_category_if_agent_exist(Interval.disk.name)


@app.route('/get/network', methods=['GET'])
def get_network():
    """
    This route get all agent network data in database.
    """
    return search_category_if_agent_exist(Interval.network.name)


@app.route('/get/sensor', methods=['GET'])
def get_sensor():
    """
    This route get all agent sensor data in database.
    """
    return search_category_if_agent_exist(Interval.sensor.name)


app.run()

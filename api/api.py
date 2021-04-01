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

        if 'start_time' in request.args and request.args['start_time'] and 'start_unit' in request.args and request.args['start_unit']:
            try:
                print(int(request.args['start_time']))
            except:
                print("time given is not an int")
            else:
                print("its all good")
                print(db.get_data_by_category_query(str(request.args['agent']), category))
                return jsonify(db.get_data_by_category_query(str(request.args['agent']), category, int(request.args['start_time']), str(request.args['start_unit'])))
        else:
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
           "<li><a href='http://127.0.0.1:5000/get/cpu?agent=PC98'>/get/cpu?agent=PC98</a></li>" \
           "<li><a href='http://127.0.0.1:5000/get/memory?agent=PC98'>/get/memory?agent=PC98</a></li>" \
           "<li><a href='http://127.0.0.1:5000/get/disk?agent=PC98&start_time=50&start_unit=m'>/get/disk?agent=PC98&start_time=50&start_unit=m</a></li>" \
           "<li><a href='http://127.0.0.1:5000/get/data?agent=PC98&category=network'>/get/data?agent=PC98&category=network</a></li>" \
            "</ul>" \
            "En précisant le start_time (int) et le start_unit (str), on peut modifier l'intervale de temps "\
            "pour lequel on recupere les données.<br>"\
           "Il est également possible de chercher tout les agents via l'url" \
           "<a href='http://127.0.0.1:5000/get/agents'>/get/agents</a>"\
           "" \
           "" \
           ""


@app.route('/get/agents')
def get_agents():
    """
    This route get all agents in DB.
    """
    return jsonify(db.get_agent_query())


@app.route('/get/data', methods=['GET'])
def get_data_by_agent_category():
    """
    This route get agent data corresponding to one category in database.
    """
    if 'agent' in request.args and 'category' in request.args:
        if 'start_time' in request.args and request.args['start_time'] and 'start_unit' in request.args and request.args['start_unit']:
            try:
                print(int(request.args['start_time']))
            except:
                print("time given is not an int")
            else:
                return jsonify(db.get_data_by_category_query(str(request.args['agent']), str(request.args['category']), int(request.args['start_time']), str(request.args['start_unit'])))
        else:
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

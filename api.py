"""
Monitoring data with api
"""

from flask import Flask, jsonify, request
from Utils.database import Database
from Utils.Config.parser import *

app = Flask(__name__)
db = Database()


@app.route('/')
def hello_world():
    return jsonify({})


@app.route('/get/agents')
def get_agents():
    return jsonify({})


@app.route('/get/cpu', methods=['GET'])
def get_cpu():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'agent' in request.args:
        agent = str(request.args['agent'])

        # Use the jsonify function from Flask to convert our list of
        # Python dictionaries to the JSON format.
        return jsonify(db.get_cpu_query(agent, Interval.cpu.name))
    else:
        return "Error: No agent field provided. Please specify an agent."


@app.route('/get/memory', methods=['GET'])
def get_memory():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'agent' in request.args:
        agent = str(request.args['agent'])

        # Use the jsonify function from Flask to convert our list of
        # Python dictionaries to the JSON format.
        return jsonify(db.get_cpu_query(agent, Interval.memory.name))
    else:
        return "Error: No agent field provided. Please specify an agent."


@app.route('/get/disk', methods=['GET'])
def get_disk():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'agent' in request.args:
        agent = str(request.args['agent'])
        print(agent)
        # Use the jsonify function from Flask to convert our list of
        # Python dictionaries to the JSON format.
        return jsonify(db.get_cpu_query(agent, Interval.disk.name))
    else:
        return "Error: No agent field provided. Please specify an agent."


@app.route('/get/network', methods=['GET'])
def get_network():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'agent' in request.args:
        agent = str(request.args['agent'])

        # Use the jsonify function from Flask to convert our list of
        # Python dictionaries to the JSON format.
        return jsonify(db.get_cpu_query(agent, Interval.network.name))
    else:
        return "Error: No agent field provided. Please specify an agent."



@app.route('/get/sensor', methods=['GET'])
def get_sensor():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'agent' in request.args:
        agent = str(request.args['agent'])

        # Use the jsonify function from Flask to convert our list of
        # Python dictionaries to the JSON format.
        return jsonify(db.get_cpu_query(agent, Interval.sensor.name))
    else:
        return "Error: No agent field provided. Please specify an agent."


app.run()

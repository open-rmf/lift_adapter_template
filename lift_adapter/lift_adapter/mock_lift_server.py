#! /usr/bin/env python3

import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/lift/status/available_floor', methods=['POST'])
def device_status():
    data = {"statusCode": 200,"isBase64Encoded": False,"headers": {"Content-Type": "application/json","Access-Control-Allow-Origin": "*"  }, "body": {"available_floor": ['l1','l2']}}
    return jsonify(data)

@app.route('/lift/status/motion_mode', methods=['POST'])
def lift_motion_mode():
    data = {"statusCode": 200,"isBase64Encoded": False,"headers": {"Content-Type": "application/json","Access-Control-Allow-Origin": "*"  }, "body": {"motion": "Up"}}
    return jsonify(data)

@app.route('/lift/status/destination', methods=['POST'])
def lift_destination():
    data = {"statusCode": 200,"isBase64Encoded": False,"headers": {"Content-Type": "application/json","Access-Control-Allow-Origin": "*"  }, "body": {"destination": "l2"}}
    return jsonify(data)

@app.route('/lift/status/current_location', methods=['POST'])
def current_floor():
    data = {"statusCode": 200,"isBase64Encoded": False,"headers": {"Content-Type": "application/json","Access-Control-Allow-Origin": "*"  }, "body": {"current_location": "l1"}}
    return jsonify(data)

@app.route('/lift/status/door_status', methods=['POST'])
def door_status():
    data = {"statusCode": 200,"isBase64Encoded": False,"headers": {"Content-Type": "application/json","Access-Control-Allow-Origin": "*"  }, "body": {"door_state": "close"}}
    return jsonify(data)

@app.route('/lift/request_floorlevel', methods=['POST'])
def request_lift_command():
    data = {"statusCode": 200,"isBase64Encoded": False,"headers": {"Content-Type": "application/json","Access-Control-Allow-Origin": "*"  }, "body": {"result":"lift request sent"}}
    return jsonify(data)

@app.route('/lift/door/remoteopen', methods=['POST'])
def lift_door_open_command():
    data = {"statusCode": 200,"isBase64Encoded": False,"headers": {"Content-Type": "application/json","Access-Control-Allow-Origin": "*"  }, "body": {"result":"lift door open command sent"}}
    return jsonify(data)

@app.route('/lift/door/remoteclose', methods=['POST'])
def lift_door_close_command():
    data = {"statusCode": 200,"isBase64Encoded": False,"headers": {"Content-Type": "application/json","Access-Control-Allow-Origin": "*"  }, "body": {"result":"lift door close command sent"}}
    return jsonify(data)

app.run(port=8888)
#!/usr/bin/python3
""" import app_views and create route to status """
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def views_route():
    """ method that returns status with json form """
    return jsonify({"status": "OK"})

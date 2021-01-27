#!/usr/bin/python3
""" import app_views and create route to status """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def views_route():
    """ method that returns status with json form """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats_route():
    """Endpoint to retrieve the number of each objects by type"""
    number_objects = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
        }
    return jsonify(number_objects)

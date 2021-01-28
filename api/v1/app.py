#!/usr/bin/python3
""" starting api """
from os import environ
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close(self):
    """Clossing session method"""
    storage.close(app, resources=r"/*")


@app.errorhandler(404)
def not_found(error):
    """handler error 404"""
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = environ.get('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)

#!/usr/bin/python3
"""New view for City object that handles all default Restfullapi actions"""
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_objs(state_id=None):
    """Return all City objects"""
    state_objs = storage.get(State, state_id)
    if state_objs:
        return jsonify([obj.to_dict() for obj in state_objs.cities])
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_by_id(city_id=None):
    """Return a city by its id"""
    city_obj = storage.get(City, city_id)
    if city_obj:
        return jsonify(city_obj.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id=None):
    """Deletes a City object"""
    city_objs = storage.get(City, city_id)
    if city_objs:
        storage.delete(city_objs)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def city_post(state_id=None):
    """Create City object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)

    state_objs = storage.get(State, state_id)
    if state_objs:
        dict_body = request.get_json()
        new_city = City(**dict_body)
        new_city.state_id = state.id
        storage.new(new_city)
        storage.save()
        return make_response(jsonify(new_city.to_dict()), 201)
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def city_put(city_id=None):
    """Update City object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    dict_body = request.get_json()
    city_obj = storage.get(City, city_id)
    if city_obj:
        for key, value in dict_body.items():
            if key != "id" and key != "created_at" and key != "updated_at":
                setattr(city_obj, key, value)
        storage.save()
        return make_response(jsonify(city_obj.to_dict()), 200)
    else:
        return abort(404)

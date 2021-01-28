#!/usr/bin/python3
"""New view for State object that handles all default Restfullapi actions"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def state_objs(state_id=None):
    """Return all States"""
    return jsonify([obj.to_dict() for obj in storage.all(State).values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_by_id(state_id=None):
    """Return state by id"""
    state_objs = storage.get(State, state_id)
    if state_objs:
        return jsonify(state_objs.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """Deletes a State object"""
    state_objs = storage.get(State, state_id)
    if state_objs:
        storage.delete(state_objs)
        storage.save()
        return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_post():
    """Create State object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    dict_body = request.get_json()
    new_state = State(**dict_body)
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_put(state_id=None):
    """Update State object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    dict_body = request.get_json()
    state_objs = storage.get(State, state_id)
    if state_objs:
        for key, value in dict_body.items():
            if key != "id" and key != "created_at" and key != "updated_at":
                setattr(state_objs, key, value)
        storage.save()
        return make_response(jsonify(state_objs.to_dict()), 200)
    else:
        return abort(404)

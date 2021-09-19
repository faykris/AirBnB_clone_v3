#!/usr/bin/python3
"""State view - module"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def states_objects():
    """Function that return a JSON dictionary"""
    state_objs = storage.all(State)
    state_list = []
    for key, value in state_objs.items():
        state_list.append(value.to_dict())
    return jsonify(state_list)


@app_views.route("/states/<string:state_id>", methods=['GET'],
                 strict_slashes=False)
def state_get(state_id=None):
    """Function that return a state object on JSON format"""
    if state_id is not None:
        state_obj = storage.get(State, state_id)
        if state_obj is not None:
            return jsonify(state_obj.to_dict())
    abort(404)


@app_views.route("/states/<string:state_id>", methods=['DELETE'],
                 strict_slashes=False)
def state_delete(state_id=None):
    """Function that return a state object on JSON format"""
    if state_id is not None:
        state_obj = storage.get(State, state_id)
        if state_obj is not None:
            storage.delete(state_obj)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def state_post():
    """Function that return a state object on JSON format"""
    state_data = request.get_json()
    if not state_data:
        return jsonify(error="Not a JSON"), 400
    state_name = state_data.get("name")
    if state_name is None:
        return jsonify(error="Missing name"), 400
    state_new = State(**state_data)
    state_new.save()
    return jsonify(state_new.to_dict()), 201


@app_views.route("/states/<string:state_id>", methods=['PUT'],
                 strict_slashes=False)
def state_put(state_id=None):
    """Update a state object and returns a JSON format"""
    state_obj = storage.get(State, state_id)
    if state_obj is not None:
        state_data = request.get_json()
        if not state_data:
            return jsonify(error="Not a JSON"), 400
        for key, value in state_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state_obj, key, value)
        state_obj.save()
        return jsonify(state_obj.to_dict())
    abort(404)

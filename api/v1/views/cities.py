#!/uar/bin/python3
"""State view - module"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State, City


@app_views.route("/states/<string:state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def cities_by_state(state_id=None):
    """Function that return a city object on JSON format"""
    if state_id is not None:
        state_obj = storage.get(State, state_id)
        if state_obj is not None:
            cities_list = []
            for key, value in storage.all(City).items():
                if state_obj.id == value.state_id:
                    cities_list.append(value.to_dict())
            return jsonify(cities_list)
    abort(404)


@app_views.route("/cities/<string:city_id>", methods=['GET'],
                 strict_slashes=False)
def city_get(city_id=None):
    """Function that return a city object on JSON format"""
    if city_id is not None:
        city_obj = storage.get(City, city_id)
        if city_obj is not None:
            return jsonify(city_obj.to_dict())
    abort(404)


@app_views.route("/cities/<string:city_id>", methods=['DELETE'],
                 strict_slashes=False)
def city_delete(city_id=None):
    """Function that remove a city object on JSON format"""
    if city_id is not None:
        city_obj = storage.get(City, city_id)
        if city_obj is not None:
            storage.delete(city_obj)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route("/states/<string:state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def city_post(state_id):
    """Function that creates and return a city object on JSON format"""
    if state_id is not None and storage.get(State, state_id) is not None:
        city_data = request.get_json()
        if not city_data:
            return jsonify(error="Not a JSON"), 400
        city_name = city_data.get("name")
        if city_name is None:
            return jsonify(error="Missing name"), 400
        city_new = City(**city_data)
        if city_new.state_id == state_id:
            city_new.save()
            return jsonify(city_new.to_dict()), 201
    abort(404)

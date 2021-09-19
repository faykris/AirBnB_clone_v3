#!/uar/bin/python3
"""index - module"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """"Function that return a status on JSON dictionary"""
    return jsonify(status="OK")


@app_views.route("/stats", strict_slashes=False)
def number_each_object():
    """"Returns the number of each objects by type"""
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})

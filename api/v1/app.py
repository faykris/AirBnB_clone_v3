#!/usr/bin/python3
"""Is the Status of your API file"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exc):
    """call reload() method for deserializing the JSON file to objects"""
    storage.close()


@app.errorhandler(404)
def invalid_route(exc):
    """handles error when the page is not found"""
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", default='0.0.0.0')
    port = getenv("HBNB_API_PORT", default=5000)

    app.run(host=host, port=port, threaded=True, debug=True)

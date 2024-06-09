#!/usr/bin/python3
""" Flask Application """
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask, render_template, make_response, jsonify

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True


@app.teardown_appcontext
def close_db(err):
    storage.close()


@app.errorhandler(404)
def not_found(err):
    return make_response(jsonify({"error": "Not found"}))


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = int(getenv("HBNB_API_PORT"))
    if not host:
        host = "0.0.0.0"
    if not port:
        port = "5000"
    app.run(host=host, port=port, threaded=True)

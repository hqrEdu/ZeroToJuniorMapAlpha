from flask import abort, jsonify
from app import app


@app.errorhandler(404)
def requested_resource_missing(error):
    return jsonify(error=str(error)), 404


@app.errorhandler(400)
def invalid_client_request(error):
    return jsonify(error=str(error)), 400


@app.errorhandler(500)
def other_server_error(error):
    return jsonify(error=str(error)), 500


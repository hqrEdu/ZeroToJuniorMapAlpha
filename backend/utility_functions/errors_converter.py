from werkzeug.exceptions import HTTPException, BadRequest, InternalServerError
import psycopg2
from flask import jsonify


def convert_to_http_exception(e):
    if isinstance(e, HTTPException):
        return e
    elif isinstance(e, ValueError):
        return jsonify(
            {
                "error": "Incorrect value"
            }
        ), 400
    elif isinstance(e, KeyError):
        return jsonify(
            {
                "error": "Missing required parameter"
            }
        ), 400
    elif isinstance(e, TypeError):
        return jsonify(
            {
                "error": "Invalid parameter type"
            }
        ), 400
    elif isinstance(e, psycopg2.errors.UniqueViolation):
        return jsonify(
            {
                "error": "Entered discord username already exists in the database"
            }
        ), 400
    elif isinstance(e, psycopg2.Error):
        return jsonify(
            {
                "error": "Database error"
            }
        ), 500
    else:
        return jsonify(
            {
                "error": "Internal Server Error'"
            }
        ), 500
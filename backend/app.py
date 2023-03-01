import os

from flask import Flask, jsonify, Response, request
from db_manager import DatabaseManager
import json

app = Flask(__name__)


# POST endpoint
@app.route('/users', methods=['POST'])
def add_user():
    response_data = {
        'success': True,
        'data': []
    }

    data = request.json
    if not data:
        response_data['success'] = False
        response_data['error'] = "Request doesn't contain any data."
        response = Response(json.dumps(response_data), mimetype='application/json')
        response.status_code = 400
    elif:
        'discord' not in data or 'city_name' not in data or 'stack' not in data:
        response_data['success'] = False
        response_data['error'] = "Please provide all required information"
        response = Response(json.dumps(response_data), mimetype='application/json')
        response.status_code = 400
    else:
        db = DatabaseManager(database=os.getenv('database'), user=os.getenv('user'), password=os.getenv('password'),
                             host=os.getenv('host'))
        db_response = db.add_user(
            request.json['discord'],
            request.json['city_name'],
            request.json['stack'],
            request.json['lat'],
            request.json['lng']
        )
        response = Response(db_response, mimetype='application/json')
        response.status_code = 201

    return response


# GET endpoint
@app.route('/users')
def get_users():
    db = DatabaseManager(database=os.getenv('database'), user=os.getenv('user'), password=os.getenv('password'),
                         host=os.getenv('host'))
    all_users = db.get_users()
    db.close_connection()
    return Response(all_users, mimetype='application/json'), 200


# PUT endpoint


# DELETE endpoint


if __name__ == '__main__':
    app.run(debug=True)

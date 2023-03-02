import os

from flask import Flask, jsonify, Response, abort, request
from db_manager import DatabaseManager
from utility_functions.geolocation import postcode_to_city, get_location_from_city

app = Flask(__name__)


# POST endpoint


# GET endpoint
@app.route('/users')
def get_users():
    db = DatabaseManager(database=os.getenv('database'),
                         user=os.getenv('user'),
                         password=os.getenv('password'),
                         host=os.getenv('host'))
    all_users = db.get_users()
    db.close_connection()
    if not all_users:
        abort(500,
              description='The server has encountered an unexpected error. Please contact the server administrator')
    return Response(all_users, mimetype='application/json'), 200


# PATCH endpoint
@app.route('/users/<string:discord>', methods=['PATCH'])
def update_users(discord):
    db = DatabaseManager(database=os.getenv('database'), user=os.getenv('user'), password=os.getenv('password'),
                         host=os.getenv('host'))
    data = request.get_json()
    updated_fields = []

    if 'new_discord' in data:
        updated_fields.append('new_discord')
        db.edit_user_name(discord, data['new_discord'])

    if 'city_name' in data:
        updated_fields.append('city_name')
        db.edit_user_city(discord, data['city_name'])

    if 'stack' in data:
        updated_fields.append('stack')
        db.edit_user_stack(discord, data['stack'])

    if len(updated_fields) > 0:
        response = jsonify({"message": f"Updated fields: {', '.join(updated_fields)}"}), 200
    else:
        response = jsonify({"error": "Invalid request."}), 400

    db.close_connection()
    return response

# DELETE endpoint
#2

if __name__ == '__main__':
    app.run(debug=True)

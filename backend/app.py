from flask import Flask, jsonify, request
from user import User
from utility_functions.errors_converter import convert_to_http_exception
import re


app = Flask(__name__)


def verify_request(data):
    if 'discord' not in data or 'zip_code' not in data or 'stack' not in data:
        raise KeyError
    elif not isinstance(data['discord'], str):
        print("Discord id must be a string type.")
        raise TypeError
    # Check if 'discord' matches the correct pattern:
    elif not re.findall("[A-Za-z].*#\d\d\d\d", data['discord']):
        raise TypeError
    elif request.json['stack'].lower() not in ["be", "fe"]:
        raise ValueError


def prepare_data(data):
    data['stack'] = data['stack'].lower()
    return data


# POST endpoint
@app.route('/users', methods=['POST'])
def add_user():
    verify_request(request.json)
    data = prepare_data(request.json)
    user = User()
    result = user.post(data['discord'], data['zip_code'], data['stack'])
    print(result)
    if result:
        return jsonify(data), 201


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


# PUT endpoint


# DELETE endpoint
#2

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, request
from user import User
from utility_functions.errors_converter import convert_to_http_exception
import re

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.errorhandler(Exception)
def handle_database_error(error):
    error = convert_to_http_exception(error)
    return error


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
@app.route('/users', methods=['GET'])
def get_users():
    user = User()
    all_users = user.get()
    return jsonify(all_users), 200


# DELETE endpoint
@app.route('/users/delete', methods=['DELETE'])
def delete_user():
    discord_id = request.form.get('discord')
    if discord_id:
        user = User()
        result = user.delete(discord=discord_id)
        return jsonify(result), 204
    else:
        raise KeyError


if __name__ == '__main__':
    app.run(debug=True)

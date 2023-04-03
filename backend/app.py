from flask import Flask, jsonify, request
from flask_cors import CORS
from user import User
from utility_functions.errors_converter import convert_to_http_exception
from utility_functions.request_data_handler import verify_POST_request, prepare_data


app = Flask(__name__)


CORS(app, resources={r"/*": {"origins": "*"}})
app.config['JSON_AS_ASCII'] = False


@app.errorhandler(Exception)
def handle_database_error(error):
    error = convert_to_http_exception(error)
    return error


# POST endpoint
@app.route('/users', methods=['POST'])
def add_user():
    verify_POST_request(request)
    data = prepare_data(request.json)
    user = User()
    result = user.post(data['discord'], data['zip_code'], data['stack'])
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

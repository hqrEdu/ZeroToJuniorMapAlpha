from flask import Flask, jsonify, request
from user import User
from utility_functions.errors_converter import convert_to_http_exception
from utility_functions.request_data_handler import verify_POST_request, prepare_data


app = Flask(__name__)


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


# PUT endpoint


# DELETE endpoint


if __name__ == '__main__':
    app.run(debug=True)

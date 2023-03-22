from flask import Flask, jsonify
from user import User
from utility_functions.errors_converter import convert_to_http_exception


app = Flask(__name__)


@app.errorhandler(Exception)
def handle_database_error(error):
    error = convert_to_http_exception(error)
    return error


# POST endpoint


# GET endpoint
@app.route('/users', methods=['GET'])
def get_users():
    user = User()
    all_users = user.get()
    if not all_users:
        raise Exception
    else:
        return jsonify(all_users), 200


# PUT endpoint


# DELETE endpoint


if __name__ == '__main__':
    app.run(debug=True)

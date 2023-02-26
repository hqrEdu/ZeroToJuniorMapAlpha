import os

from flask import Flask, jsonify, Response
from db_manager import DatabaseManager

app = Flask(__name__)


# POST endpoint


# GET endpoint
@app.route('/get-users')
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

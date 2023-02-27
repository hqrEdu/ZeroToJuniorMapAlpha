import os
from flask import Flask, jsonify, Response, request
from db_manager import DatabaseManager

app = Flask(__name__)


# 400
#

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
    return Response(all_users, mimetype='application/json'), 200


# PUT endpoint


# DELETE endpoint
@app.route('/users', methods=['DELETE'])
def delete_user():
    db = DatabaseManager(database=os.getenv('database'),
                         user=os.getenv('user'),
                         password=os.getenv('password'),
                         host=os.getenv('host'))
    try:
        discord_id = request.form.get('discord')
        result = db.delete_user(discord_id)
        return Response(result, mimetype='application/json'), 200
    except KeyError:
        return jsonify({"error": "User not found or incorrect discord id"})
    finally:
        db.close_connection()


if __name__ == '__main__':
    app.run(debug=True)

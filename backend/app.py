import os
from flask import Flask, jsonify, Response, request
from db_manager import DatabaseManager

app = Flask(__name__)


## post endpoint


## get endpoint


## put endpoint


## delete endpoint
@app.route('/users/<discord>', methods=['DELETE'])
def delete_user(discord):
    db = DatabaseManager(database=os.getenv('database'), user=os.getenv('user'), password=os.getenv('password'),
                         host=os.getenv('host'))
    try:
        result = db.delete_user(discord)
        return Response(result, mimetype='application/json'), 200
    except KeyError:
        return jsonify({"error": "User not found or incorrect discord id"})
    finally:
        db.close_connection()


if __name__ == '__main__':
    app.run(debug=True)

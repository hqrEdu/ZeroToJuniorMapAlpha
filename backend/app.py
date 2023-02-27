import os
from flask import Flask, jsonify
from db_manager import DatabaseManager

app = Flask(__name__)


## post endpoint


## get endpoint


## put endpoint


## delete enpoint
@app.route('/delete-user/<discord>', methods=['DELETE'])
def delete_user(discord):
    db = DatabaseManager(database=os.getenv('database'), user=os.getenv('user'), password=os.getenv('password'),
                         host=os.getenv('host'))
    try:
        db.delete_user(discord)
    except KeyError:
        return jsonify({"error": "User not found or incorrect user_id"})
    finally:
        db.close_connection()


if __name__ == '__main__':
    app.run()

import os
from flask import Flask, jsonify, Response, request, abort
from db_manager import DatabaseManager

app = Flask(__name__)


# POST endpoint


# GET endpoint
@app.route('/users')
def get_users():
    db = DatabaseManager(database=os.getenv('database'), user=os.getenv('user'), password=os.getenv('password'),
                         host=os.getenv('host'))
    all_users = db.get_users()
    db.close_connection()
    return Response(all_users, mimetype='application/json'), 200


# PUT endpoint


# DELETE endpoint
@app.route('/users', methods=['DELETE'])
def delete_user():
    discord_id = request.form.get('discord')
    if discord_id:  # tutaj spr czy podany id w formularzu - jak tak, to idzie dalej
        db = DatabaseManager(database=os.getenv('database'),
                             user=os.getenv('user'),
                             password=os.getenv('password'),
                             host=os.getenv('host'))
        result = db.delete_user(discord_id)
        db.close_connection()
        return Response(result, mimetype='application/json')
    else:  # tutaj wyrzuca błąd i przerywa operację, jeśli brak id
        abort(400,
              description='Invalid request. Required data missing (discord id)')


if __name__ == '__main__':
    app.run(debug=True)

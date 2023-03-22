from flask import Flask, jsonify, request
from user import User
from utility_functions.errors_converter import convert_to_http_exception

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.errorhandler(Exception)
def handle_database_error(error):
    error = convert_to_http_exception(error)
    return error


# GET endpoint
@app.route('/users', methods=['GET'])
def get_users():
    user = User()
    all_users = user.get()
    return jsonify(all_users, ), 200


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

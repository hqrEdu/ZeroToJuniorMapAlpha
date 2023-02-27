import os
from flask import Flask
from db_manager import DatabaseManager

app = Flask(__name__)


## post endpoint


## get endpoint


## put endpoint


## delete enpoint
@app.route('/delete-user/<discord>')
def delete_user(discord):
    db = DatabaseManager(database=os.getenv('database'), user=os.getenv('user'), password=os.getenv('password'),
                         host=os.getenv('host'))
    db.delete_user(discord)
    db.close_connection()


if __name__ == '__main__':
    app.run()



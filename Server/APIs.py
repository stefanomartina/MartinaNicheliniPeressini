#!flask/bin/python
from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from DbHandler import DBHandler
from datetime import datetime
import pprint

data_container = list()
data_container.append("first element")

auth = HTTPBasicAuth()
db_handler = DBHandler()

app = Flask(__name__)


@auth.get_password
def get_password(username):
    return db_handler.get_user_password(str(username))


@auth.error_handler
def unauthorized():
    return jsonify({'Response': '-1',
                    'Message': 'Username or password is incorrect'})


def get():
    return ''.join(data_container)


def post(request):
    json = request.get_json()
    if json is None:
        return jsonify({'error': 'No json data were found. Request aborted',
                        'errorCode': 400}), 400
    print(str(json)),
    data_container.append(str(json))
    return "ok"


@app.route('/')
def index():
    return "Hello, World!. This is Data4Help project by Stefano Martina, Alessandro Nichelini, Francesco Peressini"


@app.route('/api/users', methods=['GET', 'POST'])
def users_handling():
    return jsonify({"EASTEREGG": "Hello there"})


@app.route('/api/users/login', methods=['POST'])
@auth.login_required
def login():
    return jsonify({'Response': '1'})


@app.route('/api/users/data/heart', methods=['POST'])
@auth.login_required
def heart():
    try:
        data = dict(request.get_json())
        #pprint.pprint(data)

        for key in data.keys():
            bpm = int(data[key]['bpm'])
            timestamp = data[key]['timestamp']
            timestamp = timestamp[:len(timestamp)-6]
            print(timestamp)

        return jsonify({'Response': '1'})


    except Exception:
        return jsonify({'Response': '0',
                        'Reason': 'Error with heart rate data'})


@app.route('/api/users/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        first_name = data['firstname']
        last_name = data['lastname']
        birthday = '2000-10-10'
        db_handler.create_user(username, password, first_name, last_name, birthday)
        return jsonify({'Response': '1'})

    except Exception:
        return jsonify({'Response': '0',
                        'Reason': 'Creation error'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

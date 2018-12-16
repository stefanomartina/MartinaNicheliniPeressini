#!flask/bin/python
from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from DbHandler import DBHandler
from DbHandler import DuplicateException

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

#######################################################################################################################

@app.route('/')
def index():
    return "Hello, World!. This is Data4Help project by Stefano Martina, Alessandro Nichelini, Francesco Peressini"


@app.route('/api/users', methods=['GET', 'POST'])
def users_handling():
    return jsonify({"EASTER_EGG": "Hello there"})


@app.route('/api/users/login', methods=['POST'])
@auth.login_required
def login():
    return jsonify({'Response': '1'})


@app.route('/api/users/data/heart', methods=['POST'])
@auth.login_required
def heart():
    try:
        data = dict(request.get_json())

        for key in data.keys():
            bpm = data[key]['bpm']
            bpm = int(bpm[:len(bpm) - 10])
            timestamp = data[key]['timestamp']
            timestamp = timestamp[:len(timestamp) - 6]
            try:
                db_handler.insert_heart_rate(auth.username(), bpm, timestamp)
            except DuplicateException as e:
                print(str(e))
                return jsonify({'Response': '2',
                        'Reason': 'Insertion failed, duplicated tuple in HeartRate table'})

        return jsonify({'Response': 0})

    except Exception:
        return jsonify({'Response': 1,
                        'Reason': 'Error with heart rate data'})


@app.route('/api/users/data/heart/get_data', methods=['GET'])
@auth.login_required
def get_heart_rate_by_user():
    return db_handler.get_heart_rate_by_user(auth.username())


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
        return jsonify({'Response': 1})

    except Exception:
        return jsonify({'Response': 1,
                        'Reason': 'Creation error'})

#######################################################################################################################

@app.route('/api/thirdparties/subscribe', methods=['POST'])
@auth.login_required
def subscribe():
    try:
        data = request.get_json()
        FC = data['FC']
        #do something
    except Exception:
        return jsonify({'Response' : 1})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

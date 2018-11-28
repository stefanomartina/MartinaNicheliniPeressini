#!flask/bin/python
from flask import Flask, request, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from DbHandler import DBHandler

data_container = list()
data_container.append("first element")

auth = HTTPBasicAuth()
db_handler = DBHandler()

app = Flask(__name__)


@auth.get_password
def get_password(username):
    return db_handler.get_user_password(username)


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access',
                                  'errorCode': 401}), 401)


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
@auth.login_required
def users_handling():
    if request.method == 'POST':
        return post(request)
    elif request.method == 'GET':
        return get()


@app.route('/api/users/register', methods=['POST'])
def register():
    try:
        data=request.get_json()
        username=data['username']
        password=data['password']
        firstname=data['firstname']
        lastname=data['lastname']
        birthday='0'
        db_handler.create_user(username, password, firstname, lastname, birthday)
        return "ok"

    except Exception:
        return jsonify({'error': 'Request must have these fields: username, password, firstname, lastname, birthdate',
                        'errorCode': 400}), 400


if __name__ == '__main__':
    app.run(debug=True)

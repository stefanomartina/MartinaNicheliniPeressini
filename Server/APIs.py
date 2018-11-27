#!flask/bin/python
from flask import Flask, request, jsonify, make_response
from flask_httpauth import HTTPBasicAuth

data_container = list()
data_container.append("first element")

auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'Steve':
        return 'Jobs'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access',
                                  'errorCode': 401}), 401)


app = Flask(__name__)


def get():
    return ''.join(data_container)


def post(request):
    json = request.get_json()
    if json == None:
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


if __name__ == '__main__':
    app.run(debug=True)

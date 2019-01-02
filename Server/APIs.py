#!flask/bin/python
from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from DbHandler import DBHandler
from DbHandler import DuplicateException
import pprint
import sys

auth = HTTPBasicAuth()
db_handler = DBHandler()

app = Flask(__name__)

userLogged = dict()

cert = '/etc/letsencrypt/live/data4help.cloud/fullchain.pem'
key = '/etc/letsencrypt/live/data4help.cloud/privkey.pem'


@auth.get_password
def get_password(username):
    try:
        retrieved = userLogged[username]
        return retrieved
    except KeyError:
        retrieved = db_handler.get_user_password(str(username))
        if retrieved is None:
            return db_handler.get_third_party_secret(str(username))
        else:
            userLogged[username] = retrieved
            return retrieved


@auth.error_handler
def unauthorized():
    return jsonify({'Response': '1',
                    'Message': 'Username or password is incorrect'})

########################################################################################################################
# USER ENDPOINT OPERATIONS


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
        db_handler.insert_heart_rate(auth.username(), request.get_json())
        return jsonify({'Response': 0})

    except DuplicateException as e:
        print(str(e))
        return jsonify({'Response': '2', 'Reason': 'Insertion failed, duplicated tuple in HeartRate table'})

    except Exception:
        return jsonify({'Response': 1, 'Reason': 'Error with heart rate data'})


@app.route('/api/users/data/heart', methods=['GET'])
@auth.login_required
def get_heart_rate_by_user():
    return db_handler.get_heart_rate_by_user(auth.username())


@app.route('/api/users/register', methods=['POST'])
def user_register():
    try:
        data = request.get_json()
        first_name = data['firstname']
        last_name = data['lastname']
        username = data['username']
        password = data['password']
        fiscal_code = data['fiscalcode']
        gender = data['gender']
        birth_date = data['birthdate']
        birth_place = data['birthplace']
        try:
            db_handler.create_user(first_name, last_name, username, password, fiscal_code, gender,
                                   birth_date, birth_place)
        except DuplicateException as e:
            print(str(e))
            return jsonify({'Response': -1, 'Reason': str(e)})

        return jsonify({'Response': 1, 'Reason': 'Registration successful!'})

    except Exception as e:
        print(str(e))
        return jsonify({'Response': -2, 'Reason': str(e)})


@app.route('/api/users/subscription', methods=['GET'])
@auth.login_required
def user_subscription():
    return db_handler.get_subscription_to_user(auth.username())


@app.route('/api/users/subscription', methods=['PUT'])
@auth.login_required
def update_subscription_status():
    try:
        data = request.get_json()
        username = auth.username()
        third_party = data['thirdparty']
        new_status = data['new_status']

    except TypeError:
        return jsonify({"Signal": 1, "Response": "Request was not JSON Encoded"})

    signal = db_handler.modify_subscription_status(username, third_party, new_status)
    return jsonify({"Signal": signal})


@app.route('/api/users/location', methods=['POST'])
@auth.login_required
def user_location():
    try:
        data = request.get_json()
        pprint.pprint(data)
        latitude = data['latitude']
        longitude = data['longitude']
        timestamp = data['timestamp']
        try:
            db_handler.insert_latitude_longitude(auth.username(), timestamp, latitude, longitude)

        except Exception as e:
            print(str(e))
            return jsonify({'Response': -1, 'Reason': str(e)})

        return jsonify({'Response': 1, 'Reason': 'Location data correctly inserted!'})

    except Exception as e:
        print(str(e))
        return jsonify({'Response': -2, 'Reason': str(e)})


@app.route('/api/users/location', methods=['GET'])
@auth.login_required
def get_user_location():
    return db_handler.get_location_by_user(auth.username())


@app.route('/api/users/sos', methods=['POST'])
@auth.login_required
def user_sos():
    try:
        data = request.get_json()
        timestamp = data['timestamp']
        sos = data['SOS']
        try:
            db_handler.insert_sos(auth.username(), timestamp, sos)

        except Exception as e:
            print(str(e))
            return jsonify({'Response': -1, 'Reason': str(e)})

        return jsonify({'Response': 1, 'Reason': 'SOS correctly inserted in database'})

    except Exception as e:
        print(str(e))
        return jsonify({'Response': -2, 'Reason': str(e)})


#######################################################################################################################
# THIRD-PARTY ENDPOINT OPERATIONS

@app.route('/api/thirdparties/subscribe', methods=['POST'])
@auth.login_required
def subscribe():
    try:
        data = request.get_json()
        fc = data['FC']
        description = data['description']

        try:
            db_handler.subscribe_tp_to_user(auth.username(), fc, description)
        except Exception as e:
            print(str(e))
            return jsonify({'Response': -1, 'Reason': str(e)})

        return jsonify({'Response': 1, 'Reason': 'Subscription completed'})

    except Exception as e:
        print(str(e))
        return jsonify({'Response': -2, 'Reason': str(e)})


@app.route('/api/thirdparties/get_third_party', methods=['GET'])
def get_third_party():
    return db_handler.get_third_party()


@app.route('/api/thirdparties/get_third_party_secret', methods=['GET'])
def get_third_party_secret():
    username = request.args.get('username')
    try:
        result = db_handler.get_third_party_secret(username)
        return jsonify({'Response': 1, 'Reason': result})

    except Exception as e:
        print(str(e))
        return jsonify({'Response': -1, 'Reason': str(e)})


@app.route('/api/thirdparties/renew_third_party_secret', methods=['GET'])
def renew_third_party_secret():
    username = request.args.get('username')
    secret = request.args.get('secret')
    try:
        result = db_handler.check_third_party(username, secret)
        if result == 0:
            return jsonify({'Response': -1, 'Reason': 'Third-party not found'})
        else:
            try:
                db_handler.renew_third_party_secret(username)

            except Exception as e:
                print(str(e))
                return jsonify({'Response': -2, 'Reason': str(e)})

            return jsonify({'Response': 1, 'Reason': 'Secret correctly updated'})

    except Exception as e:
        print(str(e))
        return jsonify({'Response': -3, 'Reason': str(e)})


@app.route('/api/thirdparties/get_location_by_fc', methods=['GET'])
def get_location_by_fc():
    fc = request.args.get('fiscalCode')
    username = request.args.get('username')
    secret = request.args.get('secret')
    try:
        result = db_handler.check_third_party(username, secret)
        if result == 0:
            return jsonify({'Response': -1, 'Reason': 'Third-party not found'})
        else:
            try:
                return db_handler.get_location_by_fc(fc)

            except Exception as e:
                print(str(e))
                return jsonify({'Response': -2, 'Reason': str(e)})

    except Exception as e:
        print(str(e))
        return jsonify({'Response': -3, 'Reason': str(e)})


@app.route('/api/thirdparties/get_heart_rate_by_fc', methods=['GET'])
def get_heart_rate_by_fc():
    fc = request.args.get('fiscalCode')
    username = request.args.get('username')
    secret = request.args.get('secret')
    try:
        result = db_handler.check_third_party(username, secret)
        if result == 0:
            return jsonify({'Response': -1, 'Reason': 'Third-party not found'})
        else:
            try:
                return db_handler.get_heart_rate_by_fc(fc)

            except Exception as e:
                print(str(e))
                return jsonify({'Response': -2, 'Reason': str(e)})

    except Exception as e:
        print(str(e))
        return jsonify({'Response': -3, 'Reason': str(e)})


@app.route('/api/thirdparties/check_third_party', methods=['GET'])
def check_third_party():
    username = request.args.get('username')
    secret = request.args.get('secret')
    try:
        result = db_handler.check_third_party(username, secret)
        if result == 0:
            return jsonify({'Response': -1, 'Reason': 'Third-party not found'})
        else:
            return jsonify({'Response': 1, 'Reason': 'Third-party is present in the database!'})

    except Exception as e:
        print(str(e))
        return jsonify({'Response': -2, 'Reason': str(e)})


if __name__ == '__main__':
    try:
        try:
            # try to run the WebAPP with SSL certificate active
            context = (cert, key)
            app.run(host='0.0.0.0', port=5000, ssl_context=context, threaded=True, debug=True)
        except:
            # old mode without SSL certificate for debugging in localhost
            app.run(host='0.0.0.0', threaded=True, debug=True)

    except KeyboardInterrupt:
        print("[*] Server shutted down")
        db_handler.db.close()
        sys.exit(0)

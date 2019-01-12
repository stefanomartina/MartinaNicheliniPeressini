#!/usr/bin/python
import mysql.connector
import collections
import json
import pprint
import secrets
import hashlib

# parameters = {
#     'host': '35.198.157.139',
#     'user': 'root',
#     'password': 'trackme',
#     'database': 'data4help',
#     'ssl_ca': '/root/MartinaNicheliniPeressini/Server/server-ca.pem',
#     'ssl_cert': '/root/MartinaNicheliniPeressini/Server/client-cert.pem',
#     'ssl_key': '/root/MartinaNicheliniPeressini/Server/client-key.pem'
# }

parameters = {
    'host': '35.198.157.139',
    'user': 'root',
    'password': 'trackme',
    'database': 'data4help'
}


class DuplicateException(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class ConnectionPool:
    @staticmethod
    def get_new_connection():
        # return mysql.connector.connect(host='35.198.157.139', database='data4help', user='root', passwd='trackme')
        try:
            return mysql.connector.connect(**parameters)
        except:
            print('[*] WARNING: Un-secure connection')
            return mysql.connector.connect(host=parameters.get('host'), database=parameters.get('database'), user=parameters.get('user'), passwd=parameters.get('password'))


class DBHandler:
    def __init__(self, host=None, password=None):
        if(host):
            parameters['host'] = host
            parameters['password'] = password


    """
    To be called each time another method needs to write data on database
    """
    @staticmethod
    def __send(query, values):
        db = ConnectionPool.get_new_connection()
        db_cursor = db.cursor(buffered=True)
        db_cursor.execute(query, values)
        db.commit()
        db_cursor.close()
        db.close()

    """
    To be called each time another method needs to read data from database
    """
    @staticmethod
    def __get(query, values=None, multiple_lines=False):
        db = ConnectionPool.get_new_connection()
        db_cursor = db.cursor(buffered=True)
        db_cursor.execute(query, values)

        if multiple_lines:
            to_return = db_cursor.fetchall()
            db_cursor.close()
            db.close()
            return to_return
        else:
            for x in db_cursor:
                to_return = x[0]
            db_cursor.close()
            db.close()
            return to_return

    ####################################################################################################################
    # User queries

    def auth(self, username, password):
        query = "SELECT password FROM User WHERE username = %s"
        query_returned = self.__get(query, username)

        if query_returned == password:
            return True
        else:
            return False

    def get_user_password(self, username):
        query = "SELECT password FROM User WHERE username = '" + username + "'"
        return self.__get(query, None, multiple_lines=False)

    def get_subscription_to_user(self, username):
        query = "SELECT Username_ThirdParty, status FROM subscription" \
                " WHERE Username_User = '" + username + "'"

        query_returned = self.__get(query, None, multiple_lines=True)

        objects_list = []
        for row in query_returned:
            d = collections.OrderedDict()
            d['Username_ThirdParty'] = row[0]
            d['status'] = row[1]
            objects_list.append(d)
        return json.dumps(objects_list)

    def create_user(self, first_name, last_name, username, password, fiscal_code, gender, birth_date, birth_place):
        query = "INSERT INTO User (username, password, firstName, lastName, birthday, FiscalCode," \
                " birthPlace, gender) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (username, password, first_name, last_name, birth_date, fiscal_code, birth_place, gender)
        try:
            self.__send(query, values)

        except mysql.connector.IntegrityError:
            raise DuplicateException('Username is already taken!')

        except Exception as e:
            raise Exception(str(e))

    def insert_latitude_longitude(self, username, timestamp, latitude, longitude):
        query = "INSERT INTO Location VALUES (%s, %s, %s, %s)"
        timestamp = timestamp[:len(timestamp) - 6]
        values = (latitude, longitude, username, timestamp)

        try:
            self.__send(query, values)
        except Exception as e:
            raise Exception(str(e))

    def insert_heart_rate(self, username, dict_to_insert, SOS=False):
        query = "INSERT INTO HeartRate VALUES (%s, %s, %s, %s)"
        pprint.pprint(dict_to_insert)
        db = ConnectionPool.get_new_connection()
        dbCursor = db.cursor(buffered=True)

        for key in dict_to_insert.keys():
            bpm = dict_to_insert[key]['bpm']
            bpm = int(bpm[:len(bpm) - 10])
            timestamp = dict_to_insert[key]['timestamp']
            timestamp = timestamp[:len(timestamp) - 6]
            try:
                SOS = dict_to_insert[key]['sos']
            except KeyError:
                pass
            values = (username, timestamp, bpm, SOS)
            try:
                dbCursor.execute(query, values)
            except mysql.connector.IntegrityError:
                raise DuplicateException('Insertion failed, duplicated tuple in HeartRate table')

            except Exception as e:
                print(str(e))
        db.commit()
        dbCursor.close()
        db.close()

    def get_heart_rate_by_user(self, username):
        query = "SELECT HeartRate.Timestamp, BPM, SOS FROM HeartRate" \
                " WHERE Username ='" + username + "' ORDER BY Timestamp DESC"
        rows = self.__get(query, None, multiple_lines=True)

        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['timestamp'] = row[0].strftime('%Y-%m-%d %H:%M:%S')
            d['bpm'] = row[1]
            d['SOS'] = row[2]
            objects_list.append(d)

        return json.dumps(objects_list)

    def get_location_by_user(self, username):
        query = "SELECT Location.Latitude, Location.Longitude, Location.timestamp FROM Location" \
                " WHERE Username ='" + username + "' ORDER BY Timestamp DESC"

        rows = self.__get(query, None, multiple_lines=True)

        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['Latitude'] = str(row[0])
            d['Longitude'] = str(row[1])
            d['timestamp'] = row[2].strftime('%Y-%m-%d %H:%M:%S')
            objects_list.append(d)

        return json.dumps(objects_list)

    ####################################################################################################################
    # WebApp queries

    # REGISTER A NEW THIRD-PARTY IN THE DATABASE
    def register_third_party(self, email, password, company_name):
        query = "INSERT INTO ThirdParty (Username, Password, CompanyName, secret) VALUES (%s, %s, %s, %s)"
        secret = secrets.token_hex(32)
        values = (email, password, company_name, secret)
        try:
            self.__send(query, values)

        except Exception as e:
            raise Exception(str(e))

    # GET THIRD-PARTY'S PASSWORD BY ITS USERNAME
    def get_third_party_password(self, username):
        query = "SELECT password FROM ThirdParty WHERE Username = '" + username + "'"

        rows = self.__get(query, None, multiple_lines=True)
        return rows[0][0]

    # GET THIRD-PARTY'S SECRET BY ITS USERNAME
    def get_third_party_secret(self, username):
        query = "SELECT ThirdParty.secret FROM ThirdParty WHERE ThirdParty.username = '" + username + "'"

        rows = self.__get(query, None, multiple_lines=True)
        return rows[0][0]

    # RENEW THIRD-PARTY'S SECRET BY ITS USERNAME
    def renew_third_party_secret(self, username):
        new_secret = secrets.token_hex(32)
        query = "UPDATE ThirdParty SET ThirdParty.secret = '" + new_secret + "' " \
                " WHERE ThirdParty.Username = '" + username + "'"

        try:
            self.__send(query, None)

        except Exception as e:
            raise Exception(str(e))

    # CHECK IF A THIRD-PARTY IS PRESENT OR NOT IN THE DB
    def check_third_party(self, username, secret):
        query = "SELECT COUNT(*) FROM ThirdParty " \
                "WHERE ThirdParty.Username = '" + username + "' AND ThirdParty.secret = '" + secret + "'"

        rows = self.__get(query, None, multiple_lines=True)
        return rows[0][0]

    # CHECK THIRD-PARTY SUBSCRIPTION
    def check_third_party_subscription(self, tp_username, user_fc):
        query = "SELECT subscription.status FROM subscription " \
                "WHERE subscription.Username_User IN (SELECT username FROM User WHERE FiscalCode = '" + user_fc + "')" \
                "AND subscription.Username_ThirdParty = '" + tp_username + "'"

        rows = self.__get(query, None, multiple_lines=True)
        return rows[0][0]

    # GET LOCATION DATA BY THE FISCAL CODE OF THE USER
    def get_location_by_fc(self, fc):
        query = "SELECT Location.Latitude, Location.Longitude, Location.timestamp FROM Location " \
                "WHERE Username IN (SELECT username FROM User WHERE FiscalCode = '" + fc + "')" \
                "ORDER BY Location.timestamp DESC LIMIT 10"

        # ORDER BY --> FROM THE MOST RECENT TO THE LEAST RECENT
        # LIMIT X --> LIMIT THE NUMBER OF TUPLES AT X

        rows = self.__get(query, None, multiple_lines=True)

        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['Latitude'] = str(row[0])
            d['Longitude'] = str(row[1])
            d['timestamp'] = row[2].strftime('%Y-%m-%d %H:%M:%S')
            objects_list.append(d)

        return json.dumps(objects_list)

    # GET HEART RATE DATA BY THE FISCAL CODE OF THE USER
    def get_heart_rate_by_fc(self, fc):
        query = "SELECT HeartRate.BPM, HeartRate.SOS, HeartRate.Timestamp FROM HeartRate " \
                "WHERE Username IN (SELECT username FROM User WHERE FiscalCode = '" + fc + "')" \
                "ORDER BY HeartRate.Timestamp DESC LIMIT 10"

        # ORDER BY --> FROM THE MOST RECENT TO THE LEAST RECENT
        # LIMIT X --> LIMIT THE NUMBER OF TUPLES AT X

        rows = self.__get(query, None, multiple_lines=True)

        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['BPM'] = str(row[0])
            d['SOS'] = str(row[1])
            d['Timestamp'] = row[2].strftime('%Y-%m-%d %H:%M:%S')
            objects_list.append(d)

        return json.dumps(objects_list)

    def groups_heart_rate_by_birth_place(self, birth_place):
        query = "SELECT HeartRate.Username, HeartRate.BPM, HeartRate.SOS, HeartRate.Timestamp FROM HeartRate " \
                "WHERE Username IN (SELECT username FROM User WHERE birthPlace = '" + birth_place + "')" \
                "ORDER BY HeartRate.Username, HeartRate.Timestamp"

        rows = self.__get(query, None, multiple_lines=True)

        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['UserID'] = int(hashlib.sha1((str(row[0])).encode('utf-8')).hexdigest(), 16) % (10 ** 8)
            d['BPM'] = str(row[1])
            d['SOS'] = str(row[2])
            d['Timestamp'] = row[3].strftime('%Y-%m-%d %H:%M:%S')
            objects_list.append(d)

        return json.dumps(objects_list)

    def groups_heart_rate_by_year_of_birth(self, year_of_birth):
        query = "SELECT HeartRate.Username, HeartRate.BPM, HeartRate.SOS, HeartRate.Timestamp FROM HeartRate " \
                "WHERE Username IN (SELECT username FROM User WHERE YEAR(birthday) = '" + year_of_birth + "')" \
                "ORDER BY HeartRate.Username, HeartRate.Timestamp"

        rows = self.__get(query, None, multiple_lines=True)

        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['UserID'] = int(hashlib.sha1((str(row[0])).encode('utf-8')).hexdigest(), 16) % (10 ** 8)
            d['BPM'] = str(row[1])
            d['SOS'] = str(row[2])
            d['Timestamp'] = row[3].strftime('%Y-%m-%d %H:%M:%S')
            objects_list.append(d)

        return json.dumps(objects_list)

    def groups_location_by_birth_place(self, birth_place):
        query = "SELECT Location.Username, Location.Latitude, Location.Longitude, Location.timestamp FROM Location " \
                "WHERE Username IN (SELECT username FROM User WHERE birthPlace = '" + birth_place + "')" \
                "ORDER BY Location.Username, Location.timestamp"

        rows = self.__get(query, None, multiple_lines=True)

        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['UserID'] = int(hashlib.sha1((str(row[0])).encode('utf-8')).hexdigest(), 16) % (10 ** 8)
            d['Latitude'] = str(row[1])
            d['Longitude'] = str(row[2])
            d['timestamp'] = row[3].strftime('%Y-%m-%d %H:%M:%S')
            objects_list.append(d)

        return json.dumps(objects_list)

    def groups_location_by_year_of_birth(self, year_of_birth):
        query = "SELECT Location.Username, Location.Latitude, Location.Longitude, Location.timestamp FROM Location " \
                "WHERE Username IN (SELECT username FROM User WHERE YEAR(birthday) = '" + year_of_birth + "')" \
                "ORDER BY Location.Username, Location.timestamp"

        rows = self.__get(query, None, multiple_lines=True)

        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['UserID'] = int(hashlib.sha1((str(row[0])).encode('utf-8')).hexdigest(), 16) % (10 ** 8)
            d['Latitude'] = str(row[1])
            d['Longitude'] = str(row[2])
            d['timestamp'] = row[3].strftime('%Y-%m-%d %H:%M:%S')
            objects_list.append(d)

        return json.dumps(objects_list)

    def get_user_username_by_fc(self, fc):
        query = "SELECT username FROM User WHERE FiscalCode ='" + fc + "'"
        rows = self.__get(query, None, multiple_lines=True)
        return rows[0][0]

    def subscribe_tp_to_user(self, username, fc):
        query = "INSERT INTO subscription VALUES (%s, %s, %s)"
        user_username = self.get_user_username_by_fc(fc)
        values = (user_username, username, 'pending')

        try:
            self.__send(query, values)

        except Exception as e:
            print(str(e))

    def modify_subscription_status(self, username, third_party, new_status):
        query = "UPDATE subscription SET status= '" + new_status + "'" \
                " WHERE (`Username_User`= '" + username + "' and `Username_ThirdParty`= '" + third_party + "');"
        self.__send(query, None)
        return 0

    def drop_content(self):
        query_drop_content_heart_rate = "DELETE FROM HeartRate"
        self.__send(query_drop_content_heart_rate, None)

        query_drop_content_location = "DELETE FROM Location"
        self.__send(query_drop_content_location, None)

        query_drop_content_subscription = "DELETE FROM subscription"
        self.__send(query_drop_content_subscription, None)

        query_drop_content_user = "DELETE FROM User"
        self.__send(query_drop_content_user, None)

        query_drop_content_third_party = "DELETE FROM ThirdParty"
        self.__send(query_drop_content_third_party, None)







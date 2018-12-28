#!/usr/bin/python
import mysql.connector
from mysql.connector import errorcode
import collections, json, pprint


class DuplicateException(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class ConnectionPool:

    @staticmethod
    def get_new_connection():
        return mysql.connector.connect(host='35.198.157.139', database='data4help', user='root', passwd='trackme')


class DBHandler:

    @staticmethod
    def __send(query, values):
        db = ConnectionPool.get_new_connection()
        db_cursor = db.cursor(buffered=True)
        db_cursor.execute(query, values)
        db.commit()
        db_cursor.close()
        db.close()

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

    def auth(self, username, password):
        query = "SELECT password FROM User WHERE username = %s"
        query_returned = self.__get(query, (username))

        if query_returned == password:
            return True
        else:
            return False

    def get_user_password(self, username):
        query = "SELECT password FROM User WHERE username = '" + username + "'"
        return self.__get(query, None, multiple_lines=False)

    def get_tp_secret(self, username):
        query = "SELECT secret FROM ThirdParty WHERE username = '" + username + "'"
        return self.__get(query, None, multiple_lines=False)

    def get_subscription_to_user(self, username):
        query = "SELECT Username_ThirdParty, status, description FROM subscription" \
                " WHERE Username_User = '" + username + "'"

        query_returned = self.__get(query, None, multiple_lines=True)

        objects_list = []
        for row in query_returned:
            d = collections.OrderedDict()
            d['Username_ThirdParty'] = row[0]
            d['status'] = row[1]
            d['description'] = row[2]
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

    def create_tp(self, username, secret):
        query = "INSERT INTO ThirdParty VALUES (%s, %s)"
        values = (username, secret)

        try:
            self.__send(query, secret)

        except mysql.connector.errors.IntegrityError:
            raise Exception("Error")

    def insert_sos(self, username, timestamp, sos):
        timestamp = timestamp[:len(timestamp) - 6]
        query = "UPDATE HeartRate SET SOS = '" + sos + "' " \
                " WHERE (HeartRate.Username = '" + username + "' and HeartRate.Timestamp = '" + timestamp + "')"

        try:
            self.__send(query, None)

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

    def insert_heart_rate(self, username, dictToInsert):
        query = "INSERT INTO HeartRate VALUES (%s, %s, %s)"
        pprint.pprint(dictToInsert)
        db = ConnectionPool.get_new_connection()
        dbCursor = db.cursor(buffered=True)

        for key in dictToInsert.keys():
            bpm = dictToInsert[key]['bpm']
            bpm = int(bpm[:len(bpm) - 10])
            timestamp = dictToInsert[key]['timestamp']
            timestamp = timestamp[:len(timestamp) - 6]
            values = (username, timestamp, bpm)
            try:
                dbCursor.execute(query, values)
                #dbCursor.close()
            except mysql.connector.IntegrityError:
                #dbCursor.close()
                raise DuplicateException('Insertion failed, duplicated tuple in HeartRate table')

            except Exception as e:
                #dbCursor.close()
                print(str(e))
        db.commit()
        dbCursor.close()
        db.close()

    def get_heart_rate_by_user(self, username):
        query = "SELECT HeartRate.Timestamp, BPM FROM HeartRate" \
                " WHERE Username ='" + username + "' ORDER BY Timestamp DESC"
        rows = self.__get(query, None, multiple_lines=True)

        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['timestamp'] = row[0].strftime('%Y-%m-%d %H:%M:%S')
            d['bpm'] = row[1]
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

    def get_tp(self):
        query = "SELECT ThirdParty.Username, ThirdParty.secret FROM ThirdParty"

        rows = self.__get(query, None, multiple_lines=True)

        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['Username'] = str(row[0])
            d['secret'] = str(row[1])
            objects_list.append(d)

        return json.dumps(objects_list)

##    def get_location_by_fc(self, fc):
##        query = "SELECT Location.Latitude, Location.Longitude, Location.timestamp FROM Location " \
##                "WHERE Username = (SELECT username FROM User WHERE FiscalCode = '" + fc + "')"
##        rows = self.__get(query, None, multiple_lines=True)
##
##        objects_list = []
##        for row in rows:
##            d = collections.OrderedDict()
##            d['Latitude'] = str(row[0])
##            d['Longitude'] = str(row[1])
##            d['timestamp'] = row[2].strftime('%Y-%m-%d %H:%M:%S')
##           objects_list.append(d)
##
##        return json.dumps(objects_list)

    def get_user_username_by_fc(self, fc):
        query = "SELECT username FROM User WHERE FiscalCode ='" + fc + "'"
        rows = self.__get(query, None, multiple_lines=True)
        return rows[0][0]

    def subscribe_tp_to_user(self, username, fc, description):
        query = "INSERT INTO subscription VALUES (%s, %s, %s, %s)"
        user_username = self.get_user_username_by_fc(fc)
        values = (user_username, username, description, 'pending')

        try:
            self.__send(query, values)

        except Exception as e:
            print(str(e))

    def modify_subscription_status(self, username, thirdparty, new_status):
        query = "UPDATE subscription SET status= '" + new_status +"' WHERE (`Username_User`= '"+ username+ "' and `Username_ThirdParty`= '"+ thirdparty+"');"
        print(query)
        self.__send(query, None)
        return 0
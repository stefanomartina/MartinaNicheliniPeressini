#!/usr/bin/python
import mysql.connector
from mysql.connector import errorcode
import collections
import json

class DuplicateException(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class DBHandler:

    def __init__(self):
        self.db = mysql.connector.connect(host='35.198.157.139', database='data4help', user='root', passwd='trackme')
        self.dbMy = self.db.cursor()

    def auth(self, username, password):
        query = "SELECT password FROM User WHERE username = %s"

        self.dbMy.execute(query, username)

        if self.dbMy[0] == password:
            return True
        else:
            return False

    def get_user_password(self, username):
        query = "SELECT password FROM User WHERE username = '" + username + "'"
        self.dbMy.execute(query)

        for x in self.dbMy:
            if x[0] is not None:
                return x[0]
            else:
                return None

    def get_tp_secret(self, username):
        query = "SELECT secret FROM ThirdParty WHERE username = '" + username + "'"
        self.dbMy.execute(query)

        for x in self.dbMy:
            if x[0] is not None:
                return x[0]
            else:
                return None

    def get_subscription_to_user(self, username):
        query = "SELECT Username_ThirdParty, status, description FROM subscription"\
                " WHERE Username_User = '" + username + "'"

        self.dbMy.execute(query)
        rows = self.dbMy.fetchall()

        objects_list = []
        for row in rows:
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
            self.dbMy.execute(query, values)
            self.db.commit()

        except mysql.connector.IntegrityError:
            raise DuplicateException('Username is already taken!')

        except Exception as e:
            raise Exception(str(e))

    def create_tp(self, username, secret):
        query = "INSERT INTO ThirdParty VALUES (%s, %s)"
        values = (username, secret)

        try:
            self.dbMy.execute(query, values)
            self.db.commit()

        except mysql.connector.errors.IntegrityError:
            raise Exception("Error")

    def insert_heart_rate(self, username, bpm, timestamp):
        query = "INSERT INTO HeartRate VALUES (%s, %s, %s)"
        values = (username, timestamp, bpm)

        try:
            self.dbMy.execute(query, values)
            self.db.commit()

        except mysql.connector.IntegrityError:
            raise DuplicateException('Insertion failed, duplicated tuple in HeartRate table')

        except Exception as e:
            print(str(e))

    def get_heart_rate_by_user(self, username):
        query = "SELECT HeartRate.Timestamp, BPM FROM HeartRate" \
                " WHERE Username ='" + username + "' ORDER BY Timestamp ASC"

        self.dbMy.execute(query)
        rows = self.dbMy.fetchall()

        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['timestamp'] = row[0].strftime('%Y-%m-%d %H:%M:%S')
            d['bpm'] = row[1]
            objects_list.append(d)

        return json.dumps(objects_list)

    def get_user_username_by_fc(self, fc):
        query = "SELECT username FROM User WHERE FiscalCode ='" + fc + "'"
        self.dbMy.execute(query)
        rows = self.dbMy.fetchall()
        return rows[0][0]

    def subscribe_tp_to_user(self, username, fc, description):
        query = "INSERT INTO subscription VALUES (%s, %s, %s, %s)"
        user_username = self.get_user_username_by_fc(fc)
        values = (user_username, username, description, 'pending')

        try:
            self.dbMy.execute(query, values)
            self.db.commit()

        except Exception as e:
            print(str(e))

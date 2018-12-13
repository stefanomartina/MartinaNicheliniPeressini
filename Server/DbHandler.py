#!/usr/bin/python
import mysql.connector
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

    def create_user(self, username, password, first_name, last_name, birthday):
        query = "INSERT INTO User VALUES (%s, %s, %s, %s, %s)"
        values = (username, password, first_name, last_name, birthday)

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
        print(query)

        self.dbMy.execute(query)
        rows = self.dbMy.fetchmany(2)

        #str(row_array_list[row]["Timestamp"])

        row_array_list = []
        for row in rows:
            t = (row[1], row[0].strftime('%Y-%m-%d %H:%M:%S'))
            row_array_list.append(t)

        j = json.dumps(dict(row_array_list))
        return j

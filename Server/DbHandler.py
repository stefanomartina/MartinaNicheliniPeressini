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
        query = "SELECT (Timestamp, BPM) FROM HeartRate" \
                " WHERE HeartRate.Username = %s ORDER BY Timestamp ASC"

        self.dbMy.execute(query, username)
        rows = self.db.cursor.fetchall()

        row_array_list = []
        for row in rows:
            t = (row.Timestamp, row.BPM)
            row_array_list.append(t)

        j = json.dumps(row_array_list)
        return j

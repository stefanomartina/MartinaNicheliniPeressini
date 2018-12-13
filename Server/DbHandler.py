#!/usr/bin/python
import mysql.connector
import json
from flask import jsonify
import collections

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


        #for row in rows:
        #    data['timestamp'] += row[0].strftime('%Y-%m-%d %H:%M:%S')
        #    data['bpm'] += row[1]

    def get_heart_rate_by_user(self, username):
        query = "SELECT HeartRate.Timestamp, BPM FROM HeartRate" \
                    " WHERE Username ='" + username + "' ORDER BY Timestamp ASC"

        self.dbMy.execute(query)
        rows = self.dbMy.fetchmany(50)

        d = {}
        objects_list = {}
        for row in rows:
            d['bpm'] = row[1]
            d['timestamp'] = row[0].strftime('%Y-%m-%d %H:%M:%S')
            objects_list.append(d)

        return jsonify(objects_list)





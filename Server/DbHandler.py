#!/usr/bin/python
import mysql.connector


class DBHandler:

    def __init__(self):
        self.db = mysql.connector.connect(host='35.198.157.139', database='data4help', user='root', passwd='trackme')
        self.dbMy = self.db.cursor()

    def auth(self, username, password):
        query = "SELECT * FROM User WHERE username = %s"

        self.dbMy.execute(query, username)

        for x in self.dbMy:
            print(x[1])
            if x[1] == password:
                return True
            else:
                return False

    def get_user_password(self, username):
        query = "SELECT password FROM User WHERE username = %s"

        self.dbMy.execute(query, username)

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

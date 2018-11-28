#!/usr/bin/python

import mysql.connector


class DBHandler:

    def __init__(self):
        self.db = mysql.connector.connect( host = '35.198.157.139', database='data4help', user='root', passwd='trackme');
        self.dbMy = self.db.cursor()

    def auth(self, usr, psw):
        query = "SELECT * FROM User WHERE username = \"" + usr +"\" ";

        self.dbMy.execute(query)
        for x in self.dbMy:
            print(x[1])

            if x[1] == psw :
                return True
            else :
                return False

    def get_user_password(self, username):
        query = "SELECT password FROM User WHERE username = '"+username+"'";

        self.dbMy.execute(query)
        for x in self.dbMy:
            if x[0] is not None:
                return x[0]
            else:
                return None

    def create_user(self, username, password, fname, lname, birthday):
        query = "INSERT INTO User VALUES ('{}','{}','{}','{}','{}')".format(username, password, fname, lname, birthday);
        print(query)
        try:
            self.dbMy.execute(query)
            self.db.commit()
            print("DONE")
        except mysql.connector.errors.IntegrityError:
            print("ERROR")

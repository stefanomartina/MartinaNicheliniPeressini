#!/usr/bin/python

import mysql.connector


class DBHandler:

    def __init__(self):
        self.db = mysql.connector.connect(host='35.198.157.139', database='data4help', user='root', passwd='trackme')
        self.dbMy = self.db.cursor()

    def auth(self, usr, psw):
        query = "SELECT * FROM User WHERE username = \"" + usr +"\" ";

        print(query)

        self.dbMy.execute(query)

        for x in self.dbMy:
            print(x[1])

            if x[1] == psw:
                return True
            else:
                return False




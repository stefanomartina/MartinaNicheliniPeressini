#!/usr/bin/python

import mysql.connector

class DBHandler:

    def __init__(self):
        self.db = mysql.connector.connect( host = '35.198.157.139', database='data4help', user='root', passwd='trackme');
        self.dbMy = self.db.cursor()

    def auth(self, usr, psw):
        query = "SELECT * FROM User WHERE username = \"" + usr +"\" ";

        print(query)

        self.dbMy.execute(query)

        for x in self.dbMy:
            if x[1] == psw:
                return True
            else:
                return False


    def create_usr(self, usr, psw, fname, lname, birthday):
        query = "INSERT INTO User VALUES ('"+usr+"','"+ psw+"','"+lname+"','"+fname+"','"+ birthday+"')";
        print(query)


    def check_usr(self, username):
        query = "SELECT password FROM User WHERE username = \""+username+"\"";

        print(query)

        self.dbMy.execute(query)

        for x in self.dbMy:
            if x[0] != None:
                return x[0]
            else:
                return None


d = DBHandler()
#d.create_usr("pippo", "pippopsw",  "pippopsw", "pippopsw","1996-07-02")

print(d.check_usr("mario"))




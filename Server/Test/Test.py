import unittest
import mysql.connector
from DbHandler import DBHandler
import requests
import ast
import json
import datetime
import time;
from requests.auth import HTTPBasicAuth


class TestLogin(unittest.TestCase):

    dbHandler = DBHandler('127.0.0.1', 'password')


    def test_registration_DB(self):
        self.dbHandler.create_user('firstname', 'lastname', 'username', 'password', 'ABCABC12B11F111E', 'M', '2012-12-12', 'Milano')
        query_returned_check = self.dbHandler.get_user_password('username')
        self.assertEqual("password", query_returned_check)
        self.dbHandler.dropContent()

    def test_login_request_no_permission_ENDP(self):
        r = requests.get("http://localhost:5000/api/users/login")
        self.assertEqual(str(r.status_code), "405")

    def test_login_request_permission_ENDP(self):
        self.dbHandler.create_user('firstname', 'lastname', 'username', 'password', 'ABCABC12B11F111E', 'M','2012-12-12', 'Milano')
        self.dbHandler.get_user_password('username')

        r = requests.post("http://localhost:5000/api/users/login", auth=HTTPBasicAuth('username', 'password'))
        self.assertEqual(str(r.status_code), "200")
        self.dbHandler.dropContent()


    def test_registration_ENDP(self):
        #NOT WORKING string indices must be integers response
         data = {
             "firstname" : "first_name",
             "lastname": "lastname",
             "username": "username",
             "password": "password",
             "gender" : "M",
             "fiscalcode": "AAAAAAAA",
             "birthdate" : "2019-01-08",
             "birthplace" : "Milano"
         }
         r = requests.post("http://localhost:5000/api/users/register", json = data)
         print(r)

         print(r.json())

         self.dbHandler.dropContent()


    def test_location_ENDP(self):
        self.dbHandler.create_user('firstname', 'lastname', 'username', 'password', 'ABCABC12B11F111E', 'M','2012-12-12', 'Milano')

        data = {}
        data['latitude'] = '122'
        data['longitude'] = '122'
        data['timestamp'] = '2018-12-31 12:00:00'

        r_insertion = requests.post("http://localhost:5000/api/users/location", json=data, auth= HTTPBasicAuth('username', 'password'))
        self.assertEqual(str(r_insertion.status_code), "200")

        r_read = requests.get("http://localhost:5000/api/users/location", auth= HTTPBasicAuth('username', 'password'))
        self.dbHandler.dropContent()

        self.assertEqual(r_read.json()[0]["Latitude"], "122.000000")
        self.assertEqual(r_read.json()[0]["Longitude"], "122.000000")
        self.assertEqual(r_read.json()[0]["timestamp"], "2018-12-31 12:00:00")


    def test_heartrate_END(self):
        self.dbHandler.create_user('firstname', 'lastname', 'username', 'password', 'ABCABC12B11F111E', 'M','2012-12-12', 'Milano')
        data = {}
        data['bpm'] = '70'
        data['timestamp'] = '2019-12-31 12:00:00'

        r_insertion = requests.post("http://localhost:5000/api/users/data/heart", json=data, auth= HTTPBasicAuth('username', 'password'))
        self.assertEqual(str(r_insertion.status_code), "200")
        print( r_insertion.json())
        r_read = requests.get("http://localhost:5000/api/users/data/heart", auth= HTTPBasicAuth('username', 'password'))
        self.dbHandler.dropContent()
        print("-----")
        print(r_read.json())



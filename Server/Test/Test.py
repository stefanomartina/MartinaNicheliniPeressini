import unittest
import mysql.connector
from DbHandler import DBHandler
import requests
import json
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
         data = {}
         data['firstname'] = 'first_name'
         data['gender'] = 'M'
         data['fiscalcode'] = 'AAAAAAAAA'
         data['password'] = 'password'
         data['lastname'] = 'last_name'
         data['birthday'] = '2019-01-08'
         data['birthplace'] = 'Milano'


         json_data = json.dumps(data)

         r = requests.post("http://localhost:5000/api/users/register", json = json_data)
         print(r)

         print(r.json())

         self.dbHandler.dropContent()

    def test_location_ENDP(self):
        self.dbHandler.create_user('firstname', 'lastname', 'username', 'password', 'ABCABC12B11F111E', 'M','2012-12-12', 'Milano')
        self.dbHandler.get_user_password('username')
        r = requests.post("http://localhost:5000/api/users/login", auth=HTTPBasicAuth('username', 'password'))

        data = {}
        data['latitude'] = '1212'
        data['longitude'] = '1212'
        data['timestamp'] = '1212'
        json_data = json.dumps(data)

        r = requests.post("http://localhost:5000/api/users/register", json=json_data)
        self.assertEqual(str(r.status_code), "200")
        self.dbHandler.dropContent()
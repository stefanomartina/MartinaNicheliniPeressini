import unittest
import mysql.connector
from DbHandler import DBHandler
import requests
from requests.auth import HTTPBasicAuth


class TestLogin(unittest.TestCase):

    dbHandler = DBHandler('127.0.0.1', 'password')


    def test_login(self):
        self.dbHandler.create_user('firstname', 'lastname', 'username', 'password', 'ABCABC12B11F111E', 'M', '2012-12-12', 'Milano')
        query_returned_check = self.dbHandler.get_user_password('username')
        self.assertEqual("password", query_returned_check)
        self.dbHandler.dropContent()

    def test_login_request_no_permission(self):
        r = requests.get("http://localhost:5000/api/users/login")
        self.assertEqual(str(r.status_code), "405")

    def test_login_request_permission(self):
        self.dbHandler.create_user('firstname', 'lastname', 'username', 'password', 'ABCABC12B11F111E', 'M','2012-12-12', 'Milano')
        self.dbHandler.get_user_password('username')

        r = requests.post("http://localhost:5000/api/users/login", auth=HTTPBasicAuth('user', 'pass'))
        self.assertEqual(str(r.status_code), "200")
        self.dbHandler.dropContent()


import unittest
from DbHandler import DBHandler
import requests
from requests.auth import HTTPBasicAuth


class TestLogin(unittest.TestCase):
    dbHandler = DBHandler('127.0.0.1', 'password')

    def test_registration_DB(self):
        self.dbHandler.create_user('firstname', 'lastname', 'username', 'password', 'ABCABC12B11F111E', 'M',
                                   '2012-12-12', 'Milano')
        query_returned_check = self.dbHandler.get_user_password('username')
        self.assertEqual("password", query_returned_check)
        self.dbHandler.drop_content()

    def test_login_request_no_permission_ENDP(self):
        r = requests.get("http://localhost:5000/api/users/login")
        self.assertEqual(str(r.status_code), "405")

    def test_login_request_permission_ENDP(self):
        self.dbHandler.create_user('firstname', 'lastname', 'username', 'password', 'ABCABC12B11F111E', 'M',
                                   '2012-12-12', 'Milano')
        self.dbHandler.get_user_password('username')

        r = requests.post("http://localhost:5000/api/users/login", auth=HTTPBasicAuth('username', 'password'))
        self.assertEqual(str(r.status_code), "200")
        self.dbHandler.drop_content()

    def test_registration_ENDP(self):
        # NOT WORKING string indices must be integers response
        data = {
            "firstname": "first_name",
            "lastname": "lastname",
            "username": "username",
            "password": "password",
            "gender": "M",
            "fiscalcode": "AAAAAAAA",
            "birthdate": "2019-01-08",
            "birthplace": "Milano"
        }
        requests.post("http://localhost:5000/api/users/register", json=data)

        self.dbHandler.drop_content()

    def test_location_ENDP(self):
        self.dbHandler.create_user('firstname', 'lastname', 'username', 'password', 'ABCABC12B11F111E', 'M',
                                   '2012-12-12', 'Milano')

        data = {'latitude': '122', 'longitude': '122', 'timestamp': '2018-12-31 12:00:00'}

        r_insertion = requests.post("http://localhost:5000/api/users/location", json=data,
                                    auth=HTTPBasicAuth('username', 'password'))
        self.assertEqual(str(r_insertion.status_code), "200")

        r_read = requests.get("http://localhost:5000/api/users/location", auth=HTTPBasicAuth('username', 'password'))
        self.dbHandler.drop_content()

        self.assertEqual(r_read.json()[0]["Latitude"], "122.000000")
        self.assertEqual(r_read.json()[0]["Longitude"], "122.000000")
        self.assertEqual(r_read.json()[0]["timestamp"], "2018-12-31 12:00:00")

    def test_heart_rate_END(self):
        self.dbHandler.create_user('firstname', 'lastname', 'username', 'password', 'ABCABC12B11F111E', 'M',
                                   '2012-12-12', 'Milano')
        data = {'data0': {'timestamp': '2019-01-10 21:07:00 +0000', 'bpm': '90 count/min'}}

        r_insertion = requests.post("http://localhost:5000/api/users/data/heart", json=data,
                                    auth=HTTPBasicAuth('username', 'password'))
        self.assertEqual(str(r_insertion.status_code), "200")

        r_read = requests.get("http://localhost:5000/api/users/data/heart", auth=HTTPBasicAuth('username', 'password'))
        self.dbHandler.drop_content()
        self.assertEqual("2019-01-10 21:07:00", r_read.json()[0]["timestamp"])
        self.assertEqual(90, r_read.json()[0]["bpm"])

    def test_third_parties_subscription(self):
        self.dbHandler.create_user('firstname', 'lastname', 'username', 'password', 'ABCABC12B11F111E', 'M',
                                   '2012-12-12', 'Milano')

        data = {'latitude': '122', 'longitude': '122', 'timestamp': '2018-12-31 12:00:00'}

        r_insertion = requests.post("http://localhost:5000/api/users/location", json=data,
                                    auth=HTTPBasicAuth('username', 'password'))
        self.assertEqual(str(r_insertion.status_code), "200")

        self.dbHandler.register_third_party('tp_test', 'password', 'tp_test')
        secret = self.dbHandler.get_third_party_secret('tp_test')

        r_read = requests.get("http://localhost:5000/api/thirdparties/subscribe?"
                              "fiscalCode=ABCABC12B11F111E&username=tp_test&secret=" + secret + "")
        self.assertEqual(str(r_read.status_code), "200")

        r_read = r_read.json()
        self.assertEqual("Subscription completed", r_read['Reason'])
        self.assertEqual(1, r_read['Response'])

        self.dbHandler.drop_content()

    def test_third_parties_check_third_party_subscription(self):
        self.dbHandler.create_user('firstname', 'lastname', 'username', 'password', 'ABCABC12B11F111E', 'M',
                                   '2012-12-12', 'Milano')

        self.dbHandler.register_third_party('tp_test', 'password', 'tp_test')
        secret = self.dbHandler.get_third_party_secret('tp_test')
        r_read = requests.get("http://localhost:5000/api/thirdparties/subscribe?"
                              "fiscalCode=ABCABC12B11F111E&username=tp_test&secret=" + secret + "")
        self.assertEqual(str(r_read.status_code), "200")

        status = self.dbHandler.check_third_party_subscription('tp_test', 'ABCABC12B11F111E')
        self.assertEqual('pending', status)

        self.dbHandler.modify_subscription_status('username', 'tp_test', 'approved')
        status = self.dbHandler.check_third_party_subscription('tp_test', 'ABCABC12B11F111E')
        self.assertEqual('approved', status)

        self.dbHandler.modify_subscription_status('username', 'tp_test', 'rejected')
        status = self.dbHandler.check_third_party_subscription('tp_test', 'ABCABC12B11F111E')
        self.assertEqual('rejected', status)

        self.dbHandler.drop_content()

    def test_third_parties_get_location_by_fc(self):
        self.dbHandler.create_user('firstname', 'lastname', 'username', 'password', 'ABCABC12B11F111E', 'M',
                                   '2012-12-12', 'Milano')

        data = {'latitude': '122', 'longitude': '122', 'timestamp': '2018-12-31 12:00:00'}

        r_insertion = requests.post("http://localhost:5000/api/users/location", json=data,
                                    auth=HTTPBasicAuth('username', 'password'))
        self.assertEqual(str(r_insertion.status_code), "200")

        self.dbHandler.register_third_party('tp_test', 'password', 'tp_test')
        secret = self.dbHandler.get_third_party_secret('tp_test')
        r_read = requests.get("http://localhost:5000/api/thirdparties/subscribe?"
                              "fiscalCode=ABCABC12B11F111E&username=tp_test&secret=" + secret + "")
        self.assertEqual(str(r_read.status_code), "200")

        self.dbHandler.modify_subscription_status('username', 'tp_test', 'approved')

        r_read = requests.get("http://localhost:5000/api/thirdparties/get_location_by_fc?"
                              "fiscalCode=ABCABC12B11F111E&username=tp_test&secret=" + secret + "")
        self.assertEqual(str(r_read.status_code), "200")

        r_read = r_read.json()
        self.assertEqual("122.000000", r_read[0]['Latitude'])
        self.assertEqual("122.000000", r_read[0]['Longitude'])
        self.assertEqual("2018-12-31 12:00:00", r_read[0]['timestamp'])

        self.dbHandler.drop_content()

    def test_third_parties_get_heart_rate_by_fc(self):
        self.dbHandler.create_user('firstname', 'lastname', 'username', 'password', 'ABCABC12B11F111E', 'M',
                                   '2012-12-12', 'Milano')

        data = {'data0': {'timestamp': '2019-01-10 21:07:00 +0000', 'bpm': '90 count/min'}}

        r_insertion = requests.post("http://localhost:5000/api/users/data/heart", json=data,
                                    auth=HTTPBasicAuth('username', 'password'))
        self.assertEqual(str(r_insertion.status_code), "200")

        self.dbHandler.register_third_party('tp_test', 'password', 'tp_test')
        secret = self.dbHandler.get_third_party_secret('tp_test')
        r_read = requests.get("http://localhost:5000/api/thirdparties/subscribe?"
                              "fiscalCode=ABCABC12B11F111E&username=tp_test&secret=" + secret + "")
        self.assertEqual(str(r_read.status_code), "200")

        self.dbHandler.modify_subscription_status('username', 'tp_test', 'approved')

        r_read = requests.get("http://localhost:5000/api/thirdparties/get_heart_rate_by_fc?"
                              "fiscalCode=ABCABC12B11F111E&username=tp_test&secret=" + secret + "")
        self.assertEqual(str(r_read.status_code), "200")

        r_read = r_read.json()
        self.assertEqual("2019-01-10 21:07:00", r_read[0]['Timestamp'])
        self.assertEqual("90", r_read[0]['BPM'])
        self.assertEqual("0", r_read[0]['SOS'])

        self.dbHandler.drop_content()

    def test_third_parties_heart_rate_by_birth_place(self):
        self.dbHandler.create_user('firstname', 'lastname', 'username', 'password', 'ABCABC12B11F111E', 'M',
                                   '2012-12-12', 'Milano')

        data = {'data0': {'timestamp': '2019-01-10 21:07:00 +0000', 'bpm': '90 count/min'}}

        r_insertion = requests.post("http://localhost:5000/api/users/data/heart", json=data,
                                    auth=HTTPBasicAuth('username', 'password'))
        self.assertEqual(str(r_insertion.status_code), "200")

        self.dbHandler.register_third_party('tp_test', 'password', 'tp_test')
        secret = self.dbHandler.get_third_party_secret('tp_test')
        r_read = requests.get("http://localhost:5000/api/thirdparties/subscribe?"
                              "fiscalCode=ABCABC12B11F111E&username=tp_test&secret=" + secret + "")
        self.assertEqual(str(r_read.status_code), "200")

        self.dbHandler.modify_subscription_status('username', 'tp_test', 'approved')

        r_read = requests.get("http://localhost:5000/api/thirdparties/groups/heart_rate_by_birth_place?"
                              "birthPlace=Milano&username=tp_test&secret=" + secret + "")
        self.assertEqual(str(r_read.status_code), "200")

        r_read = r_read.json()
        self.assertEqual("2019-01-10 21:07:00", r_read[0]['Timestamp'])
        self.assertEqual("90", r_read[0]['BPM'])
        self.assertEqual("0", r_read[0]['SOS'])

        self.dbHandler.drop_content()

    def test_third_party_location_by_birth_place(self):
        self.dbHandler.create_user('firstname', 'lastname', 'username', 'password', 'ABCABC12B11F111E', 'M',
                                   '2012-12-12', 'Milano')

        data = {'latitude': '122', 'longitude': '122', 'timestamp': '2018-12-31 12:00:00'}

        r_insertion = requests.post("http://localhost:5000/api/users/location", json=data,
                                    auth=HTTPBasicAuth('username', 'password'))
        self.assertEqual(str(r_insertion.status_code), "200")

        self.dbHandler.register_third_party('tp_test', 'password', 'tp_test')
        secret = self.dbHandler.get_third_party_secret('tp_test')
        r_read = requests.get("http://localhost:5000/api/thirdparties/subscribe?"
                              "fiscalCode=ABCABC12B11F111E&username=tp_test&secret=" + secret + "")
        self.assertEqual(str(r_read.status_code), "200")

        self.dbHandler.modify_subscription_status('username', 'tp_test', 'approved')

        r_read = requests.get("http://localhost:5000/api/thirdparties/groups/location_by_birth_place?"
                              "birthPlace=Milano&username=tp_test&secret=" + secret + "")
        self.assertEqual(str(r_read.status_code), "200")

        r_read = r_read.json()
        self.assertEqual("122.000000", r_read[0]['Latitude'])
        self.assertEqual("122.000000", r_read[0]['Longitude'])
        self.assertEqual("2018-12-31 12:00:00", r_read[0]['timestamp'])

        self.dbHandler.drop_content()

    def test_third_party_heart_rate_by_year_of_birth(self):
        self.dbHandler.create_user('firstname', 'lastname', 'username', 'password', 'ABCABC12B11F111E', 'M',
                                   '2012-12-12', 'Milano')

        data = {'data0': {'timestamp': '2019-01-10 21:07:00 +0000', 'bpm': '90 count/min'}}

        r_insertion = requests.post("http://localhost:5000/api/users/data/heart", json=data,
                                    auth=HTTPBasicAuth('username', 'password'))
        self.assertEqual(str(r_insertion.status_code), "200")

        self.dbHandler.register_third_party('tp_test', 'password', 'tp_test')
        secret = self.dbHandler.get_third_party_secret('tp_test')
        r_read = requests.get("http://localhost:5000/api/thirdparties/subscribe?"
                              "fiscalCode=ABCABC12B11F111E&username=tp_test&secret=" + secret + "")
        self.assertEqual(str(r_read.status_code), "200")

        self.dbHandler.modify_subscription_status('username', 'tp_test', 'approved')

        r_read = requests.get("http://localhost:5000/api/thirdparties/groups/heart_rate_by_year_of_birth?"
                              "year=2012&username=tp_test&secret=" + secret + "")
        self.assertEqual(str(r_read.status_code), "200")

        r_read = r_read.json()
        self.assertEqual("2019-01-10 21:07:00", r_read[0]['Timestamp'])
        self.assertEqual("90", r_read[0]['BPM'])
        self.assertEqual("0", r_read[0]['SOS'])

        self.dbHandler.drop_content()

    def test_third_party_location_by_year_of_birth(self):
        self.dbHandler.create_user('firstname', 'lastname', 'username', 'password', 'ABCABC12B11F111E', 'M',
                                   '2012-12-12', 'Milano')

        data = {'latitude': '122', 'longitude': '122', 'timestamp': '2018-12-31 12:00:00'}

        r_insertion = requests.post("http://localhost:5000/api/users/location", json=data,
                                    auth=HTTPBasicAuth('username', 'password'))
        self.assertEqual(str(r_insertion.status_code), "200")

        self.dbHandler.register_third_party('tp_test', 'password', 'tp_test')
        secret = self.dbHandler.get_third_party_secret('tp_test')
        r_read = requests.get("http://localhost:5000/api/thirdparties/subscribe?"
                              "fiscalCode=ABCABC12B11F111E&username=tp_test&secret=" + secret + "")
        self.assertEqual(str(r_read.status_code), "200")

        self.dbHandler.modify_subscription_status('username', 'tp_test', 'approved')

        r_read = requests.get("http://localhost:5000/api/thirdparties/groups/location_by_year_of_birth?"
                              "year=2012&username=tp_test&secret=" + secret + "")
        self.assertEqual(str(r_read.status_code), "200")

        r_read = r_read.json()
        self.assertEqual("122.000000", r_read[0]['Latitude'])
        self.assertEqual("122.000000", r_read[0]['Longitude'])
        self.assertEqual("2018-12-31 12:00:00", r_read[0]['timestamp'])

        self.dbHandler.drop_content()

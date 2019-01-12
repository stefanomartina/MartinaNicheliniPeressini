import unittest
import mysql.connector
import requests
from requests.auth import HTTPBasicAuth
from DbHandler import DBHandler


def delete_db():
    my_db = mysql.connector.connect(host="127.0.0.1", user="root", passwd="password")
    my_cursor = my_db.cursor(buffered=True)
    sql_query = "DROP DATABASE `data4help`;"
    my_cursor.execute(sql_query)
    my_db.commit()
    my_cursor.close()
    my_db.close()


def create_db():
    my_db = mysql.connector.connect(host="127.0.0.1", user="root", passwd="password")
    my_cursor = my_db.cursor(buffered=True)

    query1 = "SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;"
    query2 = "SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;"
    query3 = "SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_" \
             "DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';"
    query4 = "CREATE SCHEMA IF NOT EXISTS `data4help` DEFAULT CHARACTER SET utf8 ;"
    query5 = "USE `data4help` ;"
    query6 = """CREATE TABLE IF NOT EXISTS `data4help`.`Event` (
              `idEvent` INT(11) NOT NULL AUTO_INCREMENT,
              `Name` VARCHAR(45) NULL DEFAULT NULL,
              `Description` VARCHAR(600) NULL DEFAULT NULL,
              `StartDate` DATE NULL DEFAULT NULL,
              `StartTime` DATETIME NULL DEFAULT NULL,
              `Duration` INT(11) NULL DEFAULT NULL,
              `Creator` VARCHAR(45) NULL DEFAULT NULL,
              `StartLocation_CoordX` DECIMAL(9,6) NOT NULL,
              `StartLocation_CoordY` DECIMAL(9,6) NOT NULL,
              `EndLocation_CoordX` DECIMAL(9,6) NOT NULL,
              `EndLocation_CoordY` DECIMAL(9,6) NOT NULL,
              `EndDate` DATE NULL DEFAULT NULL,
              `EndTime` DATETIME NULL DEFAULT NULL,
              PRIMARY KEY (`idEvent`),
              UNIQUE INDEX `Creator_UNIQUE` (`Creator` ASC) )
            ENGINE = InnoDB
            DEFAULT CHARACTER SET = utf8;"""
    query7 = """CREATE TABLE IF NOT EXISTS `data4help`.`User` (
              `username` VARCHAR(50) NOT NULL,
              `password` VARCHAR(50) NULL DEFAULT NULL,
              `firstName` VARCHAR(60) NULL DEFAULT NULL,
              `lastName` VARCHAR(60) NULL DEFAULT NULL,
              `birthday` DATE NULL DEFAULT NULL,
              `Event_idEvent` INT(11) NULL DEFAULT NULL,
              `FiscalCode` VARCHAR(16) NULL DEFAULT NULL,
              `birthPlace` VARCHAR(45) NULL DEFAULT NULL,
              `gender` VARCHAR(1) NULL DEFAULT NULL,
              PRIMARY KEY (`username`),
              UNIQUE INDEX `username_UNIQUE` (`username` ASC) ,
              INDEX `user_event_idx` (`Event_idEvent` ASC) ,
              CONSTRAINT `user_event`
                FOREIGN KEY (`Event_idEvent`)
                REFERENCES `data4help`.`Event` (`idEvent`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION)
            ENGINE = InnoDB
            DEFAULT CHARACTER SET = utf8;"""
    query8 = """CREATE TABLE IF NOT EXISTS `data4help`.`HeartRate` (
              `Username` VARCHAR(50) NOT NULL,
              `Timestamp` DATETIME NOT NULL,
              `BPM` INT(11) NULL DEFAULT NULL,
              `SOS` TINYINT(4) NULL DEFAULT '0',
              PRIMARY KEY (`Username`, `Timestamp`),
              CONSTRAINT `user_heartRate`
                FOREIGN KEY (`Username`)
                REFERENCES `data4help`.`User` (`username`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION)
            ENGINE = InnoDB
            DEFAULT CHARACTER SET = utf8;"""
    query9 = """CREATE TABLE IF NOT EXISTS `data4help`.`Location` (
              `Latitude` DECIMAL(9,6) NULL DEFAULT NULL,
              `Longitude` DECIMAL(9,6) NULL DEFAULT NULL,
              `Username` VARCHAR(50) NOT NULL,
              `timestamp` DATETIME NOT NULL,
              PRIMARY KEY (`timestamp`, `Username`),
              INDEX `Location_Username_idx` (`Username` ASC) ,
              CONSTRAINT `user_location`
                FOREIGN KEY (`Username`)
                REFERENCES `data4help`.`User` (`username`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION)
            ENGINE = InnoDB
            DEFAULT CHARACTER SET = utf8;"""
    query10 = """CREATE TABLE IF NOT EXISTS `data4help`.`ThirdParty` (
              `Username` VARCHAR(45) NOT NULL,
              `secret` VARCHAR(100) NULL DEFAULT NULL,
              `Address` VARCHAR(45) NULL DEFAULT NULL,
              `CompanyName` VARCHAR(45) NULL DEFAULT NULL,
              `Password` VARCHAR(45) NULL DEFAULT NULL,
              PRIMARY KEY (`Username`))
            ENGINE = InnoDB
            DEFAULT CHARACTER SET = utf8;"""
    query11 = """CREATE TABLE IF NOT EXISTS `data4help`.`subscription` (
              `Username_User` VARCHAR(50) NOT NULL,
              `Username_ThirdParty` VARCHAR(50) NOT NULL,
              `status` ENUM('approved', 'rejected', 'pending') NULL DEFAULT NULL,
              PRIMARY KEY (`Username_User`, `Username_ThirdParty`),
              INDEX `subscription_Third_idx` (`Username_ThirdParty` ASC) ,
              CONSTRAINT `subscription_Third`
                FOREIGN KEY (`Username_ThirdParty`)
                REFERENCES `data4help`.`ThirdParty` (`Username`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION,
              CONSTRAINT `subscription_User`
                FOREIGN KEY (`Username_User`)
                REFERENCES `data4help`.`User` (`username`)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION)
            ENGINE = InnoDB
            DEFAULT CHARACTER SET = utf8;"""
    query12 = "SET SQL_MODE=@OLD_SQL_MODE;"
    query13 = "SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;"
    query14 = "SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;"

    queries = [query1, query2, query3, query4, query5, query6, query7, query8, query9, query10, query11, query12,
               query13, query14]

    for query in queries:
        my_cursor.execute(query)

    my_db.commit()
    my_cursor.close()
    my_db.close()


class Test(unittest.TestCase):
    dbHandler = DBHandler('127.0.0.1', 'password')

    @classmethod
    def setUpClass(cls):
        create_db()

    @classmethod
    def tearDownClass(cls):
        delete_db()

    def setUp(self):
        self.dbHandler.drop_content()

    def test_registration_DB(self):
        self.dbHandler.create_user('firstname', 'lastname', 'username', 'password', 'ABCABC12B11F111E', 'M',
                                   '2012-12-12', 'Milano')
        query_returned_check = self.dbHandler.get_user_password('username')
        self.assertEqual("password", query_returned_check)

    def test_login_request_no_permission_ENDP(self):
        r = requests.get("http://localhost:5000/api/users/login")
        self.assertEqual(str(r.status_code), "405")

    def test_login_request_permission_ENDP(self):
        self.dbHandler.create_user('firstname', 'lastname', 'username', 'password', 'ABCABC12B11F111E', 'M',
                                   '2012-12-12', 'Milano')
        self.dbHandler.get_user_password('username')

        r = requests.post("http://localhost:5000/api/users/login", auth=HTTPBasicAuth('username', 'password'))
        self.assertEqual(str(r.status_code), "200")

    def test_registration_ENDP(self):
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

    def test_location_ENDP(self):
        self.dbHandler.create_user('firstname', 'lastname', 'username', 'password', 'ABCABC12B11F111E', 'M',
                                   '2012-12-12', 'Milano')

        data = {'latitude': '122', 'longitude': '122', 'timestamp': '2018-12-31 12:00:00'}

        r_insertion = requests.post("http://localhost:5000/api/users/location", json=data,
                                    auth=HTTPBasicAuth('username', 'password'))
        self.assertEqual(str(r_insertion.status_code), "200")

        r_read = requests.get("http://localhost:5000/api/users/location", auth=HTTPBasicAuth('username', 'password'))

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

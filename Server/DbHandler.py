#!/usr/bin/python
import mysql.connector
from mysql.connector import errorcode
import collections, json, pprint


class DuplicateException(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class DBHandler:

    def __init__(self):
        self._db = mysql.connector.connect(host='35.198.157.139', database='data4help', user='root', passwd='trackme')
        # self._dbCursor = self.db.cursor(buffered=True)

    @property
    def db(self):
        if self._db.is_connected():
            # print("Connection is open")
            return self._db
        else:
            print("Connection died")
            self._db.close()
            self._db = mysql.connector.connect(host='35.198.157.139', database='data4help', user='root', passwd='trackme')
            return self._db

    def auth(self, username, password):
        query = "SELECT password FROM User WHERE username = %s"
        dbCursor = self.db.cursor(buffered=True)
        dbCursor.execute(query, username)

        if dbCursor[0] == password:
            dbCursor.close()
            return True
        else:
            dbCursor.close()
            return False

    def get_user_password(self, username):
        query = "SELECT password FROM User WHERE username = '" + username + "'"
        dbCursor = self.db.cursor(buffered=True)
        dbCursor.execute(query)

        for x in dbCursor:
            if x[0] is not None:
                dbCursor.close()
                return x[0]
            else:
                dbCursor.close()
                return None

    def get_tp_secret(self, username):
        query = "SELECT secret FROM ThirdParty WHERE username = '" + username + "'"
        dbCursor = self.db.cursor(buffered=True)
        dbCursor.execute(query)

        for x in dbCursor:
            if x[0] is not None:
                dbCursor.close()
                return x[0]
            else:
                dbCursor.close()
                return None

    def get_subscription_to_user(self, username):
        query = "SELECT Username_ThirdParty, status, description FROM subscription"\
                " WHERE Username_User = '" + username + "'"

        dbCursor = self.db.cursor(buffered=True)
        dbCursor.execute(query)
        rows = dbCursor.fetchall()
        dbCursor.close()

        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['Username_ThirdParty'] = row[0]
            d['status'] = row[1]
            d['description'] = row[2]
            objects_list.append(d)
        return json.dumps(objects_list)

    def create_user(self, first_name, last_name, username, password, fiscal_code, gender, birth_date, birth_place):
        query = "INSERT INTO User (username, password, firstName, lastName, birthday, FiscalCode," \
                " birthPlace, gender) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (username, password, first_name, last_name, birth_date, fiscal_code, birth_place, gender)
        dbCursor = self.db.cursor(buffered=True)
        try:
            dbCursor.execute(query, values)
            self.db.commit()

        except mysql.connector.IntegrityError:
            dbCursor.close()
            raise DuplicateException('Username is already taken!')

        except Exception as e:
            dbCursor.close()
            raise Exception(str(e))

    def create_tp(self, username, secret):
        query = "INSERT INTO ThirdParty VALUES (%s, %s)"
        values = (username, secret)
        dbCursor = self.db.cursor(buffered=True)
        try:
            dbCursor.execute(query, values)
            self.db.commit()
            dbCursor.close()

        except mysql.connector.errors.IntegrityError:
            dbCursor.close()
            raise Exception("Error")

    def insert_latitude_longitude(self, username, timestamp, latitude, longitude):
        query = "INSERT INTO Location VALUES (%s, %s, %s, %s)"
        values = (latitude, longitude, username, timestamp)
        dbCursor = self.db.cursor(buffered=True)

        try:
            dbCursor.execute(query, values)
            self.db.commit()
            dbCursor.close()

        except Exception as e:
            dbCursor.close()
            raise Exception(str(e))

    def insert_heart_rate(self, username, dictToInsert):
        query = "INSERT INTO HeartRate VALUES (%s, %s, %s)"
        pprint.pprint(dictToInsert)
        dbCursor = self.db.cursor(buffered=True)

        for key in dictToInsert.keys():
            bpm = dictToInsert[key]['bpm']
            bpm = int(bpm[:len(bpm) - 10])
            timestamp = dictToInsert[key]['timestamp']
            timestamp = timestamp[:len(timestamp) - 6]
            values = (username, timestamp, bpm)
            try:
                dbCursor.execute(query, values)
                dbCursor.close()
            except mysql.connector.IntegrityError:
                dbCursor.close()
                raise DuplicateException('Insertion failed, duplicated tuple in HeartRate table')

            except Exception as e:
                dbCursor.close()
                print(str(e))
        self.db.commit()



    """def insert_heart_rate(self, username, bpm, timestamp):
        query = "INSERT INTO HeartRate VALUES (%s, %s, %s)"
        values = (username, timestamp, bpm)

        try:
            self.dbMy.execute(query, values)
            self.db.commit()

        except mysql.connector.IntegrityError:
            raise DuplicateException('Insertion failed, duplicated tuple in HeartRate table')

        except Exception as e:
            print(str(e))"""

    def get_heart_rate_by_user(self, username):
        query = "SELECT HeartRate.Timestamp, BPM FROM HeartRate" \
                " WHERE Username ='" + username + "' ORDER BY Timestamp DESC"
        dbCursor = self.db.cursor(buffered=True)
        dbCursor.execute(query)
        rows = dbCursor.fetchall()
        dbCursor.close()

        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['timestamp'] = row[0].strftime('%Y-%m-%d %H:%M:%S')
            d['bpm'] = row[1]
            objects_list.append(d)

        return json.dumps(objects_list)

    def get_user_username_by_fc(self, fc):
        query = "SELECT username FROM User WHERE FiscalCode ='" + fc + "'"
        dbCursor = self.db.cursor(buffered=True)
        dbCursor.execute(query)
        rows = dbCursor.fetchall()
        dbCursor.close()
        return rows[0][0]

    def subscribe_tp_to_user(self, username, fc, description):
        query = "INSERT INTO subscription VALUES (%s, %s, %s, %s)"
        user_username = self.get_user_username_by_fc(fc)
        values = (user_username, username, description, 'pending')
        dbCursor = self.db.cursor(buffered=True)

        try:
            dbCursor.execute(query, values)
            dbCursor.close()
            self.db.commit()

        except Exception as e:
            dbCursor.close()
            print(str(e))

    def modify_subscription_status(self, username, thirdparty, new_status):
        query = "UPDATE subscription SET status= '" + new_status +"' WHERE (`Username_User`= '"+ username+ "' and `Username_ThirdParty`= '"+ thirdparty+"');"
        print(query)
        dbCursor = self.db.cursor(buffered=True)
        dbCursor.execute(query)
        dbCursor.close()
        self.db.commit()
        return 0

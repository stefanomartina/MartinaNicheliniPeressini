import mysql.connector
import secrets

class ConnectionPool:

	@staticmethod
	def get_new_connection():
		return mysql.connector.connect(host='35.198.157.139', database='data4help', user='root', passwd='trackme')


class DBHandler:

	@staticmethod
	def __send(query, values):
		db = ConnectionPool.get_new_connection()
		db_cursor = db.cursor(buffered=True)
		db_cursor.execute(query, values)
		db.commit()
		db_cursor.close()
		db.close()

	@staticmethod
	def __get(query, values=None, multiple_lines=False):
		db = ConnectionPool.get_new_connection()
		db_cursor = db.cursor(buffered=True)
		db_cursor.execute(query, values)

		if multiple_lines:
			to_return = db_cursor.fetchall()
			db_cursor.close()
			db.close()
			return to_return
		else:
			for x in db_cursor:
				to_return = x[0]
			db_cursor.close()
			db.close()
			return to_return

	def register_third_party(self, email, password, company_name):
		query = "INSERT INTO ThirdParty (Username, Password, CompanyName, secret) VALUES (%s, %s, %s, %s)"
		secret = secrets.token_hex(32)
		values = (email, password, company_name, secret)
		try:
			self.__send(query, values)

		except Exception as e:
			raise Exception(str(e))

		except Exception as e:
			raise Exception(str(e))

	def get_third_party_password(self, username):
		query = "SELECT password FROM ThirdParty WHERE Username = '" + username + "'"
		a = self.__get(query, None, multiple_lines=False)
		print(a)
		return a
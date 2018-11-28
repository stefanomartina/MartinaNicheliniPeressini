from DbHandler import DBHandler

d = DBHandler()

print(d.create_user("ciao","ciao","ciao","ciao","1996-11-11"))

print(d.get_user_password("alenichel"))
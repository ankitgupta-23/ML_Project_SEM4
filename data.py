import sqlite3

conn = sqlite3.connect('users.db')

#conn.execute('create table users (username varchar(40), password varchar(60))')
#conn.execute('insert into users values("ankit","999111")')
#conn.execute('insert into users values("amit","777456")')
#conn.commit()
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute('select* from users')
rows = cursor.fetchall()
user  ="ankit"
pw = "999111"
conn.close()
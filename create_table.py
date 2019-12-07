import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

#Normaly there's not difference between int and INTEGER except when you create an auto increment primary key
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(create_table)



connection.commit()

connection.close()
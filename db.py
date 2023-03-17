import sqlite3
# makes the table of users with user_name,id,points and inser the beginner # users 
connection = sqlite3.connect('user_database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (user_name, id, points) VALUES (?, ?,?)",
            ('Steve Smith ', '211 ','80')
            )

cur.execute("INSERT INTO users (user_name, id, points) VALUES (?, ?,?)",
            ('Jian Wong ', '122 ','92')
            )

connection.commit()
connection.close()

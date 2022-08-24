import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (user, phnno) VALUES (?, ?)",
            ('bob', '7236198')
            )

cur.execute("INSERT INTO posts (user, phnno) VALUES (?, ?)",
            ('harry', '21378123')
            )

connection.commit()
connection.close()
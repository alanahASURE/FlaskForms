import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO surveys (name, age, email, zipcode) VALUES (?, ?, ?, ?)",
            ('Lana', 24, 'alanah10bell10@gmail.com', 85281)
            )


connection.commit()
connection.close()
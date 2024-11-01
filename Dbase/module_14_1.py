import sqlite3

connection = sqlite3.connect('not_telegram.db')

cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

# for i in range(1, 11):
#     cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
#                    (f'User{i}',
#                               f'example{i}@gmail.com',
#                               10 * i,
#                               1000), )

# for i in range(1, 10, 2):
#     cursor.execute('UPDATE Users SET balance = ? WHERE id = ?',(500, i))

# for i in range(1, 11, 3):
#     cursor.execute('DELETE FROM Users WHERE id = ?', (i,))

cursor.execute('SELECT * FROM Users WHERE age != 60')
users = cursor.fetchall()
for user in users:
    id, username, email, age, balance = user
    print(f'Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}')

connection.commit()
connection.close()

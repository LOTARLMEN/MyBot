import sqlite3


def initiate_db() -> None:
    '''
    Creates the database of products and users
    if it does not exist
    '''
    connection = sqlite3.connect('telegram_database.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )
    ''')


def get_all_products() -> list:
    '''
    Returns a list of all products
    :return:
    '''
    connection = sqlite3.connect('telegram_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    list_of_products = cursor.fetchall()
    connection.commit()
    connection.close()
    return list_of_products


def get_all_users() -> list:
    '''
    Returns a list of all users
    :return:
    '''
    connection = sqlite3.connect('telegram_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT username FROM Users')
    list_of_users = cursor.fetchall()
    connection.commit()
    connection.close()
    return list_of_users


def add_user(username: str, email: str, age: int, balance=1000) -> None:
    '''
    Adds a user to the database
    :param username:
    :param email:
    :param age:
    :param balance:
    :return:
    '''
    connection = sqlite3.connect('telegram_database.db')
    cursor = connection.cursor()
    cursor.execute(
        f'INSERT INTO Users (username, email, age, balance) VALUES (\'{username}\', \'{email}\', {age}, {balance})')
    connection.commit()
    connection.close()


def is_included(username) -> bool:
    '''
    Checks if the user is included in the database
    :param username:
    :return:
    '''
    list_of_users = get_all_users()
    for user in list_of_users:
        if username in user:
            return True
    return False

for i in get_all_users():
    print(i[0])
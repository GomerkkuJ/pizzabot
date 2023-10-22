import sqlite3
from create_bot import bot

# def sql_start():
#     global base, cur
#     base = sq.connect('pizza.db')
#     cur = base.cursor()
#     if base:
#         print('Data base connected OK')
#     base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
#     base.commit()

#
# async def sql_add_command(state):
#     async with state.proxy() as data:
#         cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
#         base.commit()
#
# async def sql_read(message):
#     for ret in cur.execute('SELECT * FROM menu').fetchall():
#         await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')
#
# async def sql_read2():
#     return cur.execute('SELECT * FROM menu').fetchall()
#
# async def sql_delete_command(data):
#     cur.execute('DELETE FROM menu WHERE name == ?', (data,))
#     base.commit()

connection = sqlite3.connect(database='data_base/pizza.dp')
sql = connection.cursor()

def sql_start():
    connection = sqlite3.connect(database='data_base/pizza.dp')
    sql = connection.cursor()
    sql.execute(
        'CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT, phone_number TEXT);')
    sql.execute('CREATE TABLE IF NOT EXISTS products (pr_name TEXT, pd_des TEXT, pr_price REAL, pr_picture TEXT);')
    sql.execute('CREATE TABLE IF NOT EXISTS cart (user_id INTEGER, product_name TEXT, product_count INTEGER);')
    sql.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    if connection:
        print('Data base connected OK')
    connection.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        print(tuple(data.values()))
        sql.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values()))
        connection.commit()

async def sql_read(message):
    for ret in sql.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')

async def sql_read2():
    return sql.execute('SELECT * FROM menu').fetchall()

async def sql_delete_command(data):
    sql.execute('DELETE FROM menu WHERE name == ?', (data,))
    connection.commit()

def add_user(user_id, name, phone_number):
    connection = sqlite3.connect(database='data_base/pizza.dp')
    sql = connection.cursor()
    sql.execute('INSERT INTO users VALUES (?, ?, ?);', (user_id, name, phone_number))
    connection.commit()

def get_users():
    connection = sqlite3.connect(database='data_base/pizza.dp')
    sql = connection.cursor()

    users = sql.execute('SELECT name, id FROM users;')
    return users.fetchall()

def delete_user():
    connection = sqlite3.connect(database='data_base/pizza.dp')
    sql = connection.cursor()
    sql.execute('DELETE FROM users;')
    connection.commit()


def add_product(pr_name, pr_des, pr_price, pr_pictrure):
    connection = sqlite3.connect(database='data_base/pizza.dp')
    sql = connection.cursor()

    sql.execute('INSERT INTO products VALUES (?, ?, ?, ?);', (pr_name, pr_des, pr_price, pr_pictrure))
    connection.commit()

def get_all_info_product(current_product):
    connection = sqlite3.connect(database='data_base/pizza.dp')
    sql = connection.cursor()

    all_products = sql.execute('SELECT * FROM products WHERE pr_name=?;', (current_product, ))

    return all_products.fetchone()

# Функция для получения наименования продукта
# def get_name_product():
#     connection = sqlite3.connect(database='data_base/pizza.dp')
#     sql = connection.cursor()
#
#     products_name = sql.execute('SELECT pr_name FROM products;')
#     return products_name.fetchall()


def get_names_from_menu():
    connection = sqlite3.connect(database='data_base/pizza.dp')
    sql = connection.cursor()

    products_name = sql.execute('SELECT name FROM menu;')
    return products_name.fetchall()

def check_user(user_id):
    connection = sqlite3.connect(database='data_base/pizza.dp')
    sql = connection.cursor()

    checker = sql.execute('SELECT id FROM users WHERE id=?;', (user_id,))
    return checker.fetchone()

def add_product_to_cart(user_id, product_name, product_count):
    connection = sqlite3.connect(database='data_base/pizza.dp')
    sql = connection.cursor()
    sql.execute('INSERT INTO cart VALUES (?, ?, ?);', (user_id, product_name, product_count))
    connection.commit()

def get_user_cart(user_id):
    connection = sqlite3.connect(database='data_base/pizza.dp')
    sql = connection.cursor()
    all_products_from_cart = sql.execute('SELECT * FROM cart WHERE user_id=?;', (user_id,))

    return all_products_from_cart.fetchall()



def delete_from_cart(user_id):
    connection = sqlite3.connect(database='data_base/pizza.dp')
    sql = connection.cursor()
    sql.execute('DELETE FROM cart WHERE user_id=?;', (user_id,))
    connection.commit()


# def get_product(name: str):
#     connection = sqlite3.connect(database='data_base/pizza.dp')
#     sql = connection.cursor()
#     product = sql.execute('SELECT pr_picture, pr_name, pd_des, pr_price FROM products WHERE pr_name = ?;', (name,))
#     return product.fetchone()


def get_product_from_menu(name: str):
    connection = sqlite3.connect(database='data_base/pizza.dp')
    sql = connection.cursor()
    product = sql.execute('SELECT img, name, description, price FROM menu WHERE name = ?;', (name,))
    return product.fetchone()

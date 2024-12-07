import sqlite3


def initiate_db():
    connection = sqlite3.connect("not_telegram.db")
    cursor = connection.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL
        )
        '''
    )
    connection.commit()
    connection.close()


# for i in range(1, 5):
#     cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
#                    (f'Product {i}', f'Description {i}', i * 100))


def get_all_products():
    connection = sqlite3.connect("not_telegram.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    connection.close()
    return products

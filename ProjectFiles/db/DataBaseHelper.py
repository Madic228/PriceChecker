import sqlite3


class DataBaseHelper:

    @staticmethod
    def get_connection(db_name="PriceCheckerDB.db"):
        return sqlite3.connect(db_name)

    @classmethod
    def create_tables(cls):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Users (
                    user_id INTEGER PRIMARY KEY,
                    username VARCHAR
                );
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Products (
                    product_id INTEGER PRIMARY KEY,
                    product_name VARCHAR,
                    product_url VARCHAR,
                    product_image_url VARCHAR,
                    current_price DECIMAL
                );
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS TrackedProducts (
                    tracked_id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    product_id INTEGER,
                    tracking_date DATE,
                    FOREIGN KEY (user_id) REFERENCES Users (user_id),
                    FOREIGN KEY (product_id) REFERENCES Products (product_id)
                );
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS PriceHistory (
                    price_history_id INTEGER PRIMARY KEY,
                    product_id INTEGER,
                    date_recorded DATE,
                    price DECIMAL,
                    FOREIGN KEY (product_id) REFERENCES Products (product_id)
                );
            ''')
            conn.commit()

    @classmethod
    def add_user(cls, username):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Users (username) VALUES (?)", (username,))
            conn.commit()

    @classmethod
    def add_product(cls, product_name, product_url, product_image_url, current_price):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Products (product_name, product_url, product_image_url, current_price) VALUES (?, ?, ?, ?)",
                (product_name, product_url, product_image_url, current_price))
            conn.commit()

    @classmethod
    def track_product(cls, user_id, product_id, tracking_date):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO TrackedProducts (user_id, product_id, tracking_date) VALUES (?, ?, ?)",
                           (user_id, product_id, tracking_date))
            conn.commit()

    @classmethod
    def update_price(cls, product_id, new_price):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE Products SET current_price = ? WHERE product_id = ?", (new_price, product_id))
            conn.commit()

# Пример использования
# DataBaseHelper.create_tables()
# DataBaseHelper.add_user('JohnDoe')
# Далее можно использовать другие функции для добавления товаров и т.д.

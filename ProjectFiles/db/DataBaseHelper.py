import sqlite3
from datetime import datetime


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
                        telegram_id INTEGER PRIMARY KEY,
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
                        telegram_id INTEGER,
                        product_id INTEGER,
                        tracking_date DATE,
                        FOREIGN KEY (telegram_id) REFERENCES Users (telegram_id),
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
    def add_user(cls, telegram_id, username):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Users (telegram_id, username) VALUES (?, ?)", (telegram_id, username))
            conn.commit()

    @classmethod
    def user_exists(cls, telegram_id):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE telegram_id = ?", (telegram_id,))
            return cursor.fetchone() is not None

    @classmethod
    def add_product(cls, product_name, product_url, product_image_url, current_price):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Products (product_name, product_url, product_image_url, current_price) VALUES (?, ?, ?, ?)",
                (product_name, product_url, product_image_url, current_price))
            conn.commit()

    @classmethod
    def product_exists(cls, product_name, product_url):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Products WHERE product_name = ? OR product_url = ?",
                           (product_name, product_url))
            return cursor.fetchone() is not None

    @classmethod
    def track_product(cls, telegram_id, product_id, tracking_date):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO TrackedProducts (telegram_id, product_id, tracking_date) VALUES (?, ?, ?)",
                           (telegram_id, product_id, tracking_date))
            conn.commit()

    @classmethod
    def update_price(cls, product_id, new_price):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE Products SET current_price = ? WHERE product_id = ?", (new_price, product_id))
            conn.commit()

    @classmethod
    def get_current_price(cls, product_url):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT current_price FROM Products WHERE product_url = ?", (product_url,))
            result = cursor.fetchone()
            return result[0] if result else None

    @classmethod
    def update_price(cls, product_url, new_price):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE Products SET current_price = ? WHERE product_url = ?", (new_price, product_url))
            conn.commit()

    @classmethod
    def add_price_history(cls, product_url, price):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT product_id FROM Products WHERE product_url = ?", (product_url,))
            product_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO PriceHistory (product_id, date_recorded, price) VALUES (?, ?, ?)",
                           (product_id, datetime.now().date(), price))
            conn.commit()

    @classmethod
    def get_user_id(cls, telegram_id):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM Users WHERE username = ?", (telegram_id,))
            result = cursor.fetchone()
            return result[0] if result is not None else None

    @classmethod
    def get_tracked_products(cls, telegram_id):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                    SELECT p.product_id, p.product_name, p.product_url
                    FROM TrackedProducts t
                    JOIN Products p ON t.product_id = p.product_id
                    WHERE t.telegram_id = ?
                """, (telegram_id,))
            return [{'product_id': row[0], 'name': row[1], 'url': row[2]} for row in cursor.fetchall()]

    @classmethod
    def delete_tracked_products(cls, telegram_id):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM TrackedProducts WHERE telegram_id = ?", (telegram_id,))
            conn.commit()

    @classmethod
    def get_product_id(cls, product_url):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT product_id FROM Products WHERE product_url = ?", (product_url,))
            result = cursor.fetchone()
            return result[0] if result else None

    @classmethod
    def get_product_info(cls, product_id):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                   SELECT product_name, product_url, product_image_url, current_price
                   FROM Products
                   WHERE product_id = ?
               """, (product_id,))
            row = cursor.fetchone()
            return {
                'name': row[0],
                'url': row[1],
                'image_url': row[2],
                'price': row[3]
            } if row else None

    @classmethod
    def get_price_change_info(cls, product_id):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                   SELECT ph.price
                   FROM PriceHistory ph
                   WHERE ph.product_id = ?
                   ORDER BY ph.date_recorded DESC
                   LIMIT 1
               """, (product_id,))
            last_price = cursor.fetchone()
            cursor.execute("""
                   SELECT p.current_price
                   FROM Products p
                   WHERE p.product_id = ?
               """, (product_id,))
            current_price = cursor.fetchone()
            return {
                'last_price': last_price[0] if last_price else None,
                'current_price': current_price[0] if current_price else None
            } if last_price and current_price else None

        # Метод get_user_id_by_telegram_id для получения ID пользователя по его Telegram ID
    @classmethod
    def get_user_id_by_telegram_id(cls, telegram_id):
        with cls.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT telegram_id FROM Users WHERE telegram_id = ?", (telegram_id,))
            result = cursor.fetchone()
            return result[0] if result else None

# Пример использования
# DataBaseHelper.create_tables()
# DataBaseHelper.add_user('JohnDoe')
# Далее можно использовать другие функции для добавления товаров и т.д.

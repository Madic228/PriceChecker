import sqlite3


class DataBaseHelper:
    def __init__(self, db_name="PriceCheckerDB.sql"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                user_id INT PRIMARY KEY,
                username VARCHAR
            );
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Products (
                product_id INT PRIMARY KEY,
                product_name VARCHAR,
                product_url VARCHAR,
                product_image_url VARCHAR,
                current_price DECIMAL
            );
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS TrackedProducts (
                tracked_id INT PRIMARY KEY,
                user_id INT,
                product_id INT,
                tracking_date DATE,
                FOREIGN KEY (user_id) REFERENCES Users (user_id),
                FOREIGN KEY (product_id) REFERENCES Products (product_id)
            );
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS PriceHistory (
                price_history_id INT PRIMARY KEY,
                product_id INT,
                date_recorded DATE,
                price DECIMAL,
                FOREIGN KEY (product_id) REFERENCES Products (product_id)
            );
        ''')

        self.conn.commit()

    # Дополнительные функции для работы с базой данных
    # Например, добавление пользователя, добавление товара для отслеживания, обновление цен и т.д.

    def add_user(self, user_id, username):
        self.cursor.execute("INSERT INTO Users (user_id, username) VALUES (?, ?)", (user_id, username))
        self.conn.commit()

    def add_product(self, product_id, product_name, product_url, product_image_url, current_price):
        self.cursor.execute(
            "INSERT INTO Products (product_id, product_name, product_url, product_image_url, current_price) VALUES (?, ?, ?, ?, ?)",
            (product_id, product_name, product_url, product_image_url, current_price))
        self.conn.commit()

    def track_product(self, user_id, product_id, tracking_date):
        self.cursor.execute("INSERT INTO TrackedProducts (user_id, product_id, tracking_date) VALUES (?, ?, ?)",
                            (user_id, product_id, tracking_date))
        self.conn.commit()

    def update_price(self, product_id, new_price):
        self.cursor.execute("UPDATE Products SET current_price = ? WHERE product_id = ?", (new_price, product_id))
        self.conn.commit()

    # Добавьте здесь дополнительные функции по мере необходимости

    def __del__(self):
        self.conn.close()


# Пример использования
#db_helper = DataBaseHelper()
#db_helper.create_tables()
# Далее можно использовать функции для добавления пользователей, товаров и т.д.

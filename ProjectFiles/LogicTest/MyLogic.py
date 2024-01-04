import re
from datetime import datetime
from ProjectFiles.PriceParser.parser_detail import MegaMarketSeleniumParser
from ProjectFiles.db.DataBaseHelper import DataBaseHelper

class ProductTracker:
    def __init__(self, username):
        self.parser = MegaMarketSeleniumParser()
        DataBaseHelper.create_tables()
        if not DataBaseHelper.user_exists(username):
            DataBaseHelper.add_user(username)
        self.user_id = self.get_user_id(username)

    def get_user_id(self, username):
        conn = DataBaseHelper.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM Users WHERE username = ?", (username,))
        user_id = cursor.fetchone()[0]
        conn.close()
        return user_id

    def track_products(self):
        urls = []
        while True:
            url = input("Введите URL товара или 'quit' для выхода: ")
            if url == 'quit':
                break
            if not re.match(r'https://megamarket.ru/catalog/details/', url):
                print("URL должен начинаться с 'https://megamarket.ru/catalog/details/'")
                continue
            urls.append(url)

        for url in urls:
            product_info = self.parser.parse_product(url)
            if product_info:
                self.parser.save_to_db(product_info, url)
                self.track_product(url)

    def track_product(self, url):
        conn = DataBaseHelper.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT product_id FROM Products WHERE product_url = ?", (url,))
        product_id = cursor.fetchone()[0]

        # Проверка на существование записи
        cursor.execute("SELECT * FROM TrackedProducts WHERE user_id = ? AND product_id = ?", (self.user_id, product_id))
        if cursor.fetchone() is None:
            DataBaseHelper.track_product(self.user_id, product_id, datetime.now().date())
        else:
            print(f"Продукт с URL '{url}' уже отслеживается.")
        conn.close()

    def display_tracked_products(self):
        conn = DataBaseHelper.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.product_name, p.product_url, t.tracking_date
            FROM TrackedProducts t
            JOIN Products p ON t.product_id = p.product_id
            WHERE t.user_id = ?
        """, (self.user_id,))
        for row in cursor.fetchall():
            print(row)
        conn.close()

def main():
    username = input("Введите ваше имя пользователя: ")
    tracker = ProductTracker(username)
    tracker.track_products()
    tracker.display_tracked_products()
    tracker.parser.close_browser()

if __name__ == '__main__':
    main()

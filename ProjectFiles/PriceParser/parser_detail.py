import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from ProjectFiles.db.DataBaseHelper import DataBaseHelper

class MegaMarketSeleniumParser:
    def __init__(self):
        self.driver = None

    def start_browser(self):
        self.driver = webdriver.Chrome(service=Service("chromedriver.exe"))
        self.driver.maximize_window()

    def parse_product(self, url):
        if not self.driver:
            self.start_browser()
        self.driver.get(url)
        WebDriverWait(self.driver, 60).until(ec.presence_of_element_located((By.CLASS_NAME, "base-gallery-slide")))
        soup = BeautifulSoup(self.driver.page_source, 'lxml')

        title_tag = soup.find('h1', itemprop='name')
        title = title_tag.get_text(strip=True) if title_tag else "Название не найдено"

        image_tag = soup.find('div', class_='base-gallery-slide').find('img', class_='inner-image-zoom_image')
        image_url = image_tag['src'] if image_tag else "Изображение не найдено"

        price_tag = soup.find('span', class_='sales-block-offer-price__price-final')
        price = price_tag.get_text(strip=True) if price_tag else "Цена не найдена"

        return {'title': title, 'image_url': image_url, 'price': price}

    def save_to_db(self, product_info, product_url):
        if not DataBaseHelper.product_exists(product_info['title'], product_url):
            DataBaseHelper.add_product(product_info['title'], product_url, product_info['image_url'],
                                       product_info['price'])
        else:
            current_price = DataBaseHelper.get_current_price(product_url)
            if current_price != product_info['price']:
                print(f"Цена изменилась: старая цена {current_price}, новая цена {product_info['price']}")
                DataBaseHelper.update_price(product_url, product_info['price'])
                DataBaseHelper.add_price_history(product_url, product_info['price'])
            else:
                print("Продукт уже существует в базе данных и цена осталась прежней")

    def close_browser(self):
        if self.driver:
            self.driver.close()
            self.driver.quit()

def main():
    DataBaseHelper.create_tables()
    parser = MegaMarketSeleniumParser()
    urls = ["https://megamarket.ru/catalog/details/motopompa-huter-mp-25-100001322759_54648/", "https://megamarket.ru/catalog/details/dvb-t2-pristavka-bbk-smp028hdt2-black-100028074362_32036/", "https://megamarket.ru/catalog/details/igrovaya-pristavka-sony-playstation-5-cfi-1200a-japan-3gen-600011776874_90207/"]  # Список URL-адресов для парсинга

    for url in urls:
        product_info = parser.parse_product(url)
        print(product_info)
        parser.save_to_db(product_info, url)  # Передаем URL вместе с информацией о продукте
    parser.close_browser()

if __name__ == '__main__':
    main()

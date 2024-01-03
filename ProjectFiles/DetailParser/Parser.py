import io
import random
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from pychromedriver import chromedriver_path

class MegaMarketSeleniumParser:
    def __init__(self):
        user_agents_list = [
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ',
            'Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00',
            'Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)'
        ]

        options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={random.choice(user_agents_list)}')

        self.driver = webdriver.Chrome(
            service=Service(chromedriver_path),
            options=options
        )

    def parse_product(self, url):
        self.driver.get(url)
        time.sleep(5)  # задержка для полной загрузки страницы

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        title_tag = soup.find('h1', itemprop='name')
        title = title_tag.get_text(strip=True) if title_tag else "Название не найдено"

        image_tag = soup.find('img', class_='gallery__thumb-img')
        image_url = image_tag['src'] if image_tag else "Изображение не найдено"

        price_tag = soup.find('span', class_='sales-block-offer-price__price-final')
        price = price_tag.get_text(strip=True) if price_tag else "Цена не найдена"

        return {'title': title, 'image_url': image_url, 'price': price}

    def close(self):
        self.driver.quit()

# Пример использования
parser = MegaMarketSeleniumParser()
product_info = parser.parse_product("https://megamarket.ru/catalog/details/motopompa-huter-mp-25-100001322759_54648/")
print(product_info)
parser.close()

import requests
from bs4 import BeautifulSoup
import random


class MegaMarketParser:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15",
            # Добавьте больше юзер-агентов по желанию
        ]

    def parse_product(self, url):
        if not url.startswith("https://megamarket.ru/catalog/details/"):
            return "Неверный формат URL"

        headers = {'User-Agent': random.choice(self.user_agents)}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return "Ошибка при доступе к сайту"

        soup = BeautifulSoup(response.content, 'html.parser')

        # Название товара
        title_tag = soup.find('h1', itemprop='name')
        title = title_tag.get_text(strip=True) if title_tag else "Название не найдено"

        # Ссылка на изображение
        image_tag = soup.find('img', class_='gallery__thumb-img')
        image_url = image_tag['src'] if image_tag and 'src' in image_tag.attrs else "Изображение не найдено"

        # Цена товара
        price_tag = soup.find('span', class_='sales-block-offer-price__price-final')
        price = price_tag.get_text(strip=True) if price_tag else "Цена не найдена"

        return {'title': title, 'image_url': image_url, 'price': price}

    def get_html_content(self, url):
        headers = {'User-Agent': random.choice(self.user_agents)}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return "Ошибка при доступе к сайту"

        return response.text


# Пример использования
parser = MegaMarketParser()
product_info = parser.parse_product("https://megamarket.ru/catalog/details/motopompa-huter-mp-25-100001322759_54648/")
print(product_info)

# Для получения полного HTML-кода страницы (для анализа)
html_content = parser.get_html_content("https://megamarket.ru/catalog/details/motopompa-huter-mp-25-100001322759_54648/")
print(html_content)

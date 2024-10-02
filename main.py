import threading
import urllib
import requests
from bs4 import BeautifulSoup

from models import Result, Category

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

result = Result()

with requests.Session() as s:
    page = s.get('https://www.bethowen.ru/shops/', headers=headers)
    cookies = s.cookies
    cookies.set('BETHOWEN_GEO_TOWN', urllib.parse.quote_plus(result.city), domain='www.bethowen.ru', path='/')
    html = s.get('https://www.bethowen.ru/shops/', headers=headers, cookies=cookies)
    soup = BeautifulSoup(html.text, 'html.parser')
    result.set_shop_list(soup.findAll('div', class_='dgn-leading-5'))
    html = s.get('https://www.bethowen.ru/catalogue/', headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    category_list = soup.findAll('h2', class_='dgn-text-left')
    catalog = []
    for i in category_list:
        cat = i.find('a')
        category = Category(cat.text, 'https://www.bethowen.ru' + cat.get('href'))
        catalog.append(category)
    for i in catalog:
        i.category_pagen(s, headers)
        i.get_products_info(s, headers)
        i.get_products_shop(s, headers, result)

result.save_info()
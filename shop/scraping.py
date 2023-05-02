import os
import sys
from bs4 import BeautifulSoup
import requests
import re
from decimal import Decimal
# Добавьте путь к вашей папке проекта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
from main.settings import URL_SCRAPING_DOMAIN, URL_SCRAPING

#product-list1

"""
{
    'name': 'Одноразовая Pod система Joyetech VAAL 1500 Pineapple Ice 50 мг 1100 мАч', 
    'image_url': 'https://vapelife.com.ua/image/cache/catalog/pod-sistemu/joyetech-vaal-1500-disposable-pod/xjoyetech-vaal-1500-pineapple-ice-50mg-1100mah-200x200.jpg.pagespeed.ic.0GYgJICOdx.webp', 
    'price': Decimal('150.00'), 
    'unit': 'за шт', 
    'code': '38140012'
 }

"""
def scraping():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    URL_SCRAPING = 'https://vapelife.com.ua/odnorazovye-pod-sistemy/'
    resp = requests.get(URL_SCRAPING, headers=headers, timeout=40.0)
    if resp.status_code != 200:
        raise Exception('HTTP error access!')

    data_list = []
    html = resp.text

    soup = BeautifulSoup(html, 'html.parser')
    soup = BeautifulSoup(html, 'html.parser')
    blocks = soup.select('.product-list1 ')

    for block in blocks:
        data = {}
        
        name = block.select_one('.text-dark').get_text().strip()
        data['name'] = name

        image_url = URL_SCRAPING_DOMAIN + block.select_one('img')['src']
        data['image_url'] = image_url

        price_raw = block.select_one('.price').text
        number_string = price_raw.strip().split()[0]  # удаление пробелов и выбор первого слова
        price = int(number_string)
        price = Decimal(price)
        data['price'] = price   # 150

        url_detail = block.select_one('.text-dark')
        # <a class="text-dark" href="xxxxx">

        url_detail = url_detail['href']
        # 'xxxx'
        
        html_detail = requests.get(url_detail, 'html.parser', headers=headers).text
        soup = BeautifulSoup(html_detail, 'html.parser')
        body = soup.body
        code = body['class'][0]
        code = int(code.split('-')[2])
        data['code'] = code

        data_list.append(data)
    print(data_list)
        



if __name__ == '__main__':
    scraping()
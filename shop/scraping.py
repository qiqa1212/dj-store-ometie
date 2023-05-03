import os
import sys
from bs4 import BeautifulSoup
import requests
import re
from decimal import Decimal

from .models import Product


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
    'code': '38140012'
 }

"""

class ScrapingError(Exception):
    pass


class ScrapingTimeoutError(ScrapingError):
    pass


class ScrapingHTTPError(ScrapingError):
    pass


class ScrapingOtherError(ScrapingError):
    pass




def scraping():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    URL_SCRAPING = 'https://vapelife.com.ua/odnorazovye-pod-sistemy/'
    try:
        resp = requests.get(URL_SCRAPING, headers=headers, timeout=10.0)
    except requests.exceptions.Timeout:
        raise ScrapingTimeoutError("request timed out")
    except Exception as e:
        raise ScrapingOtherError(f'{e}')
    
    if resp.status_code != 200:
        raise ScrapingHTTPError(f"HTTP {resp.status_code}: {resp.text}")

    data_list = []
    soup = BeautifulSoup(resp.text, 'html.parser')
    blocks = soup.select('.product-list1')
    for i in range(0, 30, 3):
        for block in blocks[i:i+3]:
            data = {}

            try:
                name = block.select_one('.text-dark').get_text(strip=True)
                data['name'] = name

                image_url = URL_SCRAPING_DOMAIN + block.select_one('img')['src']
                data['image_url'] = image_url

                price_raw = block.select_one('.price').text.strip().split()[0]
                price = Decimal(price_raw)
                data['price'] = price

                url_detail = block.select_one('.text-dark')['href']
                html_detail = requests.get(url_detail, headers=headers, timeout=60.0).text
                soup = BeautifulSoup(html_detail, 'html.parser')
                body = soup.body
                code = body['class'][0]
                code = int(code.split('-')[2])
                data['code'] = code
                print(data)
                data_list.append(data)
                

            except Exception as e:
                print(f"Error occurred: {e}")
                continue
            
        print(len(data_list))

        for item in data_list:
            if not Product.objects.filter(code=item['code']).exists():
                Product.objects.create(
                    name=item['name'],
                    code=item['code'],
                    price=item['price'],
                    image_url=item['image_url'],
                )

            return data_list
        



if __name__ == '__main__':
    scraping()
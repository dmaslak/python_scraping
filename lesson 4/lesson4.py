from lxml import html
import requests
from pymongo import MongoClient

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

response = requests.get('https://yandex.ru/news', headers = header)
dom = html.fromstring(response.text)
items = dom.xpath("//article")

client = MongoClient('127.0.0.1', 27017)
db = client['yandex_news']
yandex_news = db.yandex_news

for item in items:
    items_data = {}
    
    link = item.xpath('.//a[contains(@href, "yandex")]')[0].get("href")
    title = item.xpath('.//h2[contains(@class, "title")]')[0].text
    source = item.xpath('.//a[contains(@class, "mg-card__source-link")]')[0].text
    timestamp = item.xpath('.//span[contains(@class, "mg-card-source__time")]')[0].text
    

    items_data['title'] = title
    items_data['link'] = link
    items_data['source'] = source
    items_data['timestamp'] = timestamp
    
    yandex_news.update_one({'link': link}, {'$set': items_data}, upsert = True)


import re
import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/фентези/?price_min=0&price_max=100', 
                'https://www.labirint.ru/search/фентези/?price_min=100&price_max=200',
                'https://www.labirint.ru/search/фентези/?price_min=200&price_max=300',
                'https://www.labirint.ru/search/фентези/?price_min=300&price_max=400',
                'https://www.labirint.ru/search/фентези/?price_min=400&price_max=500',
                'https://www.labirint.ru/search/фентези/?price_min=500&price_max=600',
                'https://www.labirint.ru/search/фентези/?price_min=600&price_max=700',
                'https://www.labirint.ru/search/фентези/?price_min=700&price_max=800',
                'https://www.labirint.ru/search/фентези/?price_min=800&price_max=900',
                'https://www.labirint.ru/search/фентези/?price_min=900&price_max=1000',
                'https://www.labirint.ru/search/фентези/?price_min=1000']

    def parse(self, response: HtmlResponse):
        base_url = 'https://www.labirint.ru'
        relative_links = response.xpath('//a[@class="product-title-link"]/@href').getall()
        links = [f'{base_url}{link}' for link in relative_links]
        next_page = response.xpath('//a[@title="Следующая"]/@href').get()

        if next_page:
            yield response.follow(next_page, callback = self.parse)

        for link in links:
            yield response.follow(link, callback = self.parse_one_book)
        print(response.url)
    
    def parse_one_book(self, response: HtmlResponse):
        url = response.url
        name = response.xpath('//h1/text()').get()
        author = response.xpath('//a[@data-event-label="author"]/text()').get()
        price_with_no_discount = response.xpath('//span[@class="buying-priceold-val-number"]/text()').get()
        price = response.xpath('//span[@class="buying-pricenew-val-number"]/text()').get()
        rating = response.xpath('//div[@id="rate"]/text()').get()
        yield BookparserItem(url = url, 
                            name = name, author = author, 
                            price_with_no_discount = price_with_no_discount,
                            price = price,
                            rating = rating)

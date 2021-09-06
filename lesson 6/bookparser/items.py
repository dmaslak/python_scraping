# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    price_with_no_discount = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    _id = scrapy.Field()
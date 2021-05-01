# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AgonesgrScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    flag = scrapy.Field()
    time = scrapy.Field()
    gid = scrapy.Field()
    home = scrapy.Field()
    away = scrapy.Field()
    one = scrapy.Field()
    chi = scrapy.Field()
    two = scrapy.Field()
    score = scrapy.Field()

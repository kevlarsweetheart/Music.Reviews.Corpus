# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ReviewsCrawlerItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    album_year = scrapy.Field()
    review_year = scrapy.Field()
    author = scrapy.Field()
    artist = scrapy.Field()
    album = scrapy.Field()
    rating = scrapy.Field()
    genre = scrapy.Field()
    source = scrapy.Field()
    text = scrapy.Field()
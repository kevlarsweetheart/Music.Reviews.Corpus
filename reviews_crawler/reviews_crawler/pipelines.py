# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class ReviewsCrawlerPipeline(object):

    def __init__(self):
        self.connection = sqlite3.connect("reviews.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("DROP TABLE IF EXISTS reviews;")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS reviews (_id text PRIMARY KEY,
            artist text,
            album text,
            rating text,
            genre text,
            author text,
            album_year text,
            review_date text,
            source text,
            url text);""")

    def process_item(self, item, spider):
        self.cursor.execute("""INSERT INTO reviews (_id, artist, album, rating, genre, author, album_year, source, url) VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?);""", (item['_id'], item['artist'], item['album'], item['rating'], item['genre'], item['author'],
                                                               item['album_year'], item['source'], item['url']))
        self.connection.commit()
        with open("./review_texts/" + item['_id'], 'w') as output:
            output.write(item['text'])
        return item

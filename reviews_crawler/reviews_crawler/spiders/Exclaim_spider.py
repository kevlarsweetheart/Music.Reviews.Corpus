import scrapy
import uuid
from reviews_crawler.items import ReviewsCrawlerItem
import re

class SlantMagazineReviewsCrawler(scrapy.Spider):
    name = 'Exclaim_reviews'
    start_urls = ['https://exclaim.ca/music/reviews/page/1']
    allowed_domains = ['www.exclaim.ca']

    def ParsePage(self, response):
        pages = response.xpath('//a[contains(@data-title, "News")]//@href').extract()
        for page in pages:
            yield scrapy.Request(page, callback=self.ParseReviewPage)

    def ParseReviewPage(self, response):
        _id = str(uuid.uuid4().hex)
        url = response.url
        album = response.xpath('//span[contains(@class, "article-subtitle")]//text()').extract_first()
        rating = str(int(float(response.xpath('//div[contains(@class, "article-rating")]//text()').extract_first()) * 10))
        author = response.xpath('//div[contains(@class, "article-author")]//a//text()').extract_first()
        artist = response.xpath('//span[contains(@class, "article-title")]//text()').extract_first()
        genre = response.xpath('//li[contains(@class, "filters-selected-item")]//text()').extract()[2:-1]
        albumYear = ""
        reviewYear = response.xpath('//div[contains(@class, "article-published")]//text()').extract_first()[-4:]
        source = 'Exclaim'
        text = response.xpath('//div[contains(@class, "article")]//text()').extract()
        l = text.index("MUSIC")
        text = [re.sub(r'(\n+|\xa0)', '', t) for t in text[:l]]
        text = ''.join([t for t in text if t != ''][7:])
        review = ReviewsCrawlerItem(_id=_id, url=url, album_year=albumYear, review_year=reviewYear, author=author, artist=artist, album=album, rating=rating, source=source, text=text, genre=genre)
        yield review

    # Visit Exclaim reviews pages from February 2013 to October 2018
    def parse(self, response):
        for page in range(1, 1101):
            new_page = response.url[:-1] + str(page)
            yield scrapy.Request(new_page, callback=self.ParsePage)
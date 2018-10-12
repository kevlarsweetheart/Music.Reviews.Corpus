import scrapy
import uuid
from reviews_crawler.items import ReviewsCrawlerItem

class SlantMagazineReviewsCrawler(scrapy.Spider):
    name = 'SlantMagazine_reviews'
    start_urls = ['https://www.slantmagazine.com/music/P10']
    allowed_domains = ['www.slantmagazine.com']

    def ParsePage(self, response):
        pages = response.xpath('//article//a/@href').extract()
        for page in pages:
            if 'review' in page.split('/'):
                yield scrapy.Request(page, callback=self.ParseReviewPage)

    def ParseReviewPage(self, response):
        _id = str(uuid.uuid4().hex)
        url = response.url
        album = response.xpath('//span[contains(@class, "sub-title")]/cite/text()').extract_first()
        rating = str(int(float(response.xpath('//p[contains(@class, "rating")]//img/@alt').extract_first()[:3]) * 20))
        author = response.xpath('//span[contains(@itemprop, "author")]/span/text()').extract_first()[2:-2]
        artist = response.xpath('//h1[contains(@class, "article-title")]/text()').extract_first()[5:-1]
        genre = ""
        albumYear = response.xpath('//div[contains(@id, "music-details")]/dl/dd/text()').extract_first()[-4:]
        reviewYear = response.xpath('//p[contains(@class, "byline-date byline")]/time/text()').extract_first()[-6:-2]
        source = 'Slant Magazine'
        text = []
        for a in response.xpath('//span[contains(@class, "loadable")]/p'):
            text.append("".join(a.xpath(".//text()").extract()))
        text = ' '.join(text)
        review = ReviewsCrawlerItem(_id=_id, url=url, album_year=albumYear, review_year=reviewYear, author=author, artist=artist, album=album, rating=rating, source=source, text=text, genre=genre)
        yield review

    # Visit Slant Magazine reviews pages from January 2012 to October 2018
    def parse(self, response):
        for page in range(10, 1051, 20):
            new_page = response.url[:-2] + str(page)
            yield scrapy.Request(new_page, callback=self.ParsePage)
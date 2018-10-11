import scrapy
import uuid
from reviews_crawler.items import ReviewsCrawlerItem
from tqdm import trange

class PitchforkReviewsCrawler(scrapy.Spider):
    name = 'Pitchfork_reviews'
    start_urls = ['https://pitchfork.com/reviews/albums/?page=1']
    allowed_domains = ['pitchfork.com']

    def ParsePage(self, response):
        pages = response.xpath('//a[contains(@class, "review__link")]/@href').extract()
        for page in pages:
            yield scrapy.Request('https://pitchfork.com' + page, callback=self.ParseReviewPage)

    def ParseReviewPage(self, response):
        _id = str(uuid.uuid4().hex)
        url = response.url
        album = response.xpath('//div[contains(@class, "single-album-tombstone")]//h1[contains(@class, "single-album-tombstone__review-title")]/text()').extract_first()
        rating = str(int(float(response.xpath('//div[contains(@class, "score-box ")]//span/text()').extract_first()) * 10))
        author = response.xpath('//ul[contains(@class, "authors-detail")]//a[contains(@class, "authors-detail__display-name")]/text()').extract_first()
        artist = response.xpath('//div[contains(@class, "single-album-tombstone")]//a/text()').extract_first()
        genre = response.xpath('//a[contains(@class, "genre-list__link")]/text()').extract_first()
        albumYear = response.xpath('//span[contains(@class, "single-album-tombstone__meta-year")]/text()').extract()[-1]
        source = 'Pitchfork'
        text = []
        for a in response.xpath('//div[contains(@class, "contents dropcap")]/p'):
            text.append("".join(a.xpath(".//text()").extract()))
        text = ' '.join(text)
        review = ReviewsCrawlerItem(_id=_id, url=url, album_year=albumYear, author=author, artist=artist, album=album, rating=rating, genre=genre, source=source, text=text)
        yield review

    # Visit Pitchfork reviews pages from January 2015 to October 2018
    def parse(self, response):
        for page in trange(1, 386):
            new_page = response.url[:-1] + str(page)
            yield scrapy.Request(new_page, callback=self.ParsePage)
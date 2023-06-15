import scrapy


class TrackSpider(scrapy.Spider):
    name = 'Track'
    allowed_domains = ['www.google.com']
    start_urls = ['http://www.google.com/']

    def parse(self, response):
        pass

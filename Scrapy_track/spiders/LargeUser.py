#In this I will show you how to use middleware to crate alot of user-agentts


import scrapy
from Scrapy_track.items import BookItem
import random
from urllib.parse import urlencode
API_KEY = '0244298d-d5eb-431a-9934-b89ee9a09853'

def get_proxy_url(url):
    payload= {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

class LargeScrapyUserAgent(scrapy.Spider):
    name = 'userAgent'
    allowed_domains = ['books.toscrape.com', 'proxy.scrapeops.io']
    start_urls = ['https://books.toscrape.com/']

    def start_requests(self):
        yield scrapy.Request(url=get_proxy_url(self.start_urls[0]), callback =self.parse)


  

    def parse(self, response):
        books = response.css("article.product_pod")
        for book in books:
            relative_url = book.css("h3 a ::attr(href)").get()
            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url 
            yield response.follow(url=book_url, callback= self.parse_book_page)

    def parse_book_page(self, response):
        book_item = BookItem()
        book_item["title"] = response.css(".product_main h1::text").get()
        book_item["price"] = response.css(".product_main p::text").get()
        book_item["description"] = response.xpath("//article/p/text()").get()
        book_item["category"] = response.xpath("//ul[@class='breadcrumb']/li[3]/a/text()").get()

        yield book_item
import scrapy
from Scrapy_track.items import BookItem

class SaveScrapy(scrapy.Spider):
    name = 'Save'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):
        books = response.css("article.product_pod")
        for book in books:
            relative_url = book.css("h3 a ::attr(href)").get()
            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url 
            yield response.follow(book_url, callback= self.parse_book_page)

    def parse_book_page(self, response):
        # title = response.css(".product_main h1::text").get()
        # price = response.css(".product_main p::text").get()
        # description = response.xpath("//article/p/text()").get()
        # category = response.xpath("//ul[@class='breadcrumb']/li[3]/a/text()").get()

        book_item = BookItem()

        book_item["title"] = response.css(".product_main h1::text").get()
        book_item["price"] = response.css(".product_main p::text").get()
        book_item["description"] = response.xpath("//article/p/text()").get()
        book_item["category"] = response.xpath("//ul[@class='breadcrumb']/li[3]/a/text()").get()

        yield book_item



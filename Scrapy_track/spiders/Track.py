import scrapy


class TrackSpider(scrapy.Spider):
    name = 'Track'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):
        books = response.css("article.product_pod")
        for book in books:
            yield{
                'name': book.css("h3 a::text").get(),
                'price': book.css(".product_price .price_color::text").get(),
                'link': book.xpath("//h3/a/@href").get(),
            }
            
        next_page = response.css("li.next a ::attr(href)").get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback= self.parse)


        # image = response.xpath("//article/div/a/img/@src").get()
        # url = response.xpath("//article/h3/a/@href").get()
        # text = response.xpath("//article/h3/a/text()").get()
        # price = response.xpath("//article/div/p/text()").get()

        # yield{
        #     "image": books,
        #     # "text": text,
        #     # "url": url,
        #     # "price": price,
        # }

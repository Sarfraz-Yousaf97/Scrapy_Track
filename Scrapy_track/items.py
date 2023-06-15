# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyTrackItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

# def get_serilized_data(value):
#     return f'$ {str(value)}'


class BookItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
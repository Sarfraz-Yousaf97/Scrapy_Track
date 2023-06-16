# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapyTrackPipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)

        ## Strip all whitespaces from strings
        # field_names = adapter.field_names()
        # for field_name in field_names:
        #     if field_name != 'description':
        #         value = adapter.get(field_name)
        #         adapter[field_name] = value[0].strip()


        ## Category & Product Type --> switch to lowercase
        # lowercase_keys = ['category', 'product_type']
        # for lowercase_key in lowercase_keys:
        #     value = adapter.get(lowercase_key)
        #     adapter[lowercase_key] = value.lower()



        # Price --> convert to float
        price_keys = ['price']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = str(value)


        ## Availability --> extract number of books in stock
        # availability_string = adapter.get('availability')
        # split_string_array = availability_string.split('(')
        # if len(split_string_array) < 2:
        #     adapter['availability'] = 0
        # else:
        #     availability_array = split_string_array[1].split(' ')
        #     adapter['availability'] = int(availability_array[0])



        ## Reviews --> convert string to number
        # num_reviews_string = adapter.get('num_reviews')
        # adapter['num_reviews'] = int(num_reviews_string)
        
        return item


import mysql.connector

class SaveToModelsPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'test3450',
            database = 'books'
        )

        self.cur = self.conn.cursor()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS books(
                id int NOT NULL auto_increment primary key, 
                title text,
                price DECIMAL,
                description text,
                category VARCHAR(255)
            )
            """)


    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute(""" insert into books (
            title, 
            price,
            description,
            category
            ) values (
                %s,
                %s,
                %s,
                %s
                )""", (
            item["title"],
            item["price"],
            str(item["description"][0]), # 0 is added for adding only one char for demo
            item["category"]
        ))

        # ## Execute insert of data into database
        self.conn.commit()
        return item
    

    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()
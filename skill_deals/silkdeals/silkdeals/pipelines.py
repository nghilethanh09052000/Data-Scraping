# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import sqlite3
import pymongo

#conda install pymongo dnspython -y


class SilkdealsPipeline(object):

   

    # @classmethod
    # def from_crawler(cls, crawler):
    #     logging.warning(crawler.settings.get("MONGO_URL"))

    def open_spider(self, spider):

        self.connection = sqlite3.connect("computer.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute(
                '''
                    CREATE TABLE Computer
                    (
                        name TEXT
                        url TEXT
                        store_name TEXT
                        price TEXT
                    )

                '''
            )
            self.connection.commit()
        except: sqlite3.OperationalError
            
   

    def process_item(self, item, spider):
        self.c.execute(
            '''
                INSERT INTO Computer
                (
                    name,url,store_name,price
                )
                VALUES
                (
                    ?,?,?,?
                )
            ''',
            (
                item.get('name'),
                item.get('url'),
                item.get('store_name'),
                item.get('price')
            )
        )
        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.connection.close()

# class MongodbPipeline(object):
#     collection_name = "best_movies"

#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient("mongodb+srv://ahmed:testtest@cluster0-pbhxl.mongodb.net/test?retryWrites=true&w=majority")
#         self.db = self.client["IMDB"]

#     def close_spider(self, spider):
#         self.client.close()


#     def process_item(self, item, spider):
#         self.db[self.collection_name].insert(item)
#         return item
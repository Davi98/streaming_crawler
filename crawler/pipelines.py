# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from google.Bigquery import Bigquery
from google.Storage import Storage
import datetime



class CrawlerPipeline:
    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        print("spider closed")

        
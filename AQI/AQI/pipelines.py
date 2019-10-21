# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime

import pymongo
import redis
from scrapy.exporters import JsonItemExporter, CsvItemExporter


class AqiDataPipeline(object):
    def process_item(self, item, spider):
        item['data_time'] = str(datetime.datetime.utcnow())
        item['spider'] = spider.name
        return item

class AqiJsonPipeline(object):
    def open_spider(self, spider):
        self.file = open('aqi.json', 'wb')
        self.writer = JsonItemExporter(self.file)
        self.writer.start_exporting()

    def process_item(self, item, spider):
        self.writer.export_item(item)
        return item

    def close_spider(self, spider):
        self.writer.finish_exporting()
        self.file.close()

class AqiCsvPipeline(object):
    def open_spider(self, spider):
        self.file = open('aqi.csv', 'wb')
        self.writer = CsvItemExporter(self.file)
        self.writer.start_exporting()

    def process_item(self, item, spider):
        self.writer.export_item(item)
        return item

    def close_spider(self, spider):
        self.writer.finish_exporting()
        self.file.close()

# class AqiMongodbPipeline(object):
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(host="127.0.0.1", port=27107)
#         self.db = self.client['moAqi']
#         self.colletion = self.db['aqi']
#
#     def process_item(self, item, spider):
#         self.colletion.insert(dict(item))
#         return item
#
#     def close_spider(self, spider):
#         self.client.close()

class AqiRedisPipeline(object):
    def open_spider(self, spider):
        self.client = redis.Redis(host="127.0.0.1", port=6379)

    def process_item(self, item, spider):
        self.client.lpush('aqi_list_mo', dict(item))
        return item


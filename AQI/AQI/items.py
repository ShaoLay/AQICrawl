# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AqiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city_name = scrapy.Field()
    date = scrapy.Field()
    aqi = scrapy.Field()
    level = scrapy.Field()
    pm2_5 = scrapy.Field()
    pm_10 = scrapy.Field()
    so_2 = scrapy.Field()
    co = scrapy.Field()
    no_2 = scrapy.Field()
    o_3 = scrapy.Field()

    # 数据源的字段
    data_time = scrapy.Field()
    spider = scrapy.Field()


# -*- coding: utf-8 -*-
import scrapy


class AqiSpider(scrapy.Spider):
    name = 'aqi'
    allowed_domains = ['aqi.com']
    start_urls = ['http://aqi.com/']

    def parse(self, response):
        pass

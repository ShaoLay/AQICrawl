# -*- coding: utf-8 -*-
import scrapy

from AQI.items import AqiItem


class AqiSpider(scrapy.Spider):
    name = 'aqi'
    allowed_domains = ['aqistudy.cn']
    start_urls = ['https://www.aqistudy.cn/historydata/']
    base_url = 'https://www.aqistudy.cn/historydata/'


    def parse(self, response):
        city_name_list = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/ul/div[2]/li/a/text()').extract()
        city_link_list = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/ul/div[2]/li/a/@href').extract()

        for city_name, city_link in zip(city_name_list, city_link_list):
            item = AqiItem()
            item['city_name'] = city_name
            url = self.base_url + city_link
            yield scrapy.Request(url, meta={'citykey':item}, callback=self.parse_month)

    def parse_month(self, response):
        """
        解析月份的链接
        :param response:
        :return:
        """
        item = response.meta['citykey']
        month_link_lilst = response.xpath('/html/body/div[3]/div[1]/div[1]/table/tbody/tr/td[1]/a/@href').extract()
        for month_link in month_link_lilst:
            url = self.base_url + month_link
            yield scrapy.Request(url, meta={'citykey':item}, callback=self.parse_day)

    def parse_day(self, response):
        """
        解析目标数据  每天的数据
        :param response:
        :return:
        """
        item = response.meta['citykey']
        tr_list = response.xpath('//tr')
        tr_list.pop(0)
        for tr in tr_list:
            item['date'] = tr.xpath('/html/body/div[3]/div[1]/div[1]/table/tbody/tr/td[1]/text()').extract_first()
            item['aqi'] = tr.xpath('/html/body/div[3]/div[1]/div[1]/table/tbody/tr/td[2]/text()').extract_first()
            item['level'] = tr.xpath('/html/body/div[3]/div[1]/div[1]/table/tbody/tr/td[3]/text()').extract_first()
            item['pm2_5'] = tr.xpath('/html/body/div[3]/div[1]/div[1]/table/tbody/tr/td[4]/text()').extract_first()
            item['pm_10'] = tr.xpath('/html/body/div[3]/div[1]/div[1]/table/tbody/tr/td[5]/text()').extract_first()
            item['so_2'] = tr.xpath('/html/body/div[3]/div[1]/div[1]/table/tbody/tr/td[6]/text()').extract_first()
            item['co'] = tr.xpath('/html/body/div[3]/div[1]/div[1]/table/tbody/tr/td[7]/text()').extract_first()
            item['no_2'] = tr.xpath('/html/body/div[3]/div[1]/div[1]/table/tbody/tr/td[8]/text()').extract_first()
            item['o_3'] = tr.xpath('/html/body/div[3]/div[1]/div[1]/table/tbody/tr/td[9]/text()').extract_first()

            yield item


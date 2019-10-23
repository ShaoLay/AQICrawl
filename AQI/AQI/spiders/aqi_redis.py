import scrapy
from scrapy_redis.spiders import RedisSpider

from AQI.items import AqiItem


class AqiSpider(RedisSpider):
    name = 'aqi_redis'

    allowed_domains = ['aqistudy.cn']
    base_url = 'https://www.aqistudy.cn/historydata/'

    redis_key = 'aqiredis'

    def parse(self, response):
        city_name_list = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/ul/div[2]/li/a/text()').extract()[
                         36:37]
        city_link_list = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/ul/div[2]/li/a/@href').extract()[
                         36:37]

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
        month_link_lilst = response.xpath('/html/body/div[3]/div[1]/div[1]/table/tbody/tr/td[1]/a/@href').extract()[5:6]
        for month_link in month_link_lilst:
            url = self.base_url + month_link
            yield scrapy.Request(url, meta={'citykey': item}, callback=self.parse_day)

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
            # 日期
            item['date'] = tr.xpath('./td[1]/text()').extract_first()
            # AQI
            item['aqi'] = tr.xpath('./td[2]/text()').extract_first()
            # 质量等级
            item['level'] = tr.xpath('./td[3]//text()').extract_first()
            # PM2.5
            item['pm2_5'] = tr.xpath('./td[4]/text()').extract_first()
            # PM10
            item['pm_10'] = tr.xpath('./td[5]/text()').extract_first()
            # 二氧化硫
            item['so_2'] = tr.xpath('./td[6]/text()').extract_first()
            # 一氧化碳
            item['co'] = tr.xpath('./td[7]/text()').extract_first()
            # 二氧化氮
            item['no_2'] = tr.xpath('./td[8]/text()').extract_first()
            # 臭氧
            item['o_3'] = tr.xpath('./td[9]/text()').extract_first()

            yield item
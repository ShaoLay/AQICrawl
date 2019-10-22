from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from AQI.items import AqiItem


class AqiSpider(CrawlSpider):
    name = 'aqi_crawl'
    allowed_domains = ['aqistudy.cn']
    start_urls = ['https://www.aqistudy.cn/historydata/']

    rules = (
        Rule(LinkExtractor(allow='monthdata\.php')),
        Rule(LinkExtractor(allow='daydate\.php'), callback='parse_day', follow=False)
    )

    def parse_day(self, response):
        item = AqiItem()

        title = response.xpath('//*[@id="title"]/text()').extract_first()
        item['city_name'] = title[8:-11]

        # 1. 取出所有 tr_list
        tr_list = response.xpath('//tr')

        # 2.删除表头
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
            item['pm10'] = tr.xpath('./td[5]/text()').extract_first()
            # 二氧化硫
            item['so_2'] = tr.xpath('./td[6]/text()').extract_first()
            # 一氧化碳
            item['co'] = tr.xpath('./td[7]/text()').extract_first()
            # 二氧化氮
            item['no_2'] = tr.xpath('./td[8]/text()').extract_first()
            # 臭氧
            item['o_3'] = tr.xpath('./td[9]/text()').extract_first()

            # 将数据 -->engine-->pipeline
            yield item
# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# from selenium import webdriver
import scrapy
import time

from selenium import webdriver


class ChromeMiddlewares(object):
    def process_request(self, request, spider):
        url = request.url
        if url != 'https://www.aqistudy.cn/historydata/':
            # 设置无头浏览器
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(options=options)

            driver.get(url)
            time.sleep(3)
            data = driver.page_source
            driver.quit()

            return scrapy.http.HtmlResponse(url=url, body=data.encode('utf-8'), encoding="utf-8", request=request)

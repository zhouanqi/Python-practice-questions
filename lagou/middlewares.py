# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from scrapy.http import HtmlResponse
from scrapy.http import Response
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random
import os


class LagouSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LagouDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        # driver = spider.driver

        # #第一次请求获取总页数
        # if spider.start:

        #     driver.get(request.url)
           
        #     #等待异步加载，直到获取到当前页，最多等待10秒
        #     try:
        #         element = WebDriverWait(driver, 10).until(
        #             EC.presence_of_element_located((By.CLASS_NAME, 'pager_is_current'))
        #         )
        #         #获取所有非当前页的标签
        #         elements = driver.find_elements_by_xpath("//span[@class='pager_not_current']")
                
        #         #最后一个非当前页为总页数
        #         #读取出标签中内容
        #         page_count = elements[-1].get_attribute('innerHTML')
                
        #         #得到总页数
        #         spider.start = False
        #         spider.page_count = page_count
        #     finally: 
        #         pass
    
        return None


    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        # yield request
        pass
        

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# F:\python\chonghcong\lagou\Lagou\lagou
proxy_list = open('F:\\python\\chonghcong\\lagou\\Lagou\\lagou\\ip.txt').readlines()

class MyUserAgentMiddleware(UserAgentMiddleware):
    '''
    设置User-Agent
    '''
    refers = ['ios', 'python', 'andriod', 'html5', 'java']

    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('MY_USER_AGENT')
        )

    def process_request(self, request, spider):        
        request.meta['proxy'] = 'http://%s' % random.choice(proxy_list)
        agent = random.choice(self.user_agent)
        r1 = random.choice(self.refers)
        r2 = random.choice(self.refers)
        refer = 'https://www.lagou.com/jobs/list_{}?oquery={}&fromSearch=true&labelWords=relative&city=%E6%B7%B1%E5%9C%B3'.format(r1, r2) 
        request.headers['User-Agent'] = agent
        request.headers['Referer'] = refer
        print('User-Agent:' + agent)
        print('Proxy:' + request.meta['proxy'].strip())
        print('Referer:' + refer)


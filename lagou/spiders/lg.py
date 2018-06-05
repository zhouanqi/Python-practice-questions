# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request
from lagou.items import LagouItem
import lxml


class LgSpider(scrapy.Spider):
    name = 'lg'
    allowed_domains = ['logou.com']
    start_urls = ['http://logou.com/']

    #iOS岗位信息
    iOS_url = "https://www.lagou.com/zhaopin/iOS/?labelWords=label"
    def start_requests(self): 
    	yield Request(self.iOS_url, callback=self.parse)

    def parse(self, response):
    	targetContents = response.xpath('//div[@class="s_position_list "]/ul/li')


    	for targetContent in targetContents: 

    		job = LagouItem()

    		job['job_name'] = targetContent.xpath('div//h3/text()').extract()
    		job['job_addr'] = targetContent.xpath('div//span[@class="add"]/em/text()').extract()
    		job['job_time'] = targetContent.xpath('div//span[@class="format-time"]/text()').extract()
    		job['job_limit'] = targetContent.xpath('normalize-space(div//div[@class="li_b_l"])').extract()
    		job['job_company'] = targetContent.xpath('normalize-space(div//div[@class="company_name"]/a)').extract()
    		job['job_company_type'] = targetContent.xpath('normalize-space(div//div[@class="industry"])').extract()
    		job['job_vip']	= targetContent.xpath('div//div[@class="li_b_r"]/text()').extract()

    		yield job

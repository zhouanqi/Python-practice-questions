# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_name = scrapy.Field()	#岗位名称
    job_addr = scrapy.Field()	#上班地址
    job_time = scrapy.Field()	#发布时间
    job_limit = scrapy.Field()	#应聘资格
    job_company = scrapy.Field()#公司
    job_company_type = scrapy.Field()#公司类型
    job_vip = scrapy.Field()	#公司福利
    job_salary = scrapy.Field()
    page = scrapy.Field()
    positionId = scrapy.Field()

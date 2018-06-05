# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pandas as pd
import json

class LagouPipeline(object):

    def __init__(self):
        self.name = []
        self.addr = []
        self.time = []
        self.limit = []
        self.company = []
        self.type = []
        self.vip = []

    def process_item(self, item, spider):
        
        self.name.append(item['job_name'])
        self.addr.append(item['job_addr'])
        self.time.append(item['job_time'])
        self.limit.append(item['job_limit'])
        self.company.append(item['job_company'])
        self.type.append(item['job_company_type'])
        self.vip.append(item['job_vip'])    

    
    def close_spider(self, spider):
        # print(self.name)
        data = pd.DataFrame({
          '职位':self.name,
          '上班地址':self.addr,
          '发布时间':self.time,
          '任职资格':self.limit,
          '公司名称':self.company,
          '公司类型':self.type,
          '福利待遇':self.vip,
         })
         
        data.to_csv('../data.csv')

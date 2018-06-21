# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pandas as pd
import atlogin

class LagouPipeline(object):

    def __init__(self):
        self.name = []
        self.addr = []
        self.time = []
        self.limit = []
        self.company = []
        self.type = []
        self.vip = []
        self.salary = []
        self.page = []
        self.positionId = []

    def process_item(self, item, spider):
        
        self.name.append(item['job_name'])
        self.addr.append(item['job_addr'])
        self.time.append(item['job_time'])
        self.limit.append(item['job_limit'])
        self.company.append(item['job_company'])
        self.type.append(item['job_company_type'])
        self.vip.append(item['job_vip'])   
        self.salary.append(item['job_salary'])
        self.page.append(item['page'])
        self.positionId.append(item['positionId'])
    
    def close_spider(self, spider):
        data = pd.DataFrame({
          'name':self.name,
          'salary':self.salary,
          'addr':self.addr,
          'time':self.time,
          'limit':self.limit,
          'company':self.company,
          'type':self.type,
          'vip':self.vip,
          'page': self.page,
         })
        spider.success_pages.sort()
        print('success get data of page: ',spider.success_pages)
        print('开始投递')
        # atlogin.send_resume(spider.driver, self.positionId)
        spider.driver.quit()
        data.to_csv('./result.csv')

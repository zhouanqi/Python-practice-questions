# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request
from lagou.items import LagouItem
from atlogin import aotulogin 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By

import lxml
import json
import time
import requests
import random

class LgSpider(scrapy.Spider):

    #成功获取数据的页码
    success_pages = []

    name = 'lg'
    allowed_domains = ['logou.com']
    start_urls = ['http://logou.com/',
                  'https://www.lagou.com/jobs/positionAjax.json?']

    # addrrKey  = input("请输入地址:")
    # carrerKey = input("请输入岗位:")

    addrrKey = "深圳"
    carrerKey = "ios"

    #自动登录，获取driver进行操作
    driver = aotulogin()

    #url
    page_url = "https://www.lagou.com/jobs/list_{}?city={}&cl=false&fromSearch=true&labelWords=&suginput=".format(carrerKey, addrrKey)
    base_url = "https://www.lagou.com/jobs/positionAjax.json?"

    #headers
    headers = {
        'Host': 'www.lagou.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Referer': 'https://www.lagou.com/jobs/list_python?oquery=android&fromSearch=true&labelWords=relative&city=%E6%B7%B1%E5%9C%B3',
        }

    #参数
    params = {
        'city': addrrKey.encode('utf-8'),
        'kd': carrerKey.encode('utf-8'),
        'pn': '1',
        'px': 'new', #按最新发布排序
    }

    def fetch_page(self):
        self.driver.get(self.page_url)

        try: element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'pager_is_current'))
        )
        finally: pass
        elements = self.driver.find_elements_by_xpath("//span[@class='pager_not_current']")
        

        return elements[-1].get_attribute('innerHTML')

    def start_requests(self): 

        page_count = int(self.fetch_page())

        print('-'*80)
        print('总页数: ', page_count)
        print('-'*80)

        for page in range(1, page_count+1):
            print ('start request ...... page: ', self.params['pn'])
            yield scrapy.FormRequest(self.base_url, headers=self.headers, formdata=self.params, callback=self.parse)
            self.params['pn'] = str(page+1)


    def parse(self, response):
         
        text = json.loads(response.text)

        try:
            content = text['content']
        except Exception as e:
            print(text)
        finally:
            
        
        # print(json.load(response.text))

            page = content['pageNo']
            self.success_pages.append(page)

            print('success page: ', page)
            
            #解析数据，提取需要的数据
            results = content['positionResult']['result']
            for result in results: 
                job = LagouItem()
                job['job_name'] = result['positionName']
                job['job_addr'] = result['district']
                job['job_time'] = result['createTime']
                job['job_limit'] = result['education'] + '、' + result['workYear']
                job['job_salary'] = result['salary']
                job['job_company'] = result['companyFullName']
                job['job_company_type'] = result['financeStage'] + '、' + result['industryField']
                job['job_vip']  = result['positionAdvantage']
                job['page']  = page
                job['positionId'] = result['positionId']
                yield job


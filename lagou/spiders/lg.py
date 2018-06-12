# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request
from lagou.items import LagouItem
import lxml
import json
import time
import requests
import random

class LgSpider(scrapy.Spider):

    def __init__(self):
        
        #使用无头火狐获取总页数
        self.start = True

        #总页数
        self.page_count = 0

        #成功获取数据的页码
        self.success_pages = []

    name = 'lg'
    allowed_domains = ['logou.com']
    start_urls = ['http://logou.com/']

    addrrKey  = input("请输入地址:")
    carrerKey = input("请输入岗位:")

    #url
    start_url = "https://www.lagou.com/jobs/list_{carrerKey}?city={addrrKey}&cl=false&fromSearch=true&labelWords=&suginput="
    base_url = "https://www.lagou.com/jobs/positionAjax.json?"

    #headers
    headers = {
        'Host': 'www.lagou.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Referer': 'https://www.lagou.com/jobs/list_ios?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=&suginput=',
        'Cookie': 'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1528077741,1528443958; _ga=GA1.2.1803797481.1520242780; user_trace_token=20180305173939-2023722d-2059-11e8-b126-5254005c3644; LGUID=20180305173939-20237911-2059-11e8-b126-5254005c3644; _ga=GA1.3.1803797481.1520242780; index_location_city=%E6%B7%B1%E5%9C%B3; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1528771639; LGRID=20180612104718-ec49d143-6dea-11e8-9abd-525400f775ce; JSESSIONID=ABAAABAAADGAACF735E160CA071B6829354044274453968; _gid=GA1.2.1563861466.1528767607; X_HTTP_TOKEN=6324fb39e7a00daa51e443a65e76e064; TG-TRACK-CODE=undefined; _gat=1; LGSID=20180612104708-e60a6561-6dea-11e8-9479-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F'
        }

    #参数
    params = {
        'city': addrrKey.encode('utf-8'),
        'kd': carrerKey.encode('utf-8'),
        'pn': '1'
    }

    def start_requests(self): 

        print ('start request by Firefox ......')
        yield scrapy.Request(self.start_url.format(carrerKey=self.carrerKey, addrrKey=self.addrrKey), headers=self.headers, callback=self.get_page_count)
                                   
    def get_page_count(self, response):
        
        #从中间件中获取到的page_count
        page_count = int(self.page_count)

        print('-'*80)
        print('异步获取总页数: ', page_count)
        print('-'*80)

        for page in range(1, page_count+1):
            print ('start request ...... page: ', self.params['pn'])
            yield scrapy.FormRequest(self.base_url, headers=self.headers, formdata=self.params, callback=self.parse, dont_filter=True)
            self.params['pn'] = str(page+1)
            # time.sleep(random.randint(8,20))
            time.sleep(18)

    def parse(self, response):

        content = json.loads(response.text)['content']
       
        # print(json.load(response.text))

        page = content['pageNo']
        self.success_pages.append(page)
        
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
            yield job


# Lagou
爬取拉钩招聘信息

##### 框架

- scrapy

- lxml

- Panas

##### 运行

在根目录下执行:
> pip3 scrapy crawl lg / python3 -m scrapy crawl lg 

##### 结果

在Lagou目录下生成data.csv文件 

![data](https://github.com/TuYuWang/Lagou/blob/master/result.png)


##### 版本

- 0.01 爬取拉钩iOS岗位招聘信息，并以csv文件形式输出

- 0.02 使用selenium自动翻页爬取数据

- 0.03 添加代理ip，定时任务，更改请求头。提高成功率

详情请移步 -> [Python VS 拉钩](https://tuyuwang.github.io/tuyuwang.github.io/2018/07/02/Python-VS-%E6%8B%89%E5%8B%BE/)
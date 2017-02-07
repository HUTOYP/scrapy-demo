import sys
import scrapy
from scrapy import Selector
from scrapy import Request

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

class MySpider(CrawlSpider):
    name = "MySpider"
    host = "http://www.cnblogs.com/"
    # start_urls是我们准备爬的初始页
    # start_urls = [
    #     "http://www.cnblogs.com/sitehome/p/1",
    #     "http://www.cnblogs.com/sitehome/p/2",
    # ]

    start_urls = [
        "http://www.cnblogs.com/",
    ]

    # 方法1
    rules = (
        Rule(LinkExtractor(allow='sitehome/p/[0-9]{1,2}'), callback='parse_page', follow=True),
    )

    spider_url = "http://www.cnblogs.com/sitehome/p/"

    # 方法2
    # 爬虫的入口，可以在此进行一些初始化工作，比如从某个文件或者数据库读入起始url
    # def start_requests(self):
    #     # for url in self.start_urls:
    #     #     # 此处将起始url加入scrapy的待爬取队列，并指定解析函数
    #     #     # scrapy会自行调度，并访问该url然后把内容拿回来
    #     #     print(url)
    #     #     yield Request(url=url, callback=self.parse_page)
    #
    #     for pagenum in range(1, 50+1):
    #         url = self.spider_url + str(pagenum)
    #         print(url)
    #         yield Request(url=url, callback=self.parse_page)

    # 版面解析函数，解析一个版面上的帖子的标题和地址
    def parse_page(self, response):
        selector = Selector(response)
        content_list = selector.xpath("//*[@class='titlelnk']")
        for content in content_list:
            topic = content.xpath('string(.)').extract_first()
            print(topic)
            url = self.host + content.xpath('@href').extract_first()
            print(url)
            # 此处，将解析出的帖子地址加入待爬取队列，并指定解析函数
            # yield Request(url=url, callback=self.parse_topic)
        # 可以在此处解析翻页信息，从而实现爬取版区的多个页面

    # 帖子的解析函数，解析一个帖子的每一楼的内容
    def parse_topic(self, response):
        #selector = Selector(response)
        #content_list = selector.xpath("//*[@class='postcontent ubbcode']")
        #for content in content_list:
        #    content = content.xpath('string(.)').extract_first()
            print(response)
        # 可以在此处解析翻页信息，从而实现爬取帖子的多个页面

    # # 这个是解析函数，如果不特别指明的话，scrapy抓回来的页面会由这个函数进行解析。
    # # 对页面的处理和分析工作都在此进行，这个示例里我们只是简单地把页面内容打印出来。
    # def parse(self, response):
    #     #print(response.body.decode('utf-8'))
    #
    #     selector = Selector(response)
    #     # 在此，xpath会将所有class=topic的标签提取出来，当然这是个list
    #     # 这个list里的每一个元素都是我们要找的html标签
    #     content_list = selector.xpath("//*[@class='postTitle2']")
    #
    #     # 遍历这个list，处理每一个标签
    #     for content in content_list:
    #         # 此处解析标签，提取出我们需要的帖子标题。
    #         topic = content.xpath('string(.)').extract_first()
    #         print(topic)
    #         # 此处提取出帖子的url地址。
    #         url = self.host + content.xpath('@href').extract_first()
    #         print(url)


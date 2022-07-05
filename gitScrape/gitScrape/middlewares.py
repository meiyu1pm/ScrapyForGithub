# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import random
from gitScrape.settings import USER_AGENT_LIST, PROXY_LIST
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy import signals
# from scrapy.http import HtmlResponse
from base64 import b64encode
# from selenium import webdriver
# useful for handling different item types with a single interface
# from itemadapter import is_item, ItemAdapter


# 添加Selenium中间件后期留用
# class SeleniumMiddleware:
#     def process_request(self, request, spider):
#         # Called for each request that goes through the downloader
#         # middleware.

#         # Must either:
#         # - return None: continue processing this request
#         # - or return a Response object
#         # - or return a Request object
#         # - or raise IgnoreRequest: process_exception() methods of
#         #   installed downloader middleware will be called

#         url = request.url
#         driver = webdriver.Chrome()# '需要时把chromedriver放在同级目录下'
#         driver.get(url)
#         time.sleep(3)
#         data = driver.page_source
#         driver.close()
#         res = HtmlResponse(url=url, body=data, encoding='utf-8', request=request)
#         return res

#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent='Scrapy'):
        super().__init__()
        self.user_agent = user_agent
    
    def process_request(self, request, spider):
        ua = random.choice(USER_AGENT_LIST)
        # print(ua)
        if ua:
            request.headers.setdefault('User-Agent', ua)
        # return super().process_request(request, spider)

# 添加代理中间件后期留用
# class RandomProxy:
#     def process_request(self, request, spider):
#         proxy = random.choice(PROXY_LIST)
#         if 'user_passwd' in proxy:
#             # 对账号密码进行编码
#             b64_up = b64encode(proxy['user_passwd'].encode())
#             # 设置认证
#             request.headers['Proxy-Authorization'] = 'Basic' + b64_up.decode()
#             # 设置代理
#             request.meta['proxy'] = proxy['ip_port']
#         else:
#             request.meta['proxy'] = proxy['ip_port']


class GitscrapeSpiderMiddleware:
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

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
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


class GitscrapeDownloaderMiddleware:
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
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


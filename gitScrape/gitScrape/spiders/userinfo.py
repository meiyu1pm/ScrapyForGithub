import scrapy


class UserinfoSpider(scrapy.Spider):
    name = 'userinfo'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/']

    def parse(self, response):
        pass

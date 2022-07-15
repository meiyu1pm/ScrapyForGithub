import scrapy

GITHUB_API_HOST = 'api.github.com'
USER_NAME_LIST = []
class FollowerSpider(scrapy.Spider):
    name = 'Follower'
    allowed_domains = ['github.com']

    def start_requests(self):
        # print(USER_NAME_LIST) # 测试用
        for user_name in USER_NAME_LIST:
            start_url="https://{}/users/{}".format(GITHUB_API_HOST, user_name)
            
            yield scrapy.Request(
                url=start_url, 
                callback=self.parse,
                )

    def parse(self, response):
        pass

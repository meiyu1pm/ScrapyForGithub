import re
import scrapy
# from bs4 import BeautifulSoup
from urllib.parse import urljoin
from gitScrape.items import GitscrapeItem


class GitSpiderSpider(scrapy.Spider):
    name = 'git_spider'
    allowed_domains = ['github.com']
    
    def start_requests(self):
        import csv
        # loading user_name from csv file
        with open('./noEmail.csv', 'r') as f:
            data = csv.reader(f)
            USER_NAME_LIST = [row[1] for row in data]

        # print(USER_NAME_LIST) # 测试用
        # for user_name in self.user_names:
        for user_name in USER_NAME_LIST:
            start_url = f'https://github.com/{user_name}?tab=repositories'
            yield scrapy.Request(
                url=start_url, 
                callback=self.parse,
                meta={'user_name': user_name}
                )

    def parse(self, response):
        repo_url = response.xpath('//*[@id="user-repositories-list"]//h3/a/@href').extract_first()
        if repo_url:
            first_repo_url = response.urljoin(repo_url)

            user_name = response.meta['user_name']
            first_repo_url = first_repo_url + f'/commits?author={user_name}'

            # print('parse',first_repo_url) 测试用
            yield scrapy.Request(
                url=first_repo_url,
                callback=self.parse_commit,
                meta={'user_name': user_name}
            )
        else:
            print('Parse Error')
            return None

    def parse_commit(self, response):
        # I will find the first commit which is the latest commit
        commit = response.xpath(
            '//*[@id="repo-content-pjax-container"]//div[@class="BtnGroup"]/a/@href').extract_first()
        if not commit:
            print('Parse Commit Error')
            return None

        user_name = response.meta['user_name']
        email_url = urljoin(response.url, commit) + '.patch'
        # print('parse_commit', email_url) 测试用
        yield scrapy.Request(
            url=email_url,
            callback=self.parse_email,
            meta={'user_name': user_name}
        )

    def parse_email(self, response):
        item = GitscrapeItem()
        pat = re.compile("(\<.*@.*?\>)")
        user_name = response.meta['user_name']
        try:
            target = response.text.split('\n')[1]
            results = pat.findall(target)
            
        except:
            results = pat.findall(response.text)
            print('error in parse_email')

        item['user_name'] = user_name
        item['possible_email'] = list(set(results))
        yield item
        
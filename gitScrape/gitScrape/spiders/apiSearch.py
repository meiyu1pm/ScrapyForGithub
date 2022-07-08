import scrapy
import itertools
import json
import time # 如果需要休眠时打开
import redis # 临时任务安置
from collections import Counter
from gitScrape.items import GitscrapeItem


# 前置参数
GITHUB_API_HOST = 'api.github.com'
LANGUAGES = ['Python','Java','JavaScript','Ruby','TypeScript','C++', 'C', 'C#', 'HTML', 'PHP', 'Swift', 
             'Perl', 'CSS', 'Objective-C', 'Go','Shell','MATLAB']
TOP_CITIES = ['New York','Los Angeles','Chicago','Houston', 'Phoenix','Philadelphia','San Antonio',
              'San Diego','Dallas','San Jose','Austin','Jacksonville', 'Fort Worth','Columbus', 'Indianapolis', 
              'Charlotte',  'San Francisco',  'Seattle',  'Denver',  'Washington',  'Nashville-Davidson',  
              'Oklahoma City',  'El Paso',  'Boston',  'Portland',  'Las Vegas',  'Detroit',  'Memphis',  
              'Louisville-Jefferson County',  'Baltimore',  'Milwaukee',  'Albuquerque',  'Tucson',  'Fresno',  
              'Sacramento',  'Kansas City',  'Mesa',  'Atlanta',  'Omaha',  'Colorado Springs',  'Raleigh',  
              'Long Beach',  'Virginia Beach',  'Miami',  'Oakland',  'Minneapolis',  'Tulsa',  'Bakersfield',  'Wichita',  'Arlington']
# 私人tocken,请勿copy
headers = {
    'Authorization': 'token '+ "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",
    }
headers2 = {
    'Authorization': 'token '+ "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",
}

class ApisearchSpider(scrapy.Spider):
    name = 'apiSearch'
    allowed_domains = ['github.com']
    r = redis.Redis(host='localhost', port=6379, db=1)
    # 测试redis 连接情况
    if not r.ping(): print(Exception, 'conncet redis failed')


    def start_requests(self):
        # Find User By Location and Language
        ll_perm = itertools.product(LANGUAGES, TOP_CITIES)

        for lng, loc in ll_perm:
            for page in range(1, 5):
                url=f"https://{GITHUB_API_HOST}/search/users?q=type:user+language:%22{lng}%22+location:%22{loc}%22&page={page}"
                yield scrapy.Request(url=url, headers=headers ,callback=self.parse)

    def parse(self, response):
        # Find User Informations
        # 如果响应状态!=200,说明过量限流
        if response.status != 200:
            print(f'------Unauthourization, response status: {response.status}------\n')
            time.sleep(600)
            return None
        
        # print(response.status) 测试用
        try:
            jsonresponse = json.loads(response.text)
            users = jsonresponse['items']
            if users == 'error': 
                print('user info parse failed')
                return None
        except Exception as e:
            print(e, response)   
            return None

        for user in users:
            user_url = user['url']
            repo_url = user['repos_url']

            yield scrapy.Request(
                url=repo_url, 
                headers=headers,
                callback=self.CountRepoInfo,
                meta={'user_url': user_url}
                )

    def CountRepoInfo(self, response):
        if response.status != 200:
            print(f'------failed on CountRepoInfo, response status: {response.status}------\n')
            return None

        languages_details = []
        try:
            jsonresponse = json.loads(response.text)
            error = jsonresponse['message']
            print(error)
            # print('wait 10 min to restart')
            return None

        except:
            languages = []
            for res in jsonresponse:
                fork = res.get('fork')
                language = res.get("language")
                if language and not fork:
                    languages.append(language)
            
            res = Counter(languages)
            res = res.most_common()
            details = []

            for detail in res:
                language_dict = {detail[0]: detail[1]}
                details.append(language_dict)

            languages_details.append(details)

            # 向数据库中输入数据(去重处理, set类型)
            user_url = response.meta['user_url']
            if self.r.sadd('user_url',  user_url):
                yield scrapy.Request(
                    url=user_url, 
                    headers=headers2,
                    callback=self.UserInfo,
                    meta={
                        'language_count': json.dumps({'language_details': languages_details})
                    })
            else:
                return None

    def UserInfo(self, response):
        language_details = response.meta['language_count']
        try:
            user = json.loads(response.text)
        except Exception as e:
            print(e, response)
            user = None
            return user
            
        if user:
            item = {
                'username' : user['login'],
                'gitUrl' : user['html_url'],
                'name' : user['name'],
                'company' : user['company'],
                'blog' : user['blog'],
                'email' : user['email'],
                'location' : user['location'],
                'hireable' : user['hireable'],
                'image' : user['avatar_url'],
                'update_time' : user['updated_at'],
                'followers' : user['followers'],
                'following' : user['following'],
                'languages_detail': language_details
            }
            # 过滤掉none
            keys = list(filter(lambda x: True if item[x] else False, item))
            yield {k :item[k] for k in keys}

        else:
            return None

        


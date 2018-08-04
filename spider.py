import requests
from urllib.parse import urlencode
import json
from bs4 import BeautifulSoup as bs
from analog_landing import *


class Spider():
    def __init__(self, session=None, proxy=None):
        self.query_string = {
            'px': 'default',
            'city': '成都',
            #'needAddtionalResult': 'false'
        }
        self.form_data = {
            'pn': '1',
            'kd': 'python'
        }
        self.headers = {
            'Accept-Encoding': 'gzip,deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Proxy-Authorization': proxy,
            'Connection': 'keep-alive',
            'Host': 'wwww.lagou.com',
            'Origin': 'https://www.lagou.com',
            'User-Agent': 'Mozilla/5.0(X11;Linuxx86_64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/68.0.3440.75Safari/537.36'
        }
        self.session = requests.session()
        self.url_json = 'http://www.lagou.com/jobs/positionAjax.json?'
        self.url_referer = 'https://www.lagou.com/jobs/list_python?'
        self.url_referer = self.url_referer + urlencode(self.query_string)

    def download_id(self):
        header = self.headers.copy()
        url_json = self.url_json + urlencode(self.query_string)

        header['Referer'] = self.url_referer
        header['X-Requested-With'] = 'XMLHttpRequest'
        response = self.session.post(url_json, data=self.form_data, headers=header, allow_redirects=False)
        print(response.text)
        content = json.loads(response.text)
        for i in range(15):
            id = content['content']['positionResult']['result'][i]['positionId']

            print(id)
            return id

    def download_message(self, id):
        url = 'https://www.lagou.com/jobs/'+str(id)+'.html'
        header = self.headers.copy()
        header['Referer'] = self.url_referer
        response = self.session.get(url, headers=header, allow_redirects=False)
        return response.text

    def parse(self, html):
        print(html)
        soup = bs(html, 'lxml')
        lis = soup.select('.position-content .job_request span')
        print(lis)
        list = []
        for li in lis:
            list.append(li.text())
        message = {
            'company': soup.select('.position-content .job_name .company').get_text(),
            'job_name': soup.select('.position-content .job-name .name').get_text(),
            'job_request': list,
            'advantage': soup.select('.job_detail .job_advantage p').get_text(),
            'describe': soup.select('#job_detail dd.job_bt div p').get_text(),
            'location': soup.select('#job_detail > dd.job-address.clearfix > div.work_addr').get_text(),
        }
        return message


if __name__ == '__main__':
    proxy = Proxy().get_proxy()
    print(proxy)
    logger = Login(proxy)
    #message = logger.login('18328592041', 'w001~why')
    #logger.get_ticket()
    #session = logger.session
    spider = Spider(proxy=proxy)
    id = spider.download_id()
    html = spider.download_message(id)
    message = spider.parse(html)
    print(message)

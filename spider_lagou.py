import requests
import re
from pyquery import PyQuery as pq
from hashlib import md5
import time
from urllib.parse import urlencode
import base64
from requests.adapters import HTTPAdapter
from http import cookiejar
from multiprocessing import Pool
import json
import pymongo
import random


class Login(object):
    def __init__(self):
        # 设置 session
        self.session = requests.Session()
        self.session.mount('http://', HTTPAdapter(max_retries=5))
        self.session.mount('https://', HTTPAdapter(max_retries=5))
        self.session.cookies = cookiejar.LWPCookieJar(filename='LagouCookies')
        self.headers = {
            'Referer': 'https://passport.lagou.com/login/login.html',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0',
        }
        # 设置代理
        self.proxyHost = "http-pro.abuyun.com"
        self.proxyPort = "9010"
        self.proxyUser = 'HV2C3723AY29332P'
        self.proxyPass = '9FB6F91747CABE83'
        self.proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": self.proxyHost,
            "port": self.proxyPort,
            "user": self.proxyUser,
            "pass": self.proxyPass,
        }

        self.proxies = {
            "http": self.proxyMeta,
            "https": self.proxyMeta,
        }
        # 设置mongodb
        self.client = pymongo.MongoClient('localhost')
        self.db = self.client['jobs']
        self.db['lagou_jobs'].create_index('url', unique=True)

    # 获取表单隐藏参数
    def get_token_code(self):
        url = 'https://passport.lagou.com/login/login.html'
        header = self.headers.copy()
        data = self.session.get(url, headers=header)
        match = re.match(r'.*X_Anti_Forge_Token = \'(.*?)\';.*X_Anti_Forge_Code = \'(\d+?)\'', data.text, re.S)
        if match:
            Forge_Token = match.group(1)
            Forge_Code = match.group(2)
        return Forge_Token, Forge_Code

    # 对密码加密
    def encryptPwd(self, password):
        # 对密码的双重加密
        password = md5(password.encode('utf-8')).hexdigest()
        password = 'veenike' + password + 'veenike'
        password = md5(password.encode('utf-8')).hexdigest()
        return password

    # 登陆
    def login(self, user, passwd):
        login_url = 'https://passport.lagou.com/login/login.json'
        postdata = {
            'isValidate': 'true',
            'username': user,
            'password': self.encryptPwd(passwd),
            'request_form_verifyCode': '',
            'submit': '',
        }
        X_Anti_Forge_Token, X_Anti_Forge_Code = self.get_token_code()
        header = self.headers.copy()
        header.update({
            'X-Requested-With': 'XMLHttpRequest',
            'X-Anit-Forge-Token': X_Anti_Forge_Token,
            'X-Anit-Forge-Code': X_Anti_Forge_Code,
        })
        print(header)
        response = self.session.post(login_url, headers=header, data=postdata)
        print(response.text)
        result = json.loads(response.text)
        if result['message'] == '操作成功':
            print('登陆成功')
            self.session.cookies.save()
            return True
        else:
            print('失败')
            return False

    # 检查是否已有cookies
    def get_cookies(self):
        try:
            self.session.cookies.load('LagouCookies', ignore_discard=True)
            return True
        except:
            print('cookie 未保存或过期')
            return False

    # 下载程序汇总
    def download(self, n):
        query_string = {
            'px': 'default',
            'city': '成都',
            'needAddtionalResult': 'false'
        }
        query_string_refer = {
            'px': 'default',
            'city': '成都',
        }
        form_data = {
            'first': 'false',
            'pn': n,
            'kd': 'python'
        }
        url_json = 'http://www.lagou.com/jobs/positionAjax.json?'
        url_referer = 'https://www.lagou.com/jobs/list_python?'
        url_referer = url_referer + urlencode(query_string_refer)
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.'
                          '3440.75 Safari/537.36',
            'Referer': url_referer,
            # 'X-Anit-Forge-Code': '0',
            # 'X-Anit-Forge-Token': 'None',
            'X-Requested-With': 'XMLHttpRequest',
        }
        url_json = url_json + urlencode(query_string)
        response = self.session.post(url_json, data=form_data, headers=headers, proxies=self.proxies)
        content = json.loads(response.text)
        num = content['content']['positionResult']['resultSize']
        # print(num)
        for i in range(int(num)):
            job_id = content['content']['positionResult']['result'][i]['positionId']
            print(job_id)
            time.sleep(1)
            html = self.download_message(job_id)
            message = self.parse(html)
            self.save_to_mongo(message)

    # 下载具体信息
    def download_message(self, id):
        job_url = 'https://www.lagou.com/jobs/' + str(id) + '.html'
        query_string_refer = {
            'px': 'default',
            'city': '成都',
        }
        url_referer = 'https://www.lagou.com/jobs/list_python?'
        url_referer = url_referer + urlencode(query_string_refer)
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'Host': 'www.lagou.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.'
                          '3440.75 Safari/537.36',
            'Referer': url_referer,
            }
        response = self.session.get(job_url, headers=headers, proxies=self.proxies)
        return response

    # 解析信息
    def parse(self, response):
        doc = pq(response.text)
        message = {
            'url': response.url,
            'company': doc('div.position-head div div div.job-name div.company').text(),
            'job_name': doc('div.position-head div div div.job-name span.name').text(),
            'job_request': doc('.position-content .job_request span').text(),
            'advantage': doc('#job_detail > dd.job-advantage').text(),
            'describe': doc('dl#job_detail > dd.job_bt > div > p').text(),
            'location': doc('#job_detail > dd.job-address.clearfix > div.work_addr').text(),
        }
        # print(message)
        return message

    '''将数据存储到mongodb'''
    def save_to_mongo(self, item):
        try:
            self.db['lagou_jobs'].insert_one(dict(item))
            print('存储到MongoDB', item)
            return True
        except pymongo.errors.DuplicateKeyError as e:
            print('错误为', e)
        return True


if __name__ == '__main__':
    s = Login()
    if not s.get_cookies():
        username = input('username:')
        password = input('password:')
        s.login(user, passwd)
    s.download(1)








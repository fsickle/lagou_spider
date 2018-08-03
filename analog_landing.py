import requests
from bs4 import BeautifulSoup as bs
import re
import json
from hashlib import md5
import time
from urllib.parse import urlencode

class Login():
    def __init__(self):
        self.session = requests.session()
        self.headers = {
            'Accept-Encoding': 'gzip,deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'passport.lagou.com',
            'Referer': 'https://www.lagou.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0(X11;Linuxx86_64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/68.0.3440.75Safari/537.36'
        }

    def get_token_code(self):
        url = 'https://passport.lagou.com/login/login.html'
        # query_string = {
        #     'ts': '1533271595716',
        #     'signature': 'F9415BF569085BC9A80B86B4724959C7',
        # }
        # url = url + urlencode(query_string)
        data = self.session.get(url, headers=self.headers)
        soup = bs(data.text, 'lxml')
        '''
        </script>

            <!-- 页面样式 -->    <!-- 动态token，防御伪造请求，重复提交 -->
            <script>
            window.X_Anti_Forge_Token = '13e316e1-8910-4da9-85c2-7e31fe1225b0';
            window.X_Anti_Forge_Code = '44622791';
        </script>
        '''

        anti = soup.find_all('script')[1].string
        anti_token = {'X_Anti_Forge_Token': 'None',
                      'X_Anti_Forge_Code': '0'}
        anti_token['X_Anti_Forge_Token'] = re.findall(r'= \'(.+?)\'', anti)[0]
        anti_token['X_Anti_Forge_Code'] = re.findall(r'= \'(.+?)\'', anti)[1]
        return anti_token

    def encryptPwd(self, password):
        # 对密码的双重加密
        password = md5(password.encode('utf-8')).hexdigest()
        password = 'veenike' + password + 'veenike'
        password = md5(password.encode('utf-8')).hexdigest()
        return password

    def get_Captcha(self):
        pass

    def login(self, user, passwd, captchaData=None, token_code=None):
        url = 'https://passport.lagou.com/login/login.json'
        passwd = self.encryptPwd(passwd)
        postdata = {
            'isValidate': 'true',
            'username': user,
            'password': passwd,
            'request_form_verifyCode': (captchaData if captchaData!=None else ''),
            'submit': '',
        }
        token_code = self.get_token_code() if token_code is None else token_code
        header = {
            'Accept-Encoding': 'gzip,deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Origin': 'https://passport.lagou.com',
            'Host': 'passport.lagou.com',
            'Referer': 'https://passport.lagou.com/login/login.html',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0(X11;Linuxx86_64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/68.0.3440.75Safari/537.36'
        }

        header.update(token_code)
        #print(header)
        #print('ok')
        response = self.session.post(url, headers=header, data=postdata)
        data = json.loads(response.content.decode('utf-8'))
        print(data)

        if data['state'] == 1:
            return response.content
        elif data['state'] == 10010:
            print(data['message'])
            #captchaData = self.getCaptcha()
            token_code = {'X_Anti_Forge_Token': data['submitToken'],
                      'X_Anti_Forge_Code': data['submitCode']}
            return self.login(username, password, captchaData, token_code)
        else:
            print(data['message'])
            return False

    def get_cookie(self):
        return requests.utils.dict_from_cookiejar(self.session.cookies)

    def get_ticket(self):
        #两个重定向
        url = 'https://passport.lagou.com/grantServiceTicket/grant.html'
        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'passport.lagou.com',
            'Referer': 'https://passport.lagou.com/login/login.html',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
        }
        response = self.session.get(url, headers=headers)

        redir_url = response.next.url
        print(redir_url)
        url = re.sub('http:', 'https:', redir_url)

        headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'www.lagou.com',
            'Referer': 'https://passport.lagou.com/login/login.html',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
        }
        response = self.session.get(url, headers=headers)
        print(response.status_code)
        cookies = self.get_cookie()
        print(cookies)
        with open('cookie_requests.txt', 'w') as f:
            f.write(str(cookies))











if __name__ == '__main__':
    s = Login()
    a = s.get_token_code()
    username = input('username:')
    password = input('password:')
    s.login(username, password, token_code=a)
    # s = s.get_cookie()
    # print(s)
    # with open('cookie_requests.txt', 'w') as f:
    #     f.write(str(s))





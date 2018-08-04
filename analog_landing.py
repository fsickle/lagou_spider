import requests
from bs4 import BeautifulSoup as bs
import re
import json
from hashlib import md5
import time
from urllib.parse import urlencode
import base64


class Proxy():
    def get_proxy(self):
        '''
        使用的讯代理，得到Proxy
        :return: proxy
        '''
        # 代理服务器
        # proxyHost = "http-dyn.abuyun.com"
        # proxyPort = "9020"
        #
        # # 代理隧道验证信息
        # proxyUser = "H74274906A74PP2D"
        # proxyPass = "EA516E778B9E0A75"
        #
        # proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        #     "host": proxyHost,
        #     "port": proxyPort,
        #     "user": proxyUser,
        #     "pass": proxyPass,
        # }
        #
        # proxies = {
        #     "http": proxyMeta,
        #     "https": proxyMeta,
        # }
        proxyUser = ''
        proxyPass = ''
        end = proxyUser + ":" + proxyPass
        a = base64.b64encode(end.encode('utf-8')).decode('utf-8')
        proxy = "Basic " + a
        return proxy


class Login(object):
    def __init__(self, proxy=None):
        self.session = requests.session()
        self.headers = {
            'Proxy-Authorization': proxy,
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://passport.lagou.com/login/login.html',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
        }
        # self.proxies = proxy

    def get_token_code(self):
        url = 'https://passport.lagou.com/login/login.html'
        print(self.headers)
        header = self.headers.copy()
        data = self.session.get(url, headers=header)
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
        anti_token = {
            'X_Anti_Forge_Token': 'None',
            'X_Anti_Forge_Code': '0'
        }
        anti_token['X_Anti_Forge_Token'] = re.findall(r'= \'(.+?)\'', anti)[0]
        anti_token['X_Anti_Forge_Code'] = re.findall(r'= \'(.+?)\'', anti)[1]
        print(anti_token)
        return anti_token

    def encryptPwd(self, password):
        # 对密码的双重加密
        password = md5(password.encode('utf-8')).hexdigest()
        password = 'veenike' + password + 'veenike'
        password = md5(password.encode('utf-8')).hexdigest()
        return password

    def get_Captcha(self):
        pass

    def login(self, user, passwd):
        url = 'https://passport.lagou.com/login/login.json'
        passwd = self.encryptPwd(passwd)
        postdata = {
            'isValidate': 'true',
            'username': user,
            'password': passwd,
            'request_form_verifyCode': '',
            'submit': '',
        }
        token_code = self.get_token_code()
        header = self.headers.copy()
        header.update(token_code)
        print(header)
        response = self.session.post(url, headers=header, data=postdata)
        print(response.status_code)
        print(response.text)

        # if data['state'] == 1:
        #     return response.content
        # elif data['state'] == 10010:
        #     print(data['message'])
        #     #captchaData = self.getCaptcha()
        #     token_code = {'X_Anti_Forge_Token': data['submitToken'],
        #               'X_Anti_Forge_Code': data['submitCode']}
        #     return self.login(username, password, captchaData, token_code)
        # else:
        #     print(data['message'])
        #     return False

    def get_cookie(self):
        return requests.utils.dict_from_cookiejar(self.session.cookies)

    def get_ticket(self):
        #两个重定向
        url = 'https://passport.lagou.com/grantServiceTicket/grant.html'
        header = self.headers.copy()
        header['Referer'] = 'https://passport.lagou.com/login/login.html'
        response = self.session.get(url, headers=header, allow_redirects=False)

        redir_url = response.next.url
        print(redir_url)
        url = re.sub('http:', 'https:', redir_url)
        response = self.session.get(url, headers=header, allow_redirects=False)
        print(response.status_code)
        cookies = self.get_cookie()
        print(cookies)
        with open('cookie_requests.txt', 'w') as f:
            f.write(str(cookies))


if __name__ == '__main__':
    proxy = Proxy().get_proxy()
    s = Login(proxy)
    username = 18328592041 #input('username:')
    password = 'w001~why' #input('password:')
    data = s.login(username, password)
    if data:
        print(data)
        print('登录成功')
    else:
        print('登录不成功')






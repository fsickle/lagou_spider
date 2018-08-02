import requests
from urllib.parse import urlencode
import json

class Download_id():
    query_string = {
        'px': 'default',
        'city': '成都',
        'needAddtionalResult': 'false'
    }
    form_data = {
        'pn': '1',
        'kd': 'python'
    }
    cookies = {
        'JSESSIONID': 'ABAAABAAAGGABCB93C3C3FF7A758D774AA3A561151DE137',
        'SEARCH_ID': 'dad3b6a16b774c2e8d6e86bcdd7b1da9',
        'user_trace_token': '20180802150401-8c175326-f489-470c-a0f1-af016d2c97dd',
    }
    url_json = 'http://www.lagou.com/jobs/positionAjax.json?'
    url_json = url_json + urlencode(query_string)
    url_referer = 'https://www.lagou.com/jobs/list_python?'
    url_referer = url_referer + urlencode(query_string)

    def download(self):
        session = requests.session()
        session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
        session.headers['Referer'] = self.url_referer
        response = session.post(self.url_json, cookies=self.cookies, data=self.form_data)

        content = json.loads(response.text)
        for i in range(15):
            id = content['content']['positionResult']['result'][i]['positionId']
            print(id)

if __name__ == '__main__':
    s = Download_id()
    s.download()
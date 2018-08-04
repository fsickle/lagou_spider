import requests, base64

proxyUser = 'H74274906A74PP2D'
proxyPass = 'EA516E778B9E0A7'
end = proxyUser+":"+proxyPass
a = base64.b64encode(end.encode('utf-8')).decode('utf-8')
proxy = "Basic " + a
headers = {
    'Proxy-Authorization': proxy,
    'Cookie': 'user_trace_token=20180804153428-5cea1239-f0b1-4b8d-a18c-c414b2bd63ca; X_HTTP_TOKEN=d460278d7185bb2f1dbd92c8eb6d17ca; LGUID=20180804153428-d20f1f63-97b8-11e8-a339-5254005c3644; _ga=GA1.2.1421538324.1533368121; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533273154,1533276565,1533365755,1533368121; index_location_city=%E5%85%A8%E5%9B%BD; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=7; TG-TRACK-CODE=jobs_code; PRE_UTM=; PRE_HOST=; LGSID=20180804162634-18d2e7c7-97c0-11e8-a339-5254005c3644; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%3Fcity%3D%25E5%2585%25A8%25E5%259B%25BD%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%3Fpx%3Ddefault%26city%3D%25E6%2588%2590%25E9%2583%25BD; login=false; unick=""; _putrc=""; LG_LOGIN_USER_ID=""; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533371323; LGRID=20180804162843-65c3c5a2-97c0-11e8-a339-5254005c3644; SEARCH_ID=ee35e6671831464695b4820cd4ffa1cc',
    'Host': 'wwww.lagou.com',
    'User-Agent': 'Mozilla/5.0(X11;Linuxx86_64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/68.0.3440.75Safari/537.36'
}


r = requests.get('https://www.lagou.com/jobs/4011458.html', headers=headers)
print(r.text)
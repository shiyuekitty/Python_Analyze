import requests
import urllib
import time
import json

# url = 'https://dujia.qunar.com/golfz/visa/visa_deals_places'
url='https://touch.dujia.qunar.com/depCities.qunar'
proxies = {
    # 'https': 'https://183.129.207.73:14823',
    'http:': 'http://61.135.217.7:80'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36'
}

strhtml = requests.get(url=url, headers=headers, proxies=proxies)
dep_dict = strhtml.json()
for dep_item in dep_dict['data']:
    for dep in dep_dict['data'][dep_item]:
        a = []
        print(dep)
        url = 'https://touch.dujia.qunar.com/golfz/sight/arriveRecommend?dep={}&exclude=&extensionImg=255,175'.format(
            urllib.request.quote(dep))
        time.sleep(1)
        strhtml = requests.get(url=url, headers=headers, proxies=proxies)
        arrive_dict = strhtml.json()
        for arr_item in arrive_dict['data']:
            for arr_item_1 in arr_item['subModules']:
                for query in arr_item_1['items']:
                    if query['query'] not in a:
                        a.append(query['query'])
        print(a)

from bs4 import BeautifulSoup
import requests
import re
import time

url = 'http://www.cntour.cn/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}

# proxies = {
#     'http': 'http://10.10.1.10:3128',
#     'https': 'http://10.10.1.10:1080'
# }
strhtml = requests.get(url, headers=headers)
soup = BeautifulSoup(strhtml.text, 'lxml')
data = soup.select('#main > div > div.mtop.firstMod.clearfix > div.leftBox > div > ul > li > a')

for item in data:
    result = {
        'title': item.get_text(),
        'link': item.get('href'),
        'ID': re.findall(r'\d+', item.get('href'))
    }
    time.sleep(3)
    print(result)

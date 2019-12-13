from urllib import request
import os
import time
import random
import re
import requests
from lxml import etree
ua_list=[
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

class MeiziSpider():
    def __init__(self):
        self.url = 'https://www.mzitu.com/all/'

    def get_html(self, url):
        headers = {'User-Agent': random.choice(ua_list)}
        req = request.Request(url=url, headers=headers)
        res = request.urlopen(req)
        html = res.read()
        return html
        # print(html)

    def re_func(self, re_bds, html):
        pattern = re.compile(re_bds, re.S)
        r_list = pattern.findall(html)
        return r_list

    # 获取想要的数据 - 解析一级页面
    # def parse_html(self, url):
    #     one_html = self.get_html(url).decode()
    #     # print(one_html)
    #     re_bds = '<p class="url">.*?<a href="(.*?)" target="_blank">(.*?)</a>'
    #     one_list = self.re_func(re_bds, one_html)
    #     # print(one_list)
    #     # time.sleep(random.randint(1, 3))
    #     self.write_html(one_list)

    def parse_html(self, url):
        html = self.get_html(url).decode()
        parse_obj = etree.HTML(html)
        href_list = parse_obj.xpath('//div[@class="all"]/ul[@class="archives"]/li/p[@class="url"]/a/@href')
        print("href_list:", href_list)
        self.write_html(href_list)

    def write_html(self, href_list):
        for href in href_list:
            two_url = href
            print(two_url)
            time.sleep(random.randint(1, 3))
            self.save_image(two_url)

    def save_image(self, two_url):
        headers = {'Referer': two_url, 'User-Agent': random.choice(ua_list)}
        print('---------two_url-----------', two_url)
        # 向图片链接发请求.得到bytes类型
        i = 0
        while True:
            try:
                img_link = two_url + '/{}'.format(i)
                print("img_link:", img_link)
                html = requests.get(url=img_link, headers=headers).text
                re_bds = ' <div class="main-image"><p><a href="https://www.mzitu.com/.*?" ><img ' \
                         'src="(.*?)" alt="(.*?)" width=".*?" height=".*?" /></a></p>'
                img_html_list = self.re_func(re_bds, html)
                print("img_html_list", img_html_list)
                name = img_html_list[0][1]
                print("-----name:", name)
                direc = 'G:/shiyue/picture/meizi/{}/'.format(name)
                print("direc:", direc)
                if not os.path.exists(direc):
                    os.makedirs(direc)
                img_ = requests.get(url=img_html_list[0][0], headers=headers).content
                filename = direc + name + img_link.split('/')[-1] + '.jpg'
                # print("img_:",img_)
                with open('G:/shiyue/picture/meizi/', 'wb') as f:
                    f.write(img_)
                i += 1
            except Exception as e:
                break


if __name__ == '__main__':
    spider = MeiziSpider()
    spider.parse_html('https://www.mzitu.com/all')

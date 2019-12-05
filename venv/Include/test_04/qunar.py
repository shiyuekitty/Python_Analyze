import requests
import urllib.request
import time
import pymongo
from multiprocessing import Pool

client = pymongo.MongoClient('mongodb://root:123456@localhost:27017/admin')
book_qunar = client['qunar']
sheet_qunar = book_qunar['sheet_qunar_zyx']


def get_list(dep, item):
    url = 'https://touch.dujia.qunar.com/list?modules=list%2CbookingInfo%2CactivityDetail&dep={}&query={}&dappDealTrace=true&mobFunction=%E6%89%A9%E5%B1%95%E8%87%AA%E7%94%B1%E8%A1%8C&cfrom=zyx&it=dujia_hy_destination&date=&needNoResult=true&originalquery={}&limit=0,28&includeAD=true&qsact=search'.format(
        urllib.request.quote(dep), urllib.request.quote(item), urllib.request.quote(item))
    strhtml = get_json(url)
    result = {
        'date': time.strftime('%Y-%m-%d', time.localtime(time.time())),
        'dep': dep,
        'arrive': item,
        'result': strhtml
    }
    print(result)
    sheet_qunar.insert_one(result)


cookies = {
    'cookies': 'QN1=0000280007581c8322f0530d; QN48=tc_86d899c63c1c6179_16e9b0ca0b7_dc00; _RDG=28651ef2d05ab6231107018166f8c71cba; _RF1=221.194.139.113; _RGUID=0a5e4705-ae73-4934-977d-61d1e120d29d; _RSG=qaqSkMmHUf0TAD8X7TOzT9; QN99=8845; QN300=qunar; QunarGlobal=10.86.213.151_-4f4ecca6_16e9b085213_-2b50|1574559345327; _i=RBTKS9LVdoUQsd2x6kg75YolHExx; QN621=fr%3Dmobile; QN269=383195910CE111EAACA9FA163E189E8B; QN601=baf20d6b414683b2590740bc48cdb5b8; fid=4379b53a-f072-4611-975d-e508f8b53bc0; quinn=a1cc3ce9568ba1f37d0d41ddc14c88681d100305fd1472bd805350c78028fdc8eab70ba07748d6f05a0e26a40604b28a; __utma=183398822.847300900.1574561064.1574561064.1574561064.1; __utmz=183398822.1574561064.1.1.utmcsr=dujia.qunar.com|utmccn=(referral)|utmcmd=referral|utmcct=/pd/index_%E9%98%BF%E5%9D%9D%E5%B7%9E; QN100=WyLkuInkupp8Il0%3D; QN277=organic; QN163=0; QN205=qunar; QN25=5bf0bf6b-5f91-401c-9eb3-c742bb6398d9-9f992f90; QN42=cayh0538; _q=U.ojatqil0828; _t=26499263; csrfToken=BwnVB6L4wiviu4wywHcoxjdPCtfjnbDb; _s=s_A5LESRU5S3ICBLBG4EDG77EM7I; _v=MzHfZdZyk293_ZUFEwl1F1lZoeCBrOlWZ3a5TmP7qb5xCXIlVvnvBHKu4NFdpHJxVTgEitVMCTVjkI1f6ihUsyjqAD0BvMqZokLz9EkTivrbrAPQo7upWt0OeFqsi0uAWDaesTwoSTrkIVCTvBZQvV_cqMG8KO20IfSKKLTE_zsy; QN44=ojatqil0828; JSESSIONID=6EED4AD41E9C118FD643D1695F31E44A; QN271=6e0c4fc9-2e73-4bce-88f3-3c45c67961dd; QN267=07149993998be2f998; _vi=5vZZ5Np1xAN3zzlWrNbRqRQOsvEY08aaDYGFtqCQcK-RIOEXfTW68wM9KN-NFr8oLp798iyCzIY943sLXigg17rmOvKDqr-iDHNn9t5l_aj-LPHqCFM-kifwF0Rp-u4hCIbVRcSby9WJleZnTjDK30PC1PQ9prQP3wQ17goRU7L8'}


def get_json(url):
    strhtml = requests.get(url=url, cookies=cookies)
    time.sleep(1)
    return strhtml.json()


def get_all_data(dep):
    a = []
    url = 'https://touch.dujia.qunar.com/golfz/sight/arriveRecommend?dep={}&exclude=&extensionImg=255,175'.format(
        urllib.request.quote(dep))  # urllib.request.quote()解决中文编码问题
    arrive_dict = get_json(url)
    for arr_item in arrive_dict['data']:
        for arr_item_1 in arr_item['subModules']:
            for query in arr_item_1['items']:
                if query['query'] not in a:
                    a.append(query['query'])
    for item in a:
        get_list(dep, item)


dep_list = '''
澳门
阿坝州
阿克苏地区
阿拉尔
阿拉善盟
阿勒泰
阿里
安康
安庆
鞍山
安顺
安阳
北京
白城
百色
白沙
白山
白银
保定
宝鸡
保山
保亭
包头
南阳
那曲
内江
宁波
宁德
怒江
商丘
上饶
山南
汕头
汕尾
韶关
绍兴
邵阳
神农架
深圳
石河子
十堰
石嘴山
珠海
驻马店
株洲
淄博
自贡
资阳
遵义
'''
if __name__ == '__main__':
    pool = Pool()
    pool.map(get_all_data, dep_list.split())
import requests
import time
import pymongo

client = pymongo.MongoClient('mongodb://root:123456@localhost:27017/admin')  # 建立连接
book_weather = client['weather']  # 新建weather数据库
sheet_weather = book_weather['sheet_weather_3']  # 在weather库中新建sheet_weather_3表
with open('E:/projects/pyprogram_text/Pycharm_Code/Analyze/venv/Include/Scrapy_Code/outcity.txt', 'r')as f:
    list = f.readlines()
for i in range(2):
    list.remove(list[0])
for item in list:
    print(item[0:12])
    url = 'https://free-api.heweather.net/s6/weather?location=' + item[0:12] + '&key=5ce6464c17824a6ea9aa12dd749e2bc5'
    strhtml = requests.get(url)
    strhtml.encoding = 'utf-8'
    time.sleep(1)
    dic = strhtml.json()
    sheet_weather.insert_one(dic)


#查询
# client = pymongo.MongoClient('mongodb://root:123456@localhost:27017/admin')
# book_weather = client['weather']
# sheet_weather = book_weather['sheet_weather_3']
# for item in sheet_weather.find({'HeWeather6.basic.location': '天津'}):
#     print(item)
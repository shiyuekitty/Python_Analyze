import requests
import time

url = 'https://a.hecdn.net/download/dev/china-city-list.csv'

strhtml = requests.get(url=url)
strhtml.encoding = 'utf8'
time.sleep(1)
data = strhtml.text
datal = data.split('\n')

for i in range(3):
    datal.remove(datal[0])

url = 'https://free-api.heweather.net/s6/weather/forecast?key=cc33b9a52d6e48de852477798980b76e&location=CN101090101'
strhtml = requests.get(url)
dict = strhtml.json()
weather_t = []
for item in dict["HeWeather6"][0]['daily_forecast'][1:2]:
    weather = {
        '城市名': dict["HeWeather6"][0]['basic']['location'],
        '日期': item['date'],
        '白天': item['cond_txt_d'],
        '夜间': item['cond_txt_n']
    }
    weather_t.append(weather)
print(weather_t)

# for item in datal[:20]:
#     url = 'https://free-api.heweather.net/s6/weather/forecast?key=cc33b9a52d6e48de852477798980b76e&location=' + item[
#                                                                                                                 0:11]
#     strhtml = requests.get(url)
#     dict = strhtml.json()
#     weather_t = []
#     for item in dict["HeWeather6"][0]['daily_forecast'][1:2]:
#         weather = {
#             '城市名': dict["HeWeather6"][0]['basic']['location'],
#             '今天日期': dict["HeWeather6"][0]['daily_forecast'][0]['date'],
#             'utc': dict["HeWeather6"][0]['daily_forecast'][0]['mr'],
#             'loc': dict["HeWeather6"][0]['daily_forecast'][0]['ms'],
#             '明天日期': item['date'],
#             '白天': item['cond_txt_d'],
#             '夜间': item['cond_txt_n']
#         }
#         weather_t.append(weather)
#     print(weather_t)

# C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe
import requests
import urllib
import time
import random
from selenium.webdriver.common.by import By
import requests, urllib.request, time, random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_url(url):
    time.sleep(2)
    return (requests.get(url))


if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver")
    # driver = webdriver.Firefox()
    url = 'https://m.dujia.qunar.com/depCities.qunar'
    strhtml = get_url(url)
    dep_dict = strhtml.json()
    a = []
    for dep_item in dep_dict['data']:
        for dep in dep_dict['data'][dep_item]:
            a.append(dep)
    for dep_1 in a[1:]:
        strhtml = get_url(
            'https://m.dujia.qunar.com/golfz/sight/arriveRecommend?dep={}&exclude=&extensionImg=255,175'.format(
                urllib.request.quote(dep_1)))
        arrive_dict = strhtml.json()
        for arr_item in arrive_dict['data']:
            for arr_item_1 in arr_item['subModules']:
                for query in arr_item_1['items']:
                    driver.get('https://fh.dujia.qunar.com/?tf=package')
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "depCity")))
                    driver.find_element_by_xpath('//*[@id="depCity"]').clear()
                    driver.find_element_by_xpath('//*[@id="depCity"]').send_keys(dep_1)
                    driver.find_element_by_xpath('//*[@id="arrCity"]').send_keys(query['query'])
                    driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[3]/div/div[2]/div/a').click()
                    print('dep:%s arr:%s' % (dep_1, query['query']))
                    for i in range(100):
                        time.sleep(random.uniform(5, 6))
                        wrong = driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[6]/div[2]/div')
                        if wrong == []:
                            break
                        routes = driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[6]/div[2]/div')
                        for route in routes:
                            result = {
                                'date': time.strftime('%Y-%m-%d', time.localtime(time.time())),
                                'dep': dep_1,
                                'arrive': query['query'],
                                'result': route.text
                            }
                            print(result)
                        if i < 1:
                            btns = driver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[7]/div/div/a')
                            for a in btns:
                                if a.text == u"下一页":
                                    a.click()
                                    break
                        else:
                            break
    driver.close()
    exit()

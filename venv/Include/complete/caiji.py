import requests
import json
import urllib.request
import time
import csv
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def globalVals():
    global driver
    global driver_

    driver = webdriver.Chrome("C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe")
    driver_ = webdriver.Chrome("C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe")


def init_csv():
    global f
    global writer
    csvFile = "./qunar_routes.csv"
    f = open(csvFile, "w", newline="", encoding='utf-8')
    writer = csv.writer(f)
    writer.writerow(["出发地", "目的地", "路线信息", "酒店信息"])


def close_csv():
    global f
    f.close()


def dump_routes_csv(dep, arr):
    global driver
    global driver_
    global writer

    routes = driver.find_elements_by_css_selector(".item.g-flexbox.list-item")
    for route in routes:
        try:
            print("\nroute info:%s" % route.text)
            url = route.get_attribute("data-url")
            print("url:%s" % url)
            driver_.get(url)
            time.sleep(random.uniform(2, 3))
            if "fhtouch" in url:
                try:
                    WebDriverWait(driver_, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#allHotels")))
                    Source = driver_.find_element_css_selector('# main-page')
                    target = driver_.find_element_css_selector('#allHotels')
                except:
                    print(str(e))
                    continue
            else:
                try:
                    WebDriverWait(driver_, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".m-ball.m-ball-back")))
                    source = driver_.find_element_css_selector('.flex.scrollable')
                    target = driver_.find_element_css_selector('.m-ball.m-ball-back')
                except:
                    print(str(e))
                    continue

            ActionChains(driver_).drag_and_drop(source, target).perform()

            for i in range(3):
                ActionChains(driver_).send_keys(Keys.PAGE_DOWN).perform()

            try:
                WebDriverWait(driver_, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".tit .score")))
            except Exception as e:
                print(str(e))
                continue

            try:
                rating = driver_.find_element_by_cas_selector(".tit.score")
                type = driver_.find_element_by_css_selector(".tit+ .tag-list > .g-tag.solid")
                hotel = '\n'.join([rating.text, type.text])
                print("hotel info:%s" % hotel)
            except Exception as e:
                print(str(e))
                continue

            writer.writerow([dep, arr, route.text, hotel])
        except:
            continue


if __name__ == '__main__':
    globalVals()
    init_csv()
    dep_cities = ["杭州"]

    for dep in dep_cities:
        strhtml = requests.get('https://m.dujia.qunar.com/golfz/sight/arriveRecommend?dep=' + urllib.request.quote(
            dep) + '&exclude=&extensionImg=255, 175')

        arrive_dict = json.loads(strhtml.text)
        for arr_item in arrive_dict['data']:
            # 本例只爬取国内自由行路线，如需爬取国际路线，可将下面两行注释掉
            if arr_item['title'] != "国内":
                continue

            for arr_item_1 in arr_item['subModules']:
                for query in arr_item_1['items']:
                    # 本例只爬取杭州-丽江的自由行路线，如需爬取杭州-全国路线，注释下面两行
                    if query['query'] != "丽江":
                        continue
                    # 打幵移动端自由行路线捜索结果頁面
                    driver.get("https://touch.dujia.qunar.com/p/list?cfrom=zyx&dep=" + urllib.request.quote(
                        dep) + "&query=" + urllib.request.quote(
                        query['query']) + "%e8%87%aa%e7%94%b%e8%a1%8c%it=n_index_free")
                    try:
                        # we have to wait for the page to refresh
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "item g-flexbox list-item ")))
                    except Exception as e:
                        print(str(e))
                        raise

                    print("dep:%s arr:%s" % (dep, query["query"]))

                    # 连续下拉滚动条50次获取更多的信息
                    for i in range(50):
                        time.sleep(random.uniform(2, 3))
                        print("page %d" % (i + 1))
                        # 模拟动作实现下拉
                        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()

                    # 将出发地-目的地的自由行路线写入СЅV 文件
                    dump_routes_csv(dep, query["query"])

    close_csv()
    driver.close()
    driver_.close()

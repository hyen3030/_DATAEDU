from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep

import requests
import pandas as pd
import datetime
import time
import csv
import sys

# python 제공 라이브러리
import feedparser
from newspaper import Config, Article, Source
import datetime
import datetime as dt
from datetime import timedelta

url = 'http://www.kbsm.net'
header = {'User-Agent': ''}
d = webdriver.Chrome('./chromedriver.exe')
d.set_window_position(0, 0)
d.set_window_size(1920, 1080)
d.implicitly_wait(3)
d.get(url)

today = dt.datetime.now().strftime("%Y%m%d")
today = datetime.datetime(int(today[0:4]), int(today[4:6]), int(today[6:8]))

# 1일전
before_1 = (today - timedelta(days=1)).strftime("%Y%m%d")
before_1 = datetime.datetime(int(before_1[0:4]), int(before_1[4:6]), int(before_1[6:8]))

current_date = datetime.date.today()

# - Config - #
c = Config()
c.keep_article_html = False

# - Source - #
s = Source(url, config=c)
# 페이지 다운로드 및 파싱
s.build()
link = s.articles

# - Article - #
a = Article(url, language='ko')
a.download()
a.parse()

print(a.title)
print(a.text)

formatted_date = current_date.strftime('%Y-%m-%d')

column_names = ["지역명", "기사제목", "기자이름", "날짜", "내용", "링크"]

csv_path = "./kbsm_230602_dgkb.csv"

with open(csv_path, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(column_names)

for jynews_num in range(1, 26):
    xpath_kbarea = f'/html/body/div[2]/header/div[2]/div[3]/div[1]/nav/ul/li[2]/div/div/div/div/div[2]/ul/li[{jynews_num}]/a'
    element = d.find_element(By.XPATH, xpath_kbarea)
    d.execute_script("arguments[0].click();", element)
    time.sleep(2)  # 2초 대기

    areaname = '/html/body/div[2]/div[4]/div/section/div/div[1]/div[1]/div/a/strong'
    area_element = d.find_element(By.XPATH, areaname)
    area = area_element.text
    print(area)

    d.refresh()  # 페이지 다시 로드
    time.sleep(2)  # 2초 대기

    for a_num in range(2, 12):
        xpath_numberarrow = f'/html/body/div[2]/div[4]/div/section/div/div[1]/div[2]/a[{a_num}]'
        time.sleep(1)
        d.find_element(By.XPATH, xpath_numberarrow).click()

        for jynews in range(1, 21):
            time.sleep(1)
            try:
                xpath_title = f'/html/body/div[2]/div[4]/div/section/div/div[1]/div[1]/ul/li[{jynews}]/a/div[2]/div[1]/strong'
                title_element = d.find_element(By.XPATH, xpath_title)
            except NoSuchElementException:
                xpath_title = f'/html/body/div[2]/div[4]/div/section/div/div[1]/div[1]/ul/li[{jynews}]/a/div/div[1]/strong'
                title_element = d.find_element(By.XPATH, xpath_title)
            d.find_element(By.XPATH, xpath_title).click()

            xpath_authors = f'/html/body/div[2]/div[3]/div[4]/div/section[1]/div/div/div[1]/div[3]/span[1]'
            authors = d.find_element(By.XPATH, xpath_authors).text
            print(authors)

            xpath_date_1 = '/html/body/div[2]/div[3]/div[4]/div/section[1]/div/div/div[1]/div[3]/span[3]'
            date = d.find_element(By.XPATH, xpath_date_1).text

            df = pd.DataFrame(columns=['지역명', '기사제목', '기자이름', '날짜', '내용', '링크'])
            df
            data = {
                '지역명': area,
                '기사제목': title_element.text,
                '기자이름': "경북신문 - " + authors,
                '날짜': formatted_date,
                '내용': a.text,
                '링크': a.url
            }
            df = df.append(data, ignore_index=True)
            df.to_csv("./kbsm_230602_dgkb.csv", mode='a', encoding='utf-8', header=False, index=False)
            len(df)

            print(area)
            print(title_element.text)
            print(authors)
            print(formatted_date)
            print(a.text)
            print(a.url)

            d.back()

        sleep(1)
        d.back()

    sleep(1)
    d.back()
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

import sys
import csv
import time
import codecs
import requests
import datetime
import pandas as pd

### python 제공 라이브러리 ###
# 뉴스 제목/url 수집
import feedparser
# 뉴스 본문 수집
from newspaper import Config, Article, Source
# 시간/날짜 dt라이브러리
import datetime
import datetime as dt
from datetime import timedelta

with codecs.open('./kbsm_230428_dgkb.csv','r', encoding='cp949', errors='ignore') as file:
        reader = csv.reader(file)
        
        values = []

        for row in reader:
                column_value = row[4]
                values.append(column_value)

                for values[1:] in :
                



url = 'http://www.kbsm.net'
header = {'User-Agent' : ''}
d = webdriver.Chrome('./chromedriver.exe')
d.set_window_position(0,0)
d.set_window_size(1920,1080)
d.implicitly_wait(3)
d.get(url)

current_date = datetime.date.today()

# - Article - #
art = Article(url, language = 'ko')
art.download()
art.parse()

for jynews in range(1, 26):
        #마우스 오버
        hover_all = d.find_element(By.XPATH,'/html/body/div[2]/header/div[2]/div[3]/div[1]/nav/ul/li[2]/a')
        act = ActionChains(d)
        act.move_to_element(hover_all).perform()

        #기사 지역 지정하기
        xpath_kbarea = f'/html/body/div[2]/header/div[2]/div[3]/div[1]/nav/ul/li[2]/div/div/div/div/div[2]/ul/li[{jynews}]/a'
        d.find_element(By.XPATH,xpath_kbarea).click()
        areaname = '/html/body/div[2]/div[4]/div/section/div/div[1]/div[1]/div/a/strong'
        area = d.find_element(By.XPATH, areaname).text
        print(area)

        for a in range(2, 12):
                xpath_numberarrow = f'/html/body/div[2]/div[4]/div/section/div/div[1]/div[2]/a[{a}]'
                sleep(1)
                d.find_element(By.XPATH, xpath_numberarrow).click()

                for jynews in range(1, 21):
                        wait_time = 10
                        wait = WebDriverWait(d, wait_time)
                        xpath_title = f'/html/body/div[2]/div[4]/div/section/div/div[1]/div[1]/ul/li[{jynews}]/a/div[2]/div[1]/strong'
                        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_title)))
                        element.click()
                        #변수에 저장
                        title = art.title       #기사제목
                        #authors -> 기자이름
                        formatted_date = current_date.strftime('%Y-%m-%d') #날짜
                        text = art.text         #내용

                        #기사출판 기자 가져오기
                        xpath_authors = f'/html/body/div[2]/div[3]/div[4]/div/section[1]/div/div/div[1]/div[3]/span[1]'
                        authors = d.find_element(By.XPATH, xpath_authors).text
                        #print(a.authors) #newspaper로 불러와지지 않음.

                        df = pd.DataFrame(columns=['지역명', '기사제목', '기자이름', '날짜', '내용', '링크'])
                        data = {
                                '지역명' : area, 
                                '기사제목' : text, 
                                '기자이름' : "경북신문 - " + authors,
                                '날짜' : formatted_date,
                                '내용' : title,
                                '링크' : column_value
                                }
                        df = df.append(data, ignore_index=True)
                df.to_csv("./kbsm_230602_dgkb.csv", mode = 'a', encoding='utf-8', header=False, index=False)
                len(df)
                d.back()
""" #기사 지역
print(area)
#기사 제목 출력하기
print(title)
#기사 출판기자 이름 출력하기
print(authors)
#기사 출판,년,월,일자 출력하기
print(formatted_date)
#기사 내용 출력하기(전체문단)
print(text)
#기사 링크 출력하기
print(link)
sleep(1) """
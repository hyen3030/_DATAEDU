from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep

import requests
import pandas as pd
import datetime
import time
import csv

### python 제공 라이브러리 ###
# 뉴스 제목/url 수집
import feedparser
# 뉴스 본문 수집
import newspaper
from newspaper import Article
# 시간/날짜 dt라이브러리
import datetime as dt
from datetime import timedelta
import datetime

url = "http://www.kbsm.net/"           #경북신문
header = {'User-Agent' : ''}
d = webdriver.Chrome('./chromedriver.exe')
d.set_window_position(0,0)
d.set_window_size(1920,1080)
d.implicitly_wait(3)
d.get(url)

today = dt.datetime.now().strftime("%Y%m%d") 
today = datetime.datetime(int(today[0:4]), int(today[4:6]), int(today[6:8]))

#1일전
before_1 = (today - timedelta(days = 1)).strftime("%Y%m%d") 
before_1 = datetime.datetime(int(before_1[0:4]), int(before_1[4:6]), int(before_1[6:8]))

art = newspaper.Article(url, language = 'ko')
art.download()
art.parse()

publish_date = (art.publish_date)
art_text = (art.text)

req = requests.get(url, verify=False)
html = req.text
soup = BeautifulSoup(html, "html.parser")
sleep(1)

#컬럼명 리스트
column_names = ["지역명", "기사제목", "기자이름", "날짜", "내용", "링크"]

csv_path = "./kbsm_230608_dgkb.csv"

with open(csv_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(column_names)

#지역뉴스로 이동
for jynews in range(1, 26):
    #마우스 오버
    hover_all = d.find_element(By.XPATH,'/html/body/div[2]/header/div[2]/div[3]/div[1]/nav/ul/li[2]/a')
    act = ActionChains(d)
    act.move_to_element(hover_all).perform()
    time.sleep(1)

    xpath_kbarea = f'/html/body/div[2]/header/div[2]/div[3]/div[1]/nav/ul/li[2]/div/div/div/div/div[2]/ul/li[{jynews}]/a'
    d.find_element(By.XPATH,xpath_kbarea).click()
    areaname = '/html/body/div[2]/div[4]/div/section/div/div[1]/div[1]/div/a/strong'
    area = d.find_element(By.XPATH, areaname).text
    print(area)

    xpath_afterarrow_1 = f'/html/body/div[2]/div[4]/div/section/div/div[1]/div[2]/a[12]' #1~10페이지에서만
    xpath_beforearrow = f'/html/body/div[2]/div[4]/div/section/div/div[1]/div[2]/a[2]' #11페이지부터~
    xpath_afterarrow = f'/html/body/div[2]/div[4]/div/section/div/div[1]/div[2]/a[13]' #11페이지부터~
    """    d.find_element(By.XPATH, xpath_afterarrow_1).click()
    sleep(1)
    d.find_element(By.XPATH, xpath_afterarrow).click()
    """
    for a in range(2, 12):
            xpath_numberarrow = f'/html/body/div[2]/div[4]/div/section/div/div[1]/div[2]/a[{a}]'
            sleep(1)
            d.find_element(By.XPATH, xpath_numberarrow).click()

            for jynews in range(1, 21):
                sleep(1)
            
                try:
                        xpath_title = f'/html/body/div[2]/div[4]/div/section/div/div[1]/div[1]/ul/li[{jynews}]/a/div[2]/div[1]/strong'
                        title_element = d.find_element(By.XPATH, xpath_title)
                except NoSuchElementException:
                        xpath_title = f'/html/body/div[2]/div[4]/div/section/div/div[1]/div[1]/ul/li[{jynews}]/a/div/div[1]/strong'
                        title_element = d.find_element(By.XPATH, xpath_title)
                d.find_element(By.XPATH, xpath_title).click()

                xpath_title_1 = '/html/body/div[2]/div[3]/div[4]/div/section[1]/div/div/div[1]/div[2]/h2'
                title = d.find_element(By.XPATH, xpath_title_1).text

                xpath_writer_1 = '/html/body/div[2]/div[3]/div[4]/div/section[1]/div/div/div[1]/div[3]/span[1]'
                writer = d.find_element(By.XPATH, xpath_writer_1).text

                xpath_date_1 = '/html/body/div[2]/div[3]/div[4]/div/section[1]/div/div/div[1]/div[3]/span[3]'
                date = d.find_element(By.XPATH, xpath_date_1).text

                if publish_date is not None:
                        # 날짜 정보 포맷팅
                        formatted_date = publish_date.strftime('%Y-%m-%d')
                        print(formatted_date)

                link = d.current_url

                #newspaper 라이브러리 사용
                #기사 날짜 가져오기
                #기사의 출판날짜 추출

                print(title + " - "+ writer)
                d.back()

                df = pd.DataFrame(columns=['지역명', '기사제목', '기자이름', '날짜', '내용', '링크'])
                df
                data = {
                        '지역명' : area, 
                        '기사제목' : title, 
                        '기자이름' : "경북신문 - " + writer,
                        '날짜' : formatted_date,
                        '내용' : art_text,
                        '링크' : link
                        }
                df = df.append(data, ignore_index=True)

                df.to_csv("./kbsm_230608_dgkb.csv", mode = 'a', encoding='utf-8', header=False, index=False)
                len(df)

print(art.title)
print(art.text)
print(art.publish_date)

sleep(2)
d.back()


""" page_code = {"대구" : "part_idx=700",
             "경북" : "part_idx=800",
             "포항" : "part_idx=801",
             "구미" : "part_idx=802",
             "경주" : "part_idx=803",
             "경산" : "part_idx=804",
             "안동" : "part_idx=805",
             "김천" : "part_idx=806",
             "칠곡" : "part_idx=807",
             "영주" : "part_idx=808",
             "상주" : "part_idx=809",
             "영천" : "part_idx=810",
             "문경" : "part_idx=811",
             "의성" : "part_idx=812",
             "울진" : "part_idx=813",
             "성주" : "part_idx=814",
             "예천" : "part_idx=815",
             "청도" : "part_idx=816",
             "영덕" : "part_idx=817",
             "고령" : "part_idx=818",
             "봉화" : "part_idx=819",
             "청송" : "part_idx=820",
             "군위" : "part_idx=821",
             "영양" : "part_idx=822",
             "울릉" : "part_idx=823",
             "기타" : "part_idx=824"
             } """
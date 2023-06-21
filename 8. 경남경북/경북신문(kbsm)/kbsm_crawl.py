from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from time import sleep

import requests
import pandas as pd
import datetime
import time

### python 제공 라이브러리 ###
# 뉴스 제목/url 수집
import feedparser
# 뉴스 본문 수집
from newspaper import Article

url = "http://www.kbsm.net/"           #경북신문
header = {'User-Agent' : ''}
d = webdriver.Chrome('./chromedriver.exe')
d.set_window_position(0,0)
d.set_window_size(1920,1080)
d.implicitly_wait(3)
d.get(url)

req = requests.get(url, verify=False)
html = req.text
soup = BeautifulSoup(html, "html.parser")
sleep(1)

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

    for a in range(2, 12):
            xpath_numberarrow = f'/html/body/div[2]/div[4]/div/section/div/div[1]/div[2]/a[{a}]'
            sleep(1)
            d.find_element(By.XPATH, xpath_numberarrow).click()

            for jynews in range(1, 21):
                sleep(1)
            
                xpath_title = f'/html/body/div[2]/div[4]/div/section/div/div[1]/div[1]/ul/li[{jynews}]/a/div[2]/div[1]/strong'
                d.find_element(By.XPATH, xpath_title).click()

                xpath_title_1 = '/html/body/div[2]/div[3]/div[4]/div/section[1]/div/div/div[1]/div[2]/h2'
                title = d.find_element(By.XPATH, xpath_title_1).text

                xpath_writer_1 = '/html/body/div[2]/div[3]/div[4]/div/section[1]/div/div/div[1]/div[3]/span[1]'
                writer = d.find_element(By.XPATH, xpath_writer_1).text

                xpath_date_1 = '/html/body/div[2]/div[3]/div[4]/div/section[1]/div/div/div[1]/div[3]/span[4]'
                date = d.find_element(By.XPATH, xpath_date_1).text

                link = d.current_url

                print(title + " - "+ writer)
                d.back()

                df = pd.DataFrame(columns=['지역명', '기사제목', '기자이름', '날짜', '링크'])
                df
                data = {'지역명' : area, 
                        '기사제목' : title, 
                        '기자이름' : "일간경북신문 - " + writer,
                        '날짜' : date[3:13],
                        '링크' : link}
                df = df.append(data, ignore_index=True)

                df.to_csv("./kbsm_230428_dgkb.csv", mode = 'a', encoding='utf-8', header=False, index=False)
                len(df)
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
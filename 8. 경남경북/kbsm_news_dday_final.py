from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from time import sleep

import requests
import pandas as pd
import re

import datetime as dt
from datetime import timedelta
import datetime

import feedparser
import pymysql
from newspaper import Article


options=webdriver.ChromeOptions()
options.add_argument('headless')
d = webdriver.Chrome('chromedriver.exe', options=options)

today = dt.datetime.now().strftime("%Y%m%d") 
today = datetime.datetime(int(today[0:4]), int(today[4:6]), int(today[6:8]))

#1일전
before_1 = (today - timedelta(days = 1)).strftime("%Y%m%d") 
before_1 = datetime.datetime(int(before_1[0:4]), int(before_1[4:6]), int(before_1[6:8]))

## 지역코드 ##
page_code = {
            "25" : "대구",
            "32": "경북도청",
            "26" : "포항",
            "27" : "경주",
            "35" : "김천",
            "28" : "안동",
            "29" : "구미",
            "36" : "영주",
            "37" : "영천",
            "38" : "상주",
            "39" : "문경",
            "40" : "경산",
            "30" : "군위",
            "41" : "의성",
            "42" : "청송",
            "43" : "영양",
            "44" : "영덕",
            "45" : "청도",
            "46" : "고령",
            "47" : "성주",
            "48" : "칠곡",
            "49" : "예천",
            "50" : "봉화",
            "31" : "울진",
            "51" : "울릉/독도"
            }




def get_url():
    
    article_list = []
    
    for a in range(2, 4):
        xpath_numberarrow = f'/html/body/div[2]/div[4]/div/section/div/div[1]/div[2]/a[{a}]'
        sleep(1)
        d.find_element(By.XPATH, xpath_numberarrow).click()

        articles = html.select("ul.list_news2_4 > li")

    for ar in articles:
        articleUrl = ar.find("a")['href']
        #print(articleUrl)

        articleDate = ar.select("div.news_date")[0].text
        articleDate = re.sub('[가-힣]', '', articleDate).replace("   ","")
        articleDate = datetime.datetime(int(articleDate[0:4]), int(articleDate[5:7]), int(articleDate[8:10]))
        #print(articleDate)

        ### 크롤링 전 전일/당일 데이터 수집 확인 필요 ###  
        if articleDate == before_1: # 크롤링 전일 데이터 가져오기
        #if articleDate == today: # 크롤링 당일 데이터 가져오기  
            article_list.append(articleUrl)
                
    return article_list


def kbsm_news():
    
    article_list = get_url()
        
    df = pd.DataFrame(columns=['지역명', '기사제목', '날짜', '내용', '저자', 'url'])
    df
    for i in range(len(article_list)):
        #print(i)
        url = article_list[i]
        article = Article(url, language='ko')
        article.download()
        article.parse()

        areaname = '/html/body/div[2]/div[4]/div/section/div/div[1]/div[1]/div/a/strong'
        area = d.find_element(By.XPATH, areaname).text
        df.at[i, '지역명'] = area

        title = article.title
        df.at[i, '기사제목'] = title

        date = article.publish_date
        df.at[i, '날짜'] = date

        text = article.text
        df.at[i, '내용'] = text

        author = "경북신문"
        df.at[i, '저자'] = author

        url = url
        df.at[i, 'url'] = url
    
        df = df.append(data, ignore_index=True)

        df.to_csv("./kbsm_230608_dgkb.csv", mode = 'a', encoding='utf-8', header=False, index=False)
    return df



all_df = pd.DataFrame()

for i in page_code:
    
    url = "http://www.kbsm.net/news/list_local.php?part_idx={0}".format(i)
    
    d.get(url)
    raw = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, "html.parser")
    sleep(1)
    
    data = kbsm_news()
    data["지역"] = page_code.get(i)
    print(len(data))
    
    all_df = pd.concat([all_df, data])

all_df = all_df.reset_index(drop = True)
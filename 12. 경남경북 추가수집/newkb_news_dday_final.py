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

# 뉴스 제목/url 수집
import feedparser
#sql연동
import pymysql
# **뉴스 본문 수집 라이브러리
from newspaper import Article

options=webdriver.ChromeOptions()
options.add_argument('headless')
d = webdriver.Chrome('chromedriver.exe', options=options)

today = dt.datetime.now().strftime("%Y%m%d") 
today = datetime.datetime(int(today[0:4]), int(today[4:6]), int(today[6:8]))

#1일전
before_1 = (today - timedelta(days = 1)).strftime("%Y%m%d") 
before_1 = datetime.datetime(int(before_1[0:4]), int(before_1[4:6]), int(before_1[6:8]))


page_code = {
            "700" : "대구",
            "801" : "포항",
            "802" : "구미",
            "803" : "경주",
            "804" : "경산",
            "805" : "안동",
            "806" : "김천",
            "807" : "칠곡",
            "808" : "영주",
            "809" : "상주",
            "810" : "영천",
            "811" : "문경",
            "812" : "의성",
            "813" : "울진",
            "814" : "성주",
            "815" : "예천",
            "816" : "청도",
            "817" : "영덕",
            "818" : "고령",
            "819" : "봉화",
            "820" : "청송",
            "821" : "군위",
            "822" : "영양",
            "823" : "울릉"
            }

url = ""

def get_url():
    
    article_list = []
    
    for a in range(2, 4):
        xpath_numberarrow = f'/html/body/div[2]/div[4]/div/section/div/div[1]/div[2]/a[{a}]'
        sleep(1)
        d.find_element(By.XPATH, xpath_numberarrow).click()

        articles = html.select("ul.list_news2_4 > li")

    for ar in articles:
        articleUrl = ar.find("a")['href']

        articleDate = ar.select("div.news_date")[0].text
        articleDate = re.sub('[가-힣]', '', articleDate).replace("   ","")
        articleDate = datetime.datetime(int(articleDate[0:4]), int(articleDate[5:7]), int(articleDate[8:10]))

        if articleDate == before_1: # 수집일 전일 데이터 가져오기
            article_list.append(articleUrl)
                
    return article_list



def newkb_news():
    
    article_list = get_url()
        
    df = pd.DataFrame(columns=['제목', '저자', '날짜', 'url', '내용'])

    for i in range(len(article_list)):
        url = article_list[i]
        article = Article(url, language='ko')
        article.download()
        article.parse()

        #제목
        title = article.title
        df.at[i, '제목'] = title

        #기사 업로드 날짜
        date = article.publish_date
        df.at[i, '날짜'] = date

        #본문
        text = article.text
        df.at[i, '내용'] = text

        author = "일간경북신문"
        df.at[i, '저자'] = author

        #url주소
        url = url
        df.at[i, 'url'] = url

    return df



all_df = pd.DataFrame()

for i in page_code:
    
    url = "http://www.newgbnews.com/news/list.php?part_idx={0}".format(i)
    
    d.get(url)
    raw = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, "html.parser")
    sleep(2)
    
    data = newkb_news()
    data["지역"] = page_code.get(i)
    print(len(data))
    
    all_df = pd.concat([all_df, data])  

all_df = all_df.reset_index(drop = "True") 



## 데이터 입력 ##
conn = pymysql.connect(host='175.214.251.92', port=3306, user='ghostuser', password='ghostpass!1', db='ghost_2021', charset='utf8mb4')

try:
    with conn.cursor() as cursor:
        sql = '''INSERT INTO newkb_news (title, author, register_date, url, body, region)
                 VALUES(%s, %s, %s, %s, %s, %s)'''
        
        for i in range(len(all_df)):
            val = [
                all_df["제목"][i],
                all_df["저자"][i],
                all_df["날짜"][i],
                all_df["url"][i],
                all_df["내용"][i],
                all_df["지역"][i]
                ]

            cursor.execute(sql,val)
            conn.commit()
            
finally:
    conn.close()
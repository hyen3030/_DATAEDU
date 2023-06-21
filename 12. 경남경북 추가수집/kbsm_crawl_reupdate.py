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

        articleDate = ar.select("div.news_date")[0].text
        articleDate = re.search(r"\d{4}/\d{2}/\d{2}\s\d{2}:\d{2}", articleDate).group()
        articleDate = datetime.datetime.strptime(articleDate, "%Y/%m/%d %H:%M")

        if articleDate >= datetime.datetime(2023, 5, 9):
            article_list.append(articleUrl)
                
    return article_list

def kbsm_news():
    article_list = get_url()
    df = pd.DataFrame(columns=['지역', '제목', '저자', '날짜', 'url', '내용'])

    for h in range(len(article_list)):
        url = article_list[h]
        if pd.isna(url):
            continue
        try:
            article = Article(url, language='ko')
            article.download()
            article.parse()

            title = article.title
            author = "경북신문"
            date = article.publish_date.date()
            text = article.text

            print(title)
            print(author)
            print(date)
            print(url)
            print(text)

            new_data = {
                '지역': page_code.get(i),
                '제목': title,
                '저자': author,
                '날짜': date,
                'url': url,
                '내용': text,
            }

            df = df.append(new_data, ignore_index=True)

        except Exception as e:
            print(f"Error occurred for URL: {url}")
            print(f"Error message: {str(e)}")

    with open("./a.csv", mode='a', encoding='utf-8', newline='') as f:
        df.to_csv(f, index=False, header=f.tell()==0)

    return df

all_df = pd.DataFrame()

for i in page_code:
    
    url = "http://www.kbsm.net/news/list_local.php?part_idx={0}".format(i)
    
    d.get(url)
    raw = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, "html.parser")
    sleep(2)
    
    data = kbsm_news()
    data["지역"] = page_code.get(i)
    print(len(data))
    
    all_df = pd.concat([all_df, data])  

all_df = all_df.reset_index(drop = "True") 
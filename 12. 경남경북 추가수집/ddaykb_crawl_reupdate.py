from selenium import webdriver
from newspaper import Article
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import requests
import pandas as pd
import re

import datetime as dt
from datetime import timedelta
import datetime

# 뉴스 제목/url 수집
import feedparser

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

        if articleDate >= datetime.datetime(2023, 5, 9):
            article_list.append(articleUrl)

    return article_list

def newkb_news():
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
            author = "일간경북신문"
            date = article.publish_date.date()
            text = article.text

            print(title)
            print(author)
            print(date)
            print(url)
            print(text)

            new_data = {
                '지역' : page_code.get(i),
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
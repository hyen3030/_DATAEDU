#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep


# In[2]:


import requests


# In[3]:


import pandas as pd


# In[4]:


import datetime


# In[5]:


### python 제공 라이브러리 ###
# 뉴스 제목/url 수집
import feedparser
# 뉴스 본문 수집
from newspaper import Article


# In[8]:


### 백그라운드 실행

options=webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('C:/chromedriver/chromedriver.exe', options=options)


# In[5]:


header = {'User-Agent': ''}
driver = webdriver.Chrome('C:/chromedriver/chromedriver.exe') # webdriver = chrome
driver.implicitly_wait(3) # 로딩 기다리기


# In[ ]:





# In[9]:


address_g="http://www.gndomin.com/news/articleView.html?idxno=347932"
driver.get(address_g)

req = requests.get(address_g,verify=False)
html = req.text 
soup = BeautifulSoup(html, "html.parser")
sleep(2)


# In[51]:


page_code = {"창원" : "S2N68",
            "진주" : "S2N69",
            "통영" : "S2N70",
            "사천" : "S2N71",
            "김해" : "S2N72",
            "밀양" : "S2N73",
            "거제" : "S2N74",
            "양산" : "S2N75",
            "의령" : "S2N76",
            "함안" : "S2N77",
            "창녕" : "S2N78",
            "고성" : "S2N79",
            "남해" : "S2N80",
            "하동" : "S2N81",
            "산청" : "S2N82",
            "함양" : "S2N83",
            "거창" : "S2N84",
            "합천" : "S2N85",
            "부산" : "S2N86",
            }


# ## test

# In[10]:


url = "http://www.gndomin.com/news/articleView.html?idxno=347932"


# In[137]:


article = Article(url, language='ko')
article.download()
article.parse()


# In[138]:


title = article.title
text = article.text
date = article.publish_date
date = date.strftime('%Y-%m-%d')
author = "경남도민신문"


# In[ ]:





# ## 실제 원하는 지역, 정보 수집

# In[82]:


df = pd.DataFrame(columns=['제목', '저자', '날짜', '링크', '내용', '요약'])

url_Tit = list()

for n in range(1, 300):
#or n in range(1, 5):
    
    #print(n)
    if n%10 == 0:
        print(n)
    
    ## 페이지별 url 가져오기
    url = "http://www.gndomin.com/news/articleList.html?page={0}&total=15407&box_idxno=&sc_sub_section_code=S2N85&view_type=sm".format(n)
    #params = {"page" : n,
    #          "total" : 15407,
    #          "box_idxno" : "",
    #          "sc_sub_section_code" : "S2N68",
    #          "view_type" : "sm"          
    #          }
    
    #raw = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, params = params)
    raw = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(raw.text, "html.parser")
    list_Tit = soup.find_all('div', attrs={"class" : "list-titles"})   

    for i in list_Tit :
        if i.a['href'] == "":
            pass
        else:
            url_Tit.append("http://www.gndomin.com" + i.a['href'])
     
    
Merge = [(x, url_Tit[x]) for x in range(len(url_Tit))]

## 가져온 페이지 리스트에 따라 정보 수집
for (i, url_Tit) in Merge:

    article = Article(url_Tit, language='ko')
    article.download()
    article.parse()

    df.at[i, '링크'] = url
    #print(author)

    #제목 
    title = article.title
    df.at[i, '제목'] = title

    # 날짜 
    date = article.publish_date
    df.at[i, '날짜'] = date.strftime('%Y-%m-%d')

    # 내용
    text = article.text
    df.at[i, '내용'] = text

    df.at[i, '저자'] = "경남도민신문"


# In[42]:


df.head()


# In[83]:


df.tail()


# In[84]:


len(df)


# In[86]:


df.to_csv("./gndomin_hapcheon_300_230331.csv")


# In[87]:


year_y = []

for i in range(len(df)):
    if int(df["날짜"][i][0:4]) >= 2021:
        year_y.append(i)


# In[88]:


df_select = df.iloc[0:len(year_y), :]


# In[89]:


df_select.to_csv("./gndomin_Hapcheon_300(2021more)_230331.csv")


# In[ ]:





# In[90]:


driver.quit()


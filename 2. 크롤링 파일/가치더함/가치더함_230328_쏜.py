#!/usr/bin/env python
# coding: utf-8

# In[4]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import requests
import re
import pandas as pd
import numpy as np
import os

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import warnings
warnings.filterwarnings('ignore')

import time


### 가치더함 사이트접속

address_jejudsi="https://jejudsi.kr/issue.htm" #사이트 주소
header = {'User-Agent': ''}
d = webdriver.Chrome('C:/chromedriver/chromedriver.exe') #chromedriver.exe 존재하는 경로
d.implicitly_wait(3)
d.get(address_jejudsi)


# In[5]:


req = requests.get("https://www.jejudsi.kr/issue.htm", verify=False)
html = req.text                                     #HTML소스코드 가져오기
soup = BeautifulSoup(html, "html.parser")           #HTML코드 파싱하기
sleep(2)


# In[80]:


# 프로젝트 페이지 링크 
html_2 = d.page_source
soup_2 = BeautifulSoup(html_2, "html.parser")
list_issueTit = soup_2.find_all('div', attrs={"class" : "issue-tit"})

url_issueTit = list()
for i in list_issueTit :
    url_issueTit.append(i.a['href'])


# In[48]:


def page_crawler():
    
    cleantext_reason = list()
    cleantext_content = list()
    cleantext_cuase = list()
    cleantext_suggestion = list()
    cleantext_solution = list()
    cleantext_vote = list()
    cleantext_reference = list()

    # 링크에서 id값 추출 
    path_link = d.current_url
    page_no = d.current_url.replace("https://jejudsi.kr/issue/", "").replace("#!#none","").split("/")
    page_id = page_no[0]
    page = page_no[1]
    
    # 프로젝트 종류/진행상황
    path_status ='/html/body/div[1]/section/div[1]/div/p[1]/span'
    status = d.find_element(By.XPATH, path_status).text

    # 프로젝트 시작날짜 시점
    try :        
        path_period = '/html/body/div[1]/section/div[2]/div/div[3]/div[1]/div[1]/div/div[2]/h3'
        period = d.find_element(By.XPATH, path_period).text.replace("공감투표기간 : ","").split(" ~ ")
        start = period[0]
        end =  period[1]
    except :
        start = np.nan
        end = np.nan

    # 프로젝트 제목
    title = d.find_element(By.CLASS_NAME, 'text-center').text

    category = "★수정필요"
    
    
    html_test = d.page_source
    soup_test = BeautifulSoup(html_test, "html.parser")
    list_test = soup_test.find_all('div', attrs={"class" : "card m-t-10"})

    list_list_test = list()

    for i_list_test in list_test :
        cleantext = i_list_test.text
        i_list_test = re.sub("\xa0",'', cleantext) # \n 삭제.

        if '미추진 사유' in i_list_test[:15] :
            cleantext_reason.append(i_list_test)
            cleantext_content.append("")
            cleantext_cuase.append("")
            cleantext_suggestion.append("")
            cleantext_solution.append("")
            cleantext_vote.append("")
            cleantext_reference.append("")

        elif '상세 내용' in i_list_test[:15] :
            cleantext_reason.append("")
            cleantext_content.append(i_list_test[6:])
            cleantext_cuase.append("")
            cleantext_suggestion.append("")
            cleantext_solution.append("")
            cleantext_vote.append("")
            cleantext_reference.append("")

        elif '제안의 시작' in i_list_test[:15] :
            cleantext_reason.append("")
            cleantext_content.append("")
            cleantext_cuase.append(i_list_test.replace("\n\n제안의 시작 (문제정의)\n",""))
            cleantext_suggestion.append("")
            cleantext_solution.append("")
            cleantext_vote.append("")
            cleantext_reference.append("")

        elif '주요제안' in i_list_test[:15] :
            cleantext_reason.append("")
            cleantext_content.append("")
            cleantext_cuase.append("")
            cleantext_suggestion.append(i_list_test[12:]) # '주요제안(문제정의)[12:]' 빼기
            cleantext_solution.append("")
            cleantext_vote.append("")
            cleantext_reference.append("")

        elif '해결방안' in i_list_test[:15] :
            cleantext_reason.append("")
            cleantext_content.append("")
            cleantext_cuase.append("")
            cleantext_suggestion.append("")
            cleantext_solution.append(i_list_test[6:])   
            cleantext_vote.append("")
            cleantext_reference.append("")

        elif '공감투표' in i_list_test[:15] :
            cleantext_reason.append("")
            cleantext_content.append("")
            cleantext_cuase.append("")
            cleantext_suggestion.append("")
            cleantext_solution.append("") 
            cleantext_vote.append(i_list_test[10:])
            cleantext_reference.append("")

        elif '관련 자료' in i_list_test[:15] :
            cleantext_reason.append("")
            cleantext_content.append("")
            cleantext_cuase.append("")
            cleantext_suggestion.append("")
            cleantext_solution.append("") 
            cleantext_vote.append("")
            cleantext_reference.append(i_list_test[12:])

        else : ##### 비어잇는 값으로 처리합니다.
            pass

    else :
        pass
    
    new_row = pd.DataFrame({
                    'id 값' : page_id
                    ,'제목' : title
                    ,'분류' : category
                    ,'page' : page 
                    ,'프로젝트 시작' : start
                    ,'프로젝트 종류' : status
                    ,'상세 내용' : cleantext_content
                    ,'제안의 시작' : cleantext_cuase
                    ,'주요제안(문제정의)' : cleantext_suggestion
                    ,'해결방안' : cleantext_solution
                    ,'링크' : path_link
                    ,'미추진 사유' : cleantext_reason
                    ,'공감투표 참여안내' : cleantext_vote
                    ,'참고자료' : cleantext_reference
                    }, index=[0])
    
    return new_row


# In[ ]:





# In[65]:


df = pd.DataFrame()


# In[89]:


### 단계 나누기
## 페이지별 단계는 총 3단계 : index는 굳이 중복되므로 확인하지 않아도 된다.
list_tag_issueTit = list()  
page_tag = ["PROPOSE", "RESPONSE", "PROJECT"]

for j in list_tag_issueTit:
    for i in page_tag:
        d.get(f'https://jejudsi.kr/{j}/{i}')

        path_not_page = '//*[@id="main"]/div/div/div[2]/div/div/div[1]/div'
        not_page = d.find_element(By.XPATH, path_not_page).text

        if not_page == "불편을 드려 죄송합니다.":
            pass
            time.sleep(1)
        else:
            test = page_crawler()
            time.sleep(1)

            df = pd.concat([df, test])


# In[ ]:


df.head()


# In[ ]:





# In[ ]:





# In[ ]:





# !/usr/bin/env python
# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import requests
import re
import pandas as pd
import numpy as np
import os
import csv
import urllib.parse

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import warnings
warnings.filterwarnings('ignore')
import time

### 가치더함 사이트접속

address_jejudsi="https://jejudsi.kr/issue.htm"
header = {'User-Agent': ''}
d = webdriver.Chrome('./chromedriver.exe')
d.implicitly_wait(3)
d.get(address_jejudsi)

req = requests.get("https://www.jejudsi.kr/issue.htm", verify=False)
html = req.text
soup = BeautifulSoup(html, "html.parser")

# 프로젝트 제목
xpath_tit_new = f'/html/body/div[1]/section/div/div/div[2]/div/div/div/div/div[4]/div[1]/div[1]/div[{1}]/div/div[3]/div[3]/a'
title_new = d.find_element(By.XPATH,xpath_tit_new).text
title = d.find_element(By.CLASS_NAME, 'issue-tit').text

xpath_tit_proj = f'/html/body/div[1]/section/div/div/div[2]/div/div/div/div/div[7]/div[1]/div[2]/div[{2}]/div/div[3]/div[3]/a'
title_proj = d.find_element(By.XPATH,xpath_tit_proj).text

xpath_tit_end = f'/html/body/div[1]/section/div/div/div[2]/div/div/div/div/div[7]/div[1]/div[2]/div[{3}]/div/div[3]/div[3]/a'
title_end = d.find_element(By.XPATH,xpath_tit_end).text

# 프로젝트 페이지 링크 

html_2 = d.page_source
soup_2 = BeautifulSoup(html_2, "html.parser")
list_issueTit = soup_2.find_all('div', attrs={"class" : "issue-tit"})

url_issueTit = list()

for i in list_issueTit :
    url_issueTit.append(i.a['href'])

for p in range(2, 9+1):
    xpath_cate = f'/html/body/div[1]/section/div/div/div[2]/div/div/div/div/nav/div[2]/ul/li[{p}]/a'
    d.find_element(By.XPATH,xpath_cate).click()
    category = d.find_element(By.XPATH,xpath_cate).text # 카테고리
    print(category)

    # 더보기 무한 클릭
    path_more ='/html/body/div[1]/section/div/div/div[2]/div/div/div/div/div[7]/div[2]/a'
    while True :
            try :
                d.find_element(By.XPATH,path_more).click()
            except :
                break

def savecsv(data):
    #저장할 파일의 파일명
    filename = 'index.csv'

    #데이터의 중복여부 확인을 위한 파일 읽기
    existing_data = set()
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
        next(reader) #첫번째 행 건너뛰기
        for row in reader(f):
            existing_data(tuple(row))
    except FileNotFoundError:
        pass

        new_data = []
        for d_ in data:
            if tuple(d.values()) not in existing_data:
                new_data.append(d_)

        with open(filename, 'a', newline='', encoding = 'utf-8') as f:
            fieldnames = ['id 값', '제목', '분류', 
                            'page', '프로젝트 시작', '프로젝트 종류',
                            '상세 내용', '제안의 시작', '주요제안(문제정의)', 
                            '해결방안', '링크', '미추진 사유',
                            '공감투표 참여안내', '참고자료']
            
            writer = csv.DictWriter(f, fieldnames = fieldnames)

            if not existing_data:
                writer.writeheader()
            for d in new_data:
                writer.writerow(d)

# 크롤링하는 함수
def page_crawler():                    
    col = [
        'id 값'
        ,'page'
        ,'제목'
        ,'분류'
        ,'프로젝트 시작'
        ,'프로젝트 종류'
        ,'상세 내용'
        ,'제안의 시작'
        ,'주요제안(문제정의)'
        ,'해결방안'
        ,'링크'
        ,'미추진 사유'
        ,'공감투표 참여안내'
        ,'참고자료'
        ]
    df = pd.DataFrame(columns=col)
    
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
    print(page)
    print("id : " + page + "(" "link : " + path_link + ")")  
    
    # 프로젝트 종류/진행상황
    path_status ='/html/body/div[1]/section/div[1]/div/p[1]/span'
    status = d.find_element(By.XPATH, path_status).text
    print(status)

    # 프로젝트 시작날짜 시점
    try :      
        path_period = '/html/body/div[1]/ction/div[2]/div/div[3]/div[1]/div[1]/div/div[2]/h3'         # 공감투표 기간이 표시된 태그의 XPath.
        period = d.find_element(By.XPATH, path_period).text.replace("공감투표기간 : ","").split(" ~ ")   # period: 시작 날짜와 종료 날짜를 나타내는 문자열. 이 문자열에서 replace() 메서드를 사용하여 "공감투표기간 : "을 제거한 후, split() 메서드를 사용하여 시작 날짜와 종료 날짜를 분리.
        start = period[0]       
        end =  period[1]        
    except :
        start = np.nan
        end = np.nan
    print("date : " + path_period)

    # 내용 수집
    html_test = d.page_source
    soup_test = BeautifulSoup(html_test, "html.parser")

    # mt-3 섹션
    list_test = soup_test.find_all('div', attrs={"class" : "card mt-3"})

    list_list_test = list()
    for i_list_test in list_test:
        cleantext = i_list_test.text
        i_list_test = re.sub("\xa0",'', cleantext) # \n 삭제.

        if '미추진 사유' in i_list_test[:14] :
            cleantext_reason.append(i_list_test)
            cleantext_content.append("")
            cleantext_cuase.append("")
            cleantext_suggestion.append("")
            cleantext_solution.append("")
            cleantext_vote.append("")
            cleantext_reference.append("")

        elif '상세 내용' in i_list_test[:14] :
            cleantext_reason.append("")
            cleantext_content.append(i_list_test[8:])
            cleantext_cuase.append("")
            cleantext_suggestion.append("")
            cleantext_solution.append("")
            cleantext_vote.append("")
            cleantext_reference.append("")

        elif '제안의 시작' in i_list_test[:14] :
            cleantext_reason.append("")
            cleantext_content.append("")
            cleantext_cuase.append(i_list_test.replace("\n\n제안의 시작 (문제정의)\n",""))
            cleantext_suggestion.append("")
            cleantext_solution.append("")
            cleantext_vote.append("")
            cleantext_reference.append("")

        elif '주요제안' in i_list_test[:14] :
            cleantext_reason.append("")
            cleantext_content.append("")
            cleantext_cuase.append("")
            cleantext_suggestion.append(i_list_test[12:]) #'주요제안(문제정의)[12:]'빼기
            cleantext_solution.append("")
            cleantext_vote.append("")
            cleantext_reference.append("")

        elif '해결방안' in i_list_test[:14] :
            cleantext_reason.append("")
            cleantext_content.append("")
            cleantext_cuase.append("")
            cleantext_suggestion.append("")
            cleantext_solution.append(i_list_test[6:])   
            cleantext_vote.append("")
            cleantext_reference.append("")

        elif '공감투표' in i_list_test[:14] :
            cleantext_reason.append("")
            cleantext_content.append("")
            cleantext_cuase.append("")
            cleantext_suggestion.append("")
            cleantext_solution.append("") 
            cleantext_vote.append(i_list_test[10:])
            cleantext_reference.append("")

        elif '관련 자료' in i_list_test[:14] :
            cleantext_reason.append("")
            cleantext_content.append("")
            cleantext_cuase.append("")
            cleantext_suggestion.append("")
            cleantext_solution.append("") 
            cleantext_vote.append("")
            cleantext_reference.append(i_list_test[12:])

        else : 
            pass
    else:
        pass

    # mt-t-10 섹션
    list_test = soup_test.find_all('div', attrs={"class" : "card m-t-10"})
    list_list_test = list()

    for i_list_test in list_test :
        cleantext = i_list_test.text
        i_list_test = re.sub("\xa0",'', cleantext) # \n 삭제.

        if '미추진 사유' in i_list_test[:14] :
            cleantext_reason.append(i_list_test)
            cleantext_content.append("")
            cleantext_cuase.append("")
            cleantext_suggestion.append("")
            cleantext_solution.append("")
            cleantext_vote.append("")
            cleantext_reference.append("")

        elif '상세 내용' in i_list_test[:14] :
            cleantext_reason.append("")
            cleantext_content.append(i_list_test[6:])
            cleantext_cuase.append("")
            cleantext_suggestion.append("")
            cleantext_solution.append("")
            cleantext_vote.append("")
            cleantext_reference.append("")

        elif '제안의 시작' in i_list_test[:14] :
            cleantext_reason.append("")
            cleantext_content.append("")
            cleantext_cuase.append(i_list_test.replace("\n\n제안의 시작 (문제정의)\n",""))
            cleantext_suggestion.append("")
            cleantext_solution.append("")
            cleantext_vote.append("")
            cleantext_reference.append("")

        elif '주요제안' in i_list_test[:14] :
            cleantext_reason.append("")
            cleantext_content.append("")
            cleantext_cuase.append("")
            cleantext_suggestion.append(i_list_test[12:]) #'주요제안(문제정의)[12:]'빼기
            cleantext_solution.append("")
            cleantext_vote.append("")
            cleantext_reference.append("")

        elif '해결방안' in i_list_test[:14] :
            cleantext_reason.append("")
            cleantext_content.append("")
            cleantext_cuase.append("")
            cleantext_suggestion.append("")
            cleantext_solution.append(i_list_test[6:])   
            cleantext_vote.append("")
            cleantext_reference.append("")

        elif '공감투표' in i_list_test[:14] :
            cleantext_reason.append("")
            cleantext_content.append("")
            cleantext_cuase.append("")
            cleantext_suggestion.append("")
            cleantext_solution.append("") 
            cleantext_vote.append(i_list_test[10:])
            cleantext_reference.append("")

        elif '관련 자료' in i_list_test[:14] :
            cleantext_reason.append("")
            cleantext_content.append("")
            cleantext_cuase.append("")
            cleantext_suggestion.append("")
            cleantext_solution.append("") 
            cleantext_vote.append("")
            cleantext_reference.append(i_list_test[12:])

        else : 
            pass

    else :
        pass

    df = pd.read_csv("_index.csv", encoding = "utf-8-sig")
    df.drop_duplicates(subset=['page', '제목', '분류', '프로젝트 시작', '프로젝트 종류'])
    df = df.append(new_row,ignore_index=True) # 새로운 행 추가
    df.to_csv("_index.csv", encoding="utf-8-sig", index=False)

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

list_tag_issueTit = list()
page_tag = ["PROPOSE", "RESPONSE", "PROJECT"]

for j in list_tag_issueTit:
    for i in page_tag:
        d.get(f'https://jejudsi.kr{j}/{i}')

        path_not_page = '//*[@id="main"]/div/div/div[2]/div/div/div[1]/div'
        not_page = d.find_element(By.XPATH, path_not_page).text

        if not_page == "불편을 드려 죄송합니다.":
            pass
            time.sleep(1)
        else:
            test = page_crawler()
            time.sleep(1)

            df = pd.concat([df, test])
            df.head()
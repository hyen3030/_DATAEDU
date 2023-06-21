from selenium import webdriver #크롬 브라우저창(자동화)을 열때 사용하는 모듈.
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
from urllib.parse import urlparse, parse_qs, urljoin
import requests #특정 웹사이트에 HTTP 요청을 보내는 모듈.
import re #정규표현 처리를 하기 위해 표준 라이브러리이다.
import pandas as pd #데이터분석 및 조작을 위한 소프트웨어 라이브러리이다.
import numpy as np #다차원 배열을 쉽게 처리하고 효율적으로 사용할 수 있도록 지원하는 파이썬 라이브러리이다.
import os #운영체제에서 제공되는 여러 가지 기능을 파이썬에서 수행할 수 있도록 해주는 모듈.
import urllib.request
import urllib.parse #한글을 아스키코드로 변환.
import csv


from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import warnings
warnings.filterwarnings('ignore')

#url
address_hanam_LivLab="https://livinglab.hanam.go.kr/livinglab/livinglabList.hs" #사이트 주소

### 하남리빙랩 사이트접속
header = {'User-Agent': ''}
d = webdriver.Chrome('./chromedriver.exe') #chromedriver.exe 존재하는 경로
d.implicitly_wait(3)
d.get(address_hanam_LivLab)
req = requests.get(address_hanam_LivLab,verify=False)
html = req.text 
soup = BeautifulSoup(html, "html.parser")


xpath_click_collect = '/html/body/div/div[2]/div[2]/div/div[2]/div[1]/div/label'
collect = d.find_element(By.XPATH,xpath_click_collect).text
d.find_element(By.XPATH,xpath_click_collect).click() #스스로 해결단 모집 라벨클릭이벤트

for i in range(1,10):
#'메인' 페이지
    d.refresh()

    xpath_tmp = f'/html/body/div/div[2]/div[2]/div/div[4]/div/ul/li[{i}]/a/div[2]/div/h3'
    # 인원
    xpath_peo = f'/html/body/div/div[2]/div[2]/div/div[4]/div/ul/li[{i}]/a/div[3]/p[1]/span'
    people = d.find_element(By.XPATH, xpath_peo).text
    
    d.find_element(By.XPATH,xpath_tmp).click()

    html_2 = d.page_source
    soup_2 = BeautifulSoup(html_2, "html.parser")
    list_title = soup_2.find_all('div', attrs={"class" : "issue-tit"})

    list_tag_title = list()

    for i_list_title in list_title:
        href = i_list_title.a['href']
        parsed_href = urlparse(href)
        query_params = parse_qs(parsed_href.query)
        liv_id = query_params['livinglabSeq'][0]
        list_tag_title.append(urljoin(address_hanam_LivLab, f"livinglabDetail.hs?livinglabSeq={liv_id}"))
    
    
    
    # 제목(title)
    title = d.find_element(By.XPATH, "/html/body/div/div[2]/div[2]/div[2]/div/div/div[1]/h3").text

    # 기간_시작일(start) - 기준이없음.
    # start = d.find_element(By.XPATH,"")

    # 기간_종료일(end) - 기준이없음.
    # end = d.find_element(By.XPATH,"")

    # 작성일자(day_write)
    day_write = d.find_element(By.XPATH,"/html/body/div/div[2]/div[2]/div[2]/div/div/div[1]/span").text

    # 단계
    grade = d.find_element(By.CSS_SELECTOR, "body > div > div.wrapper > div.body-container > div.content-wrap > div > div > div.info-area > div.process-select > ul > li.ng-scope.select")
    text = grade.text

    print(list_tag_title) # 1. id
    print("제목 : " + title) # 2. 제목
    print("단계 : " + text) # 10. 단계
    print("작성일자 : " + day_write) # 7. (작성일자)
    print("인원 : " + people) # 11. 인원

    sleep(3)
    print("==========***==========")
    d.back()

    
    # 12. 내용


""" #'문제찾기' 클릭이벤트
xpath_click_searchquestion = '/html/body/div[1]/div[2]/div[2]/div/div[2]/div[2]/div/label'
searchquestion = d.find_element(By.XPATH,xpath_click_searchquestion).text
d.find_element(By.XPATH,xpath_click_searchquestion).click() """

""" 
for i in range(1,13):
    xpath_tmp = f'/html/body/div/div[2]/div[2]/div/div[4]/div/ul/li[i]/a/div[2]/div/h3'
    d.find_element(By.XPATH,xpath_tmp).click()

#'해결 아이디어 제시' 클릭이벤트
xpath_click_idea = '/html/body/div/div[2]/div[2]/div/div[2]/div[3]/div/label'
idea = d.find_element(By.XPATH,xpath_click_idea).text
d.find_element(By.XPATH,xpath_click_idea).click()

for i in range(1,13):
    xpath_tmp = f'/html/body/div/div[2]/div[2]/div/div[4]/div/ul/li[i]/a/div[2]/div/h3'
    d.find_element(By.XPATH,xpath_tmp).click()

#'실현' 클릭이벤트
xpath_click_cometrue = '/html/body/div/div[2]/div[2]/div/div[2]/div[4]/div/label'
cometrue = d.find_element(By.XPATH_click_cometrue).text
d.find_element(By.XPATH,xpath_click_cometrue).click()

for i in range(1,13):
    xpath_tmp = f'/html/body/div/div[2]/div[2]/div/div[4]/div/ul/li[i]/a/div[2]/div/h3'
    d.find_element(By.XPATH,xpath_tmp).click() """


""" for link in soup.find_all('a', href=re.compile('^/livinglab/livinglabView.hs')):
    print('https://livinglab.hanam.go.kr' + link.get('href')) """


""" ##### response 본문이미지 태그(/img) 크롤링 #####
html_3 = d.page_source
soup_3 = BeautifulSoup(html_3, "html.parser")
image_links = []
for img in soup_3.find_all('img', attrs={"class" : "ng-scope"}):
    src = img.get('src')
    if src.endswith('.jpg') or src.endswith('.jpeg') or src.endswith('.png'):
        image_links.append(src)

print(image_links)  """




""" /하남_리빙랩
1. id([ex]livinglabSeq = 12, 14, 16...)
2. 제목
3. 카테고리
4. 기간
5. 기간_시작일(start)
6. 기간_종료일(end)
7. (작성일자)
8. (상위단계)
9. (하위단계)
10. 단계
11. 인원
12. 내용
13. 이미지
14. 세부페이지
15. 링크(url)
16. 수집일자
17. 좋아요수
18. 댓글수
19. 댓글 
"""
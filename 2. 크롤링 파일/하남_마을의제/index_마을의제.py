from selenium import webdriver #크롬 브라우저창(자동화)을 열때 사용하는 모듈.
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
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
address_hanam_maeul="https://livinglab.hanam.go.kr/agenda/agendaList.hs" #사이트 주소

### 하남 마을의제 사이트접속 ###
header = {'User-Agent': ''}
d = webdriver.Chrome('./chromedriver.exe') #chromedriver.exe 존재하는 경로
d.implicitly_wait(3)
d.get(address_hanam_maeul)
req = requests.get(address_hanam_maeul,verify=False)
html = req.text 
soup = BeautifulSoup(html, "html.parser")
sleep(2)

# 1. id([ex]agendaSeq = 70, 69, 68...) 추출

# 2. 제목 추출
title = d.find_element(By.CLASS_NAME, 'ng-binding').text
print(title)
# 3. 카테고리 추출
# category = d.find_element(By.XPATH,xpath_tmp).text

# 4. 

# 5. 기간_시작일(start)
try:
    path_start = '/html/body/div[4]/div[2]/div[2]/div/div[3]/div[2]/div/div/a[1]/div/div[2]/div[2]/span'
    start = d.find_element(By.XPATH, path_start).text
    start = start[3:11]
except:
    start = np.nan
print("시작일 : " + start)

# 6. 기간_종료일(end)
try :
    path_end = '/html/body/div[4]/div[2]/div[2]/div/div[3]/div[2]/div/div/a[1]/div/div[2]/div[2]/span'
    end = d.find_element(By.XPATH, path_end).text
    end = end[14:22]
except:
    en = np.nan
print("종료일 : " + end)

# 7. 작성일자
date_write = soup.find_all('div', attrs = {"class" : "info-area clearfix"})
#print(date_write)


""" /하남_마을의제
1. id([ex]agendaSeq = 70, 69, 68...)
2. 제목
3. 카테고리
4. 기간
5. 기간_시작일(start)
6. 기간_종료일(end)
7. (작성일자)
8. 단계
9. 내용
10. 링크(url)
11. 수집일자 """
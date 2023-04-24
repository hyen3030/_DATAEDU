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

import pandas as pd


address_jejudsi="https://jejudsi.kr/issue.htm" #사이트 주소


###사이트접속


header = {'User-Agent': ''}
d = webdriver.Chrome('./chromedriver.exe') #chromedriver.exe 존재하는 경로
d.implicitly_wait(3)
d.get(address_jejudsi)
req = requests.get(address_jejudsi,verify=False)
html = req.text 
soup = BeautifulSoup(html, "html.parser")
sleep(2)

for i in range(2,3) :
      xpath_tmp = f'//*[@id="navbarSupportedContent"]/ul/li[{i}]/a'
      d.find_element(By.XPATH,xpath_tmp).click()
      
      # 카테고리 추출
      category = d.find_element(By.XPATH,xpath_tmp).text  
      '''
      2 = 보건복지
      3 = 산업경제
      4 = 도시교통
      5 = 문화교육
      6 = 관광
      7 = 환경
      8 = 농축수산
      9 = 기타
      '''
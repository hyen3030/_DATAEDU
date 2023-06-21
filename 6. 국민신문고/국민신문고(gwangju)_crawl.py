from telnetlib import Telnet
from turtle import title
from bs4 import BeautifulSoup
from matplotlib.textpath import text_to_path
import requests, json, re, time, datetime, random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np
from tqdm import tqdm
import csv
import sys
import os
import warnings
warnings.filterwarnings('ignore')


# url = 'https://www.miryang.go.kr/web/index.do?mnNo=10301010000' #국민신문고 링크 
# url2 = 'https://www.epeople.go.kr/frm/pttn/openPttnList.npaid?frmMenuMngNo=WBF-1705-000057' #통합 프레임 링크

#url = 'https://www.yangsan.go.kr/portal/contents.do?mId=0204010000'
url2 = 'https://www.gjcity.go.kr/portal/frame/epeopleOpen.do?mId=0401010000'
header = {'User-Agent': ''}
driver = webdriver.Chrome('./chromedriver.exe') 
driver.implicitly_wait(3)
#driver.get(url)

wait = WebDriverWait(driver, 10)

# 새 탭 열어 링크로 이동 
driver.execute_script('window.open("");') 
driver.switch_to.window(driver.window_handles[-1]) 
driver.get(url2)

req = requests.get(url2,verify=False)
html = req.text 
soup = BeautifulSoup(html, "html.parser")

from selenium.webdriver.support.select import Select
select = Select(driver.find_element(By.ID, "listCnt"))
select.select_by_index(4) #50개보기 선택

#2021-04-19 ~ 2021-10-19
#2021-10-20 ~ 2022-04-20
#2022-04-21 ~ 2022-10-20
#2023-10-21 ~ 2023-04-18

start_date= driver.find_element(By.NAME, "rqstStDt")
start_date.clear()  
start_date.send_keys("2021-04-19") #시작날짜 입력

end_date= driver.find_element(By.NAME, "rqstEndDt")
end_date.clear()  
end_date.send_keys("2021-10-18") #종료날짜 입력

select_button = f'//*[@id="searchBtn"]'
driver.find_element(By.XPATH, select_button).click() #검색 클릭
time.sleep(2)

total = driver.find_element(By.XPATH, f'//*[@id="frm"]/div[2]/span/span').text
print(total) #str

df = pd.DataFrame(columns=['제목', '내용', '작성일자', '답변', '답변일자', '담당부서'])
for i in range(1, int(total)+1):
#
      complain_list = f'//*[@id="frm"]/table/tbody/tr[{i}]/td[2]/a'
      complain_element = wait.until(EC.presence_of_element_located((By.XPATH, complain_list)))
      #print(complain_list)
      driver.find_element(By.XPATH, complain_list).click()
      
      title = driver.find_element(By.XPATH, f'//*[@id="txt"]/div[1]/div[1]/div/div[1]/strong').text
      df.at[i-1, '제목'] = title
      
      text = driver.find_element(By.XPATH, f'//*[@id="txt"]/div[1]/div[1]/div/div[2]').text
      df.at[i-1, '내용'] = text
      
      date = driver.find_element(By.XPATH, f'//*[@id="txt"]/div[1]/div[1]/div/span').text
      df.at[i-1, '작성일자'] = date
      
      answer = driver.find_element(By.XPATH, f'//*[@id="txt"]/div[1]/div[2]/div/div[1]').text
      #df.at[i-1, '답변'] = answer
      
      ans_date = answer.split('\n')
      df.at[i-1, '답변']  = answer.rstrip(ans_date[-1])
      df.at[i-1, '답변일자'] = ans_date[-1]

      department = driver.find_element(By.XPATH, f'//*[@id="txt"]/div[1]/div[2]/div/div[2]/ul/li[1]/dl/dd').text
      df.at[i-1, '담당부서'] = department
      
      time.sleep(3)
      driver.back() #뒤로가기
      df.to_csv('국민신문고_크롤링_1.csv', encoding='utf-8-sig', index=False) #파일명 크롤링_1, 크롤링_2 ..    변경 필요 
df
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

url = '/?'
url2 = 'https://www.epeople.go.kr/nep/prpsl/opnPrpl/opnpblPrpslList.npaid'
header = {'User-Agent': ''}
driver = webdriver.Chrome('./chromedriver.exe') 
driver.implicitly_wait(3)
#driver.get(url)

wait = WebDriverWait(driver, 10)

# 새 탭 열어 링크로 이동 
driver.execute_script('window.open("https://www.epeople.go.kr/nep/prpsl/opnPrpl/opnpblPrpslList.npaid");') 
driver.switch_to.window(driver.window_handles[-1])
driver.get(url2)

req = requests.get(url2,verify=False)
html = req.text 
soup = BeautifulSoup(html, "html.parser")

from selenium.webdriver.support.select import Select

select = Select(driver.find_element(By.ID, "listCnt"))
select.select_by_index(4) #50개보기 선택

select_agency = Select(driver.find_element(By.ID, "searchCd"))
select_agency.select_by_index(2)
# 0. 선택 
# 1. 중앙행정기관
# 2. 지방자치단체
# 3. 시도교육청
time.sleep(1)

select_area = Select(driver.find_element(By.NAME, "searchInstCd"))
select_area.select_by_index(5)
# 0. 선택, 1. 강원도(ok), 2. 경기도(ok), 3. 경상남도, 4. 경상북도
# 5. 광주광역시, 6. 대구광역시(ok), 7. 대전광역시(ok), 8. 부산광역시, 9. 서울특별시
# 10. 세종특별자치시(ok), 11. 울산광역시, 12. 인천광역시(ok), 13. 전라남도(ok), 14. 전라북도(ok)
# 15. 제주특별자치도(ok), 16. 충청남도(ok), 17. 충청북도(ok)

start_date= driver.find_element(By.NAME, "rqstStDt")
start_date.clear()  
start_date.send_keys("2021-09-07") #시작날짜 입력
####################################################
end_date= driver.find_element(By.NAME, "rqstEndDt")
end_date.clear()  
end_date.send_keys("2022-04-19") #종료날짜 입력
#2021-04-19 ~ 2021-10-19
#2021-10-20 ~ 2022-04-20
#2022-04-21 ~ 2022-10-20
#2023-10-21 ~ 2023-04-18

select_button = f'/html/body/div[3]/main/div/section/article/form[2]/div[1]/div[1]/div[4]/button[1]'
driver.find_element(By.XPATH, select_button).click() #검색 클릭
time.sleep(2)

total = driver.find_element(By.XPATH, f'//*[@id="frm"]/div[2]/span/span').text
print(total) #str

df = pd.DataFrame(columns=['제목', '내용', '작성일자', '답변', '답변일자', '처리담당부서', '추진상황'])
for i in range(1, int(total)+1):
#
      complain_list = f'//*[@id="frm"]/table/tbody/tr[{i}]/td[2]/a'
      complain_element = wait.until(EC.presence_of_element_located((By.XPATH, complain_list)))
      #print(complain_list)
      driver.find_element(By.XPATH, complain_list).click()
      
      try:
            title = driver.find_element(By.XPATH, f'/html/body/div[3]/main/div/section/article/div[1]/div/div[1]/div[1]').text
            df.at[i-1, '제목'] = title
      except:
            pass
      try:
            text = driver.find_element(By.XPATH, f'/html/body/div[3]/main/div/section/article/div[1]/div/div[3]').text
            df.at[i-1, '내용'] = text
      except:
            pass
      try:
            date = driver.find_element(By.XPATH, f'/html/body/div[3]/main/div/section/article/div[1]/div/div[4]/div[2]').text
            df.at[i-1, '작성일자'] = date
      except:
            pass
      try:
            answer = driver.find_element(By.XPATH, f'/html/body/div[3]/main/div/section/article/div[2]/div[1]/div[2]/div/div').text
      #df.at[i-1, '답변'] = answer
      except:
            pass
      try:
            ans_date = driver.find_element(By.XPATH, f'/html/body/div[3]/main/div/section/article/div[2]/div[1]/div[1]/div[2]').text
            df.at[i-1, '답변']  = answer.rstrip(ans_date[-1])
            df.at[i-1, '답변일자'] = ans_date
      except:
            pass
      try:
            department_in_charge = driver.find_element(By.XPATH, f'/html/body/div[3]/main/div/section/article/div[1]/div/div[2]/div[2]').text
            df.at[i-1, '처리담당부서'] = department_in_charge
      except:
            pass
      try:
            department = driver.find_element(By.XPATH, f'/html/body/div[3]/main/div/section/article/div[2]/div[1]/div[1]/div[1]').text
            df.at[i-1, '추진상황'] = department
      except:
            pass
      
      time.sleep(3)
      driver.back() #뒤로가기
      df.to_csv('국민신문고_크롤링_.csv', encoding='utf-8-sig', index=False) #파일명 크롤링_1, 크롤링_2 ..    변경 필요 
df
from bs4 import BeautifulSoup
from matplotlib.textpath import text_to_path
import requests, json, re, time, datetime, random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import numpy as np
from tqdm import tqdm
import csv
import sys
import os
import warnings
warnings.filterwarnings('ignore')
from bigkinds_text import get_text
import pymysql

def crawler(date):
      # options=webdriver.ChromeOptions()
      # options.add_argument('headless')
      # service = Service('./chromedriver.exe')
      # driver = webdriver.Chrome(service=service, options=options)

      header = {'User-Agent': ''}
      driver = webdriver.Chrome('./chromedriver.exe')
      driver.implicitly_wait(3)

      url = 'https://www.bigkinds.or.kr/v2/news/index.do'
      driver.get(url)

      press_button = f'/html/body/div[1]/main/div[1]/div[2]/div/div[1]/div[2]/div[3]/div/div[1]/div[3]/a' #언론사 선택
      driver.find_element(By.XPATH, press_button).click()
      time.sleep(2)
      
      press_select2 = driver.find_element(By.XPATH, '//*[@id="경상"]') #경상
      driver.execute_script("arguments[0].click();", press_select2)

      class_button = f'/html/body/div[1]/main/div[1]/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div[1]/a' #통합 분류 선택
      driver.find_element(By.XPATH, class_button).click()
      
      driver.find_element(By.XPATH, f'/html/body/div[1]/main/div[1]/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div[2]/ul/li[1]/div/span[3]').click() #정치
      driver.find_element(By.XPATH, f'/html/body/div[1]/main/div[1]/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div[2]/ul/li[2]/div/span[3]').click() #경제
      driver.find_element(By.XPATH, f'/html/body/div[1]/main/div[1]/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div[2]/ul/li[3]/div/span[3]').click() #사회
      driver.find_element(By.XPATH, f'/html/body/div[1]/main/div[1]/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div[2]/ul/li[4]/div/span[3]').click() #문화
      driver.find_element(By.XPATH, f'/html/body/div[1]/main/div[1]/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div[2]/ul/li[6]/div/span[3]').click() #지역
      time.sleep(2)
      
      date_button = f'/html/body/div[1]/main/div[1]/div[2]/div/div[1]/div[2]/div[3]/div/div[1]/div[1]/a' #기간 선택
      driver.find_element(By.XPATH, date_button).click()
      
      start_date =  driver.find_element(By.ID, 'search-begin-date')
      start_date.click()
      start_date.send_keys(Keys.CONTROL + "A")
      start_date.send_keys(date) #시작

      end_date= driver.find_element(By.ID, "search-end-date")
      end_date.click()
      end_date.send_keys(Keys.CONTROL + "A")
      end_date.send_keys(date)  #종료
      time.sleep(2)


      driver.find_element(By.XPATH, f'//*[@id="search-foot-div"]/div[2]/button[2]').send_keys(Keys.ENTER) #적용
      select = Select(driver.find_element(By.ID, "select2"))
      select.select_by_index(3)

      time.sleep(2)
      total = driver.find_element(By.XPATH, f'//*[@id="news-results-tab"]/div[3]/h3/span[6]').text
      print(total)

      page_count = driver.find_element(By.XPATH, f'//*[@id="news-results-tab"]/div[7]/div[1]/div/div/div/div[3]/div/b').text
      print(page_count)


      result_df = pd.DataFrame(columns=['제목', '언론사', '작성일자', '키워드', '내용', '출처'])
      for page in range(1, int(page_count)+1):
            print(page)
            time.sleep(3)
            if page != 1:
                  try:
                        page_button = f'/html/body/div[1]/main/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[3]/div[7]/div[1]/div/div/div/div[4]/a'
                        driver.find_element(By.XPATH, page_button).click()
                        time.sleep(3)
                  except:
                        page_button = f'//*[@id="news-results-tab"]/div[7]/div[1]/div/div/div/div[4]/a'
                        driver.find_element(By.XPATH, page_button).click()
                        time.sleep(3)

            else:
                  pass

            table = driver.find_element(By.ID, 'news-results')
            rows = table.find_elements(By.CLASS_NAME,"news-item")
            #print(len(rows))

            for i in range(1, len(rows) +1):
                  try:
                        news = driver.find_element(By.XPATH, f'//*[@id="news-results"]/div[{i}]/div/div[2]/div/div/a').text
                        #print(news)

                        complain_list = f'//*[@id="news-results"]/div[{i}]/div/div[2]/a'
                        content = driver.find_element(By.XPATH, complain_list)
                        detail_id = content.get_attribute('data-newsid')
                        detail_url = 'https://www.bigkinds.or.kr/v2/news/newsDetailView.do?newsId=' + detail_id
                        print(detail_url)

                        date = driver.find_element(By.XPATH, f'//*[@id="news-results"]/div[{i}]/div/div[2]/div/p[1]').text
                        date = datetime.strptime(date, '%Y/%m/%d')
                        date = date.strftime('%Y-%m-%d')
                        #print(date)

                        keyword = driver.find_element(By.XPATH, f'/html/body/div[1]/main/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[3]/div[5]/div[{i}]/div/div[2]/div/div/span').text
                        keyword = keyword.split('|')
                        #print(keyword)

                        title =  driver.find_element(By.XPATH, f'//*[@id="news-results"]/div[{i}]/div/div[2]/a/div/strong/span').text
                        #print(title)
                        text = get_text(detail_url)
                        time.sleep(2)
                        result_df = result_df.append({'제목' : title, '언론사' : news,  '작성일자' : date, '키워드' : keyword, '내용' : text, '출처' : detail_url}, ignore_index=True)
                  except:
                        pass
      
      return result_df


if __name__ == "__main__":
      date = '2023-03-31'
      df = crawler(date)
      df.to_csv('빅카인즈_{}.csv'.format(date), index=False)
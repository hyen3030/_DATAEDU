#제주시 공모전 홈페이지에서 프로젝트를 크롤링하여 데이터프레임으로 변환하는 코드.

#크롬 브라우저 창을 열고, selenium을 이용하여 제주시 공모전 홈페이지에 접속.
#requests 모듈을 이용하여 html 페이지 소스를 가져옴. 
#가져온 html 소스를 BeautifulSoup 모듈을 이용하여 파싱. 
#이후, BeautifulSoup 모듈에서 제공하는 find_all 메소드를 사용하여 프로젝트 페이지를 수집=.
#이때, for 문을 이용하여 전체 프로젝트 페이지를 반복적으로 크롤링함. 크롤링한 데이터는 데이터프레임으로 변환하여 저장합니다.

#해당 코드는 Selenium, BeautifulSoup, pandas, numpy, requests 등의 모듈을 사용. 
#주요 변수는 url, header, col, d, xpath_tmp, category, path_more, df, list_tag_issueTit 등입니다.


from selenium import webdriver #크롬 브라우저창(자동화)을 열때 사용하는 모듈.
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep
from inspect import getfile
from urllib import request
from urllib.error import HTTPError
from time import time
import pandas as pd #데이터분석 및 조작을 위한 소프트웨어 라이브러리이다.
import numpy as np #다차원 배열을 쉽게 처리하고 효율적으로 사용할 수 있도록 지원하는 파이썬 라이브러리이다.
import urllib.request
import urllib.parse #한글을 아스키코드로 변환.
import requests #특정 웹사이트에 HTTP 요청을 보내는 모듈.
import re #정규표현 처리를 하기 위해 표준 라이브러리이다.
import os #운영체제에서 제공되는 여러 가지 기능을 파이썬에서 수행할 수 있도록 해주는 모듈.
import csv

import warnings
warnings.filterwarnings('ignore')

#url
address_jejudsi="https://jejudsi.kr/issue.htm" #사이트 주소

### 가치더함 사이트접속
header = {'User-Agent': ''}
d = webdriver.Chrome('./chromedriver.exe') #chromedriver.exe 존재하는 경로
d.implicitly_wait(3)
d.get(address_jejudsi)
req = requests.get(address_jejudsi,verify=False)
html = req.text                                     #HTML소스코드 가져오기
soup = BeautifulSoup(html, "html.parser")           #HTML코드 파싱하기
sleep(2)

""" # 기타 단추 클릭
xpath_click_etc = '/html/body/div[1]/section/div/div/div[2]/div/div/div/div/nav/div[2]/ul/li[9]/a'
etc = d.find_element(By.XPATH,xpath_click_etc).text
d.find_element(By.XPATH,xpath_click_etc).click() """

################################################################## /PROPOSE ##################################################################
for j in range(2, 9+1):
    xpath_tmp = f'/html/body/div[1]/section/div/div/div[2]/div/div/div/div/nav/div[2]/ul/li[{j}]/a'
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

# 더보기 무한 클릭
    path_more ='/html/body/div[1]/section/div/div/div[2]/div/div/div/div/div[7]/div[2]/a'
    while True :
        try :
            d.find_element(By.XPATH,path_more).click()
        except :
            break

# 새로운 데이터프레임 생성
    col = [
        'id 값'                        # 1. id
        ,'page'                         # 페이지(INDEX, PROJECT, PROPOSE, RESPONSE)
        ,'제목'                           # 2. 제목(title)
        ,'분류'                            # 3. 분류(category)
        ,'프로젝트 시작'                     # 4. 기간 - 프로젝트 시작
        ,'프로젝트 종류'                      # 5. 단계 - 프로젝트 종류
        ,'상세 내용'                           # 6. 내용 - 상세내용
        ,'제안의 시작'                          # 7. 내용 - 제안의시작
        ,'주요제안(문제정의)'                     # 8. 내용 - 주요제안(문제정의)
        ,'해결방안'                                # 9. 내용 - 해결방안
        ,'링크'                                      # 10. 출처 - 링크
        ,'미추진 사유'                                 # 11. 기타 - 마주친 사유
        ,'공감투표 참여안내'                             # 12. 기타 - 공감투표 참여안내
        ,'참고자료'                                       # 13. 기타 - 참고자료
        ]
    df = pd.DataFrame(columns=col)

# 프로젝트 진입 주소 수집
    html_2 = d.page_source
    soup_2 = BeautifulSoup(html_2, "html.parser")
    list_issueTit = soup_2.find_all('div', attrs={"class" : "issue-tit"})

    list_tag_issueTit = list() #main /PROJECT(프로젝트Page)
    propose = "/PROPOSE" #sub /PROPOSE(제안Page)
    page = propose.split('/')[-1]

    for j_list_issueTit in list_issueTit :
        list_tag_issueTit.append(j_list_issueTit.a['href'])

    for j_list_tag_issueTit in list_tag_issueTit :

        # 프로젝트 진입
        d.get(f'https://jejudsi.kr{j_list_tag_issueTit}{propose}')
        
        path_link = f'https://jejudsi.kr{j_list_tag_issueTit}{propose}'

        sry = f'https://jejudsi.kr{j_list_tag_issueTit}{propose}에서 데이터를 불러오지 못했습니다.'

        ##### 링크에서 id값 추출 #####
        code = path_link.split('/')[-2]
        upperid = code.upper()
        id = "jejudsi_" + upperid

        # 프로젝트 종류/진행상황
        path_status ='/html/body/div[1]/section/div[1]/div/p[1]/span'
        status = d.find_element(By.XPATH, path_status).text

        # 데이터 불러오지 못할 경우 다음으로 넘기기
        try :
            req = requests.get(address_jejudsi,verify=False)
            html = req.text 
            soup = BeautifulSoup(html, "html.parser")
            sleep(2)
        except:
            pass

        # 프로젝트 시작 시점
        try :        
            path_start = '/html/body/div[1]/section/div[2]/div/div[3]/div[1]/div[1]/div/div[2]/h3'
            start = d.find_element(By.XPATH, path_start).text
            start = start[9:19]
        except :
            start = np.nan

        # a태그에서 href 속성값이 파일 경로인 것만을 찾아보자.
        links = soup.find_all ('a', href = re.compile('\.(pdf|docx|xlsx)$'))
        # 추출한 링크 출력하기.

        # 프로젝트 제목
        title = d.find_element(By.CLASS_NAME, 'text-center').text

        # 내용 수집
        html_test = d.page_source
        soup_test = BeautifulSoup(html_test, "html.parser")

        # mt-3 섹션
        list_test = soup_test.find_all('div', attrs={"class" : "card mt-3"})

        list_list_test = list()
        for j_list_test in list_test :
            cleantext = j_list_test.text
            j_list_test = re.sub("\n|\t", "", cleantext) # \n, \t 삭제
            list_list_test.append(j_list_test)
        list_list_test

        cleantext_reason = list()
        cleantext_content = list()
        cleantext_cuase = list()
        cleantext_suggestion = list()
        cleantext_solution = list()
        cleantext_vote = list()
        cleantext_reference = list()

        for j_list_list_test in list_list_test :
            if '미추진 사유' in j_list_list_test[:15] :
                cleantext_reason.append(j_list_list_test)
            elif '상세 내용' in j_list_list_test[:15] :
                cleantext_content.append(j_list_list_test[6:]) # 6번째 글자부터 저장
            elif '제안의 시작' in j_list_list_test[:15] :
                cleantext_cuase.append(j_list_list_test[14:]) # '제안의 시작(문제정의)[16:]' 빼기
            elif '주요제안' in j_list_list_test[:15] :
                cleantext_suggestion.append(j_list_list_test[12:]) # '주요제안(문제정의)[12:]' 빼기
            elif '해결방안' in j_list_list_test[:15] :
                cleantext_solution.append(j_list_list_test[6:])
            elif '공감투표' in j_list_list_test[:15] :
                cleantext_vote.append(j_list_list_test[10:])
            elif '관련 자료' in j_list_list_test[:15] :
                cleantext_reference.append(j_list_list_test[12:])
            elif '댓글' in j_list_list_test[:15] :
                pass
        else :
            pass

        if not (cleantext_reason and \
              cleantext_content and \
              cleantext_cuase and \
              cleantext_suggestion and \
              cleantext_solution and \
              cleantext_vote and \
              cleantext_reference) :
            
            # mt-t-10 섹션
            # mt-t-10 클래스가 포함된 div 태그들을 찾아서 그 안에 포함된 텍스트 데이터를 추출하고, 
            # 특정 문자열이 포함된 경우 각각의 리스트에 해당 문자열이 포함된 텍스트 데이터를 저장하는 역할을 한다.
            list_test = soup_test.find_all('div', attrs={"class" : "card m-t-10"})

            list_list_test = list()
            for j_list_test in list_test :
                cleantext = j_list_test.text
                j_list_test = re.sub("\n",'', cleantext) # \n 삭제.
                list_list_test.append(j_list_test)
            
            for j_list_list_test in list_list_test :        
                if '미추진 사유' in j_list_list_test[:15] :
                    cleantext_reason.append(j_list_list_test)
                elif '상세 내용' in j_list_list_test[:15] :
                    cleantext_content.append(j_list_list_test[6:])
                elif '제안의 시작' in j_list_list_test[:15] :
                    cleantext_cuase.append(j_list_list_test[14:]) # '제안의 시작(문제정의)[16:]' 빼기
                elif '주요제안' in j_list_list_test[:15] :
                    cleantext_suggestion.append(j_list_list_test[12:]) # '주요제안(문제정의)[12:]' 빼기
                elif '해결방안' in j_list_list_test[:15] :
                    cleantext_solution.append(j_list_list_test[6:])          
                elif '공감투표' in j_list_list_test[:15] :
                    cleantext_vote.append(j_list_list_test[10:])
                elif '관련 자료' in j_list_list_test[:15] :
                    cleantext_reference.append(j_list_list_test[12:])
                elif '댓글' in j_list_list_test[:15] :
                    pass
                else : #그리고 마지막 부분에서는 mt-t-10 클래스가 없는 경우에는 아무 작업도 수행하지 않고 넘어가도록 처리하고 있습니다. 이 부분은 예외 처리를 위한 부분으로, mt-t-10 클래스가 없는 경우에는 해당하는 정보가 없으므로 데이터를 추출하지 않아도 되기 때문.
                    pass
        else :
            pass

        if not cleantext_content :
            cleantext_content = np.nan
        else :
            cleantext_content = cleantext_content[0]
        # cleantext_content(상세 내용)마무리
        if not cleantext_cuase :
            cleantext_cuase = np.nan
        else :
            cleantext_cuase = cleantext_cuase[0]
        # cleantext_cuase(제안의 시작)마무리
        if not cleantext_suggestion :
            cleantext_suggestion = np.nan
        else :
            cleantext_suggestion = cleantext_suggestion[0]
        # cleantext_suggestion(주요제안(문제정의))마무리
        if not cleantext_solution :
            cleantext_solution = np.nan
        else :
            cleantext_solution = cleantext_solution[0]
        # cleantext_solution(해결방안)마무리
        if not cleantext_vote :
            cleantext_vote = np.nan
        else :
            cleantext_vote = cleantext_vote[0]
        # cleantext_vote(공감투표 참여안내)마무리
        if not cleantext_reference :
            cleantext_reference = np.nan
        else :
            cleantext_reference = cleantext_reference[0]
        # cleantext_reference(참고자료)마무리


        # 데이터프레임 df를 csv 파일로 저장하는 코드
        df = pd.read_csv("test_index.csv", encoding="utf-8-sig") # 파일 읽어오기

            # 데이터프레임에 추가
        new_row =   {'id 값' : id                         # 1. id
                    ,'page' : page                       # 페이지
                    ,'제목' : title                         # 2. 제목(title)
                    ,'분류' : category                       # 3. 분류(category)
                    ,'프로젝트 시작' : start                   # 4. 기간 - 프로젝트 시작
                    ,'프로젝트 종류' : status                   # 5. 단계 - 프로젝트 종류
                    ,'상세 내용' : cleantext_content             # 6. 내용 - 상세내용
                    ,'제안의 시작' : cleantext_cuase              # 7. 내용 - 제안의시작
                    ,'주요제안(문제정의)' : cleantext_suggestion    # 8. 내용 - 주요제안(문제정의)
                    ,'해결방안' : cleantext_solution                 # 9. 내용 - 해결방안
                    ,'링크' : path_link                               # 10. 출처 - 링크
                    ,'미추진 사유' : cleantext_reason                   # 11. 기타 - 마주친 사유
                    ,'공감투표 참여안내' : cleantext_vote                 # 12. 기타 - 공감투표 참여안내
                    ,'참고자료' : cleantext_reference                      # 13. 기타 - 참고자료
                }
        
        df = df.append(new_row, ignore_index=True) # 새로운 행 추가

        print(page)
        print("id : " + id + "(" "link : " + path_link + ")")                # 1. id    # 10. 출처 - 링크   
        print("[" + category + "]"" - ""|" + status + "| - " + title)        # 2. 제목(title) # 3. 분류(category) # 5. 단계 - 프로젝트 종류
        print("date : " + str(start))       # 4. 기간 - 프로젝트 시작      
        print("======================")

        # encoding="utf-8-sig"는 csv 파일을 UTF-8 인코딩으로 저장하도록 설정
        df.drop_duplicates(subset=['page', '제목', '분류', '프로젝트 시작', '프로젝트 종류'], inplace=True)

        df = df.append(new_row,ignore_index=True) # 새로운 행 추가D

        # 중복 제거된 데이터 저장하기
        df.to_csv("test_index.csv", encoding="utf-8-sig", index=False)
        # to_csv() 함수를 이용해 df 데이터프레임을 csv 파일로 변환
        
        
        d.back() # d.back()은 이전 페이지로 돌아가는 것
        sleep(1) # 1초간의 지연을 추가
    df # 데이터프레임을 확인

################################################################## /PROJECT ##################################################################
for k in range(2, 9+1):
    
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

# 더보기 무한 클릭
    path_more ='/html/body/div[1]/section/div/div/div[2]/div/div/div/div/div[7]/div[2]/a'
    while True :
        try :
            d.find_element(By.XPATH,path_more).click()
        except :
            break

# 새로운 데이터프레임 생성
    col = [
        'id 값'                        # 1. id
        ,'page'                        # 페이지(INDEX, PROJECT, PROPOSE, RESPONSE)
        ,'제목'                           # 2. 제목(title)
        ,'분류'                            # 3. 분류(category)
        ,'프로젝트 시작'                     # 4. 기간 - 프로젝트 시작
        ,'프로젝트 종류'                      # 5. 단계 - 프로젝트 종류
        ,'상세 내용'                           # 6. 내용 - 상세내용
        ,'제안의 시작'                          # 7. 내용 - 제안의시작
        ,'주요제안(문제정의)'                     # 8. 내용 - 주요제안(문제정의)
        ,'해결방안'                                # 9. 내용 - 해결방안
        ,'링크'                                      # 10. 출처 - 링크
        ,'미추진 사유'                                 # 11. 기타 - 마주친 사유
        ,'공감투표 참여안내'                             # 12. 기타 - 공감투표 참여안내
        ,'참고자료'                                       # 13. 기타 - 참고자료
        ]
    df = pd.DataFrame(columns=col)

# 프로젝트 진입 주소 수집
    html_2 = d.page_source
    soup_2 = BeautifulSoup(html_2, "html.parser")
    list_issueTit = soup_2.find_all('div', attrs={"class" : "issue-tit"})

    list_tag_issueTit = list()
    project = "/PROJECT" #sub /PROJECT(제안Page)
    page = project.split('/')[-1]

    for k_list_issueTit in list_issueTit :
        list_tag_issueTit.append(k_list_issueTit.a['href'])

    for k_list_tag_issueTit in list_tag_issueTit :

        # 프로젝트 진입
        d.get(f'https://jejudsi.kr{k_list_tag_issueTit}{project}')
        
        path_link = f'https://jejudsi.kr{k_list_tag_issueTit}{project}'

        ##### 링크에서 id값 추출 #####
        code = path_link.split('/')[-2]
        upperid = code.upper()
        id = "jejudsi_" + upperid

        # 프로젝트 종류/진행상황
        path_status ='/html/body/div[1]/section/div[1]/div/p[1]/span'
        try :
            req = requests.get(path_status,verify=False)
            html = req.text
            soup = BeautifulSoup(html, "html.parser")
        except:
            pass

        # 데이터 불러오지 못할 경우 다음으로 넘기기
        try:
            status = d.find_element(By.XPATH, path_status).text
        except:
            pass

        # 데이터 불러오지 못할 경우 다음으로 넘기기
        try :
            req = requests.get(address_jejudsi,verify=False)
            html = req.text 
            soup = BeautifulSoup(html, "html.parser")
            sleep(2)
        except:
            pass

        # 프로젝트 시작 시점
        try :
            d.get(f'https://jejudsi.kr{k_list_tag_issueTit}')
            path_link = f'https://jejudsi.kr{k_list_tag_issueTit}'

            path_start = '/html/body/div[1]/section/div[2]/div/div[3]/div[1]/div[1]/div/div[2]/h3'
            start = d.find_element(By.XPATH, path_start).text
            start = start[9:19]
        except :
            start = np.nan

        # a태그에서 href 속성값이 파일 경로인 것만을 찾아보자.
        links = soup.find_all ('a', href = re.compile('\.(pdf|docx|xlsx)$'))
        # 추출한 링크 출력하기.
        print(links)

        # 프로젝트 제목
        title = d.find_element(By.CLASS_NAME, 'text-center').text

        if (title == np.nan) :
            title = "페이지 없음."
        else :
            pass

        # 내용 수집
        html_test = d.page_source
        soup_test = BeautifulSoup(html_test, "html.parser")

        # mt-3 섹션
        list_test = soup_test.find_all('div', attrs={"class" : "card mt-3"})

        list_list_test = list()
        for k_list_test in list_test :
            cleantext = k_list_test.text
            k_list_test = re.sub("\n|\t", "", cleantext) # \n, \t 삭제
            list_list_test.append(k_list_test)
        list_list_test

        cleantext_reason = list()
        cleantext_content = list()
        cleantext_cuase = list()
        cleantext_suggestion = list()
        cleantext_solution = list()
        cleantext_vote = list()
        cleantext_reference = list()

        for k_list_list_test in list_list_test :
            if '미추진 사유' in k_list_list_test[:15] :
                cleantext_reason.append(k_list_list_test)
            elif '상세 내용' in k_list_list_test[:15] :
                cleantext_content.append(k_list_list_test[6:]) # 6번째 글자부터 저장
            elif '제안의 시작' in k_list_list_test[:15] :
                cleantext_cuase.append(k_list_list_test[14:]) # '제안의 시작(문제정의)[16:]' 빼기
            elif '주요제안' in k_list_list_test[:15] :
                cleantext_suggestion.append(k_list_list_test[12:]) # '주요제안(문제정의)[12:]' 빼기
            elif '해결방안' in k_list_list_test[:15] :
                cleantext_solution.append(k_list_list_test[6:])
            elif '공감투표' in k_list_list_test[:15] :
                cleantext_vote.append(k_list_list_test[10:])
            elif '관련 자료' in k_list_list_test[:15] :
                cleantext_reference.append(k_list_list_test[12:])
            elif '댓글' in k_list_list_test[:15] :
                pass
        else :
            pass

        if not (cleantext_reason and \
              cleantext_content and \
              cleantext_cuase and \
              cleantext_suggestion and \
              cleantext_solution and \
              cleantext_vote and \
              cleantext_reference) :
            
            # mt-t-10 섹션
            # mt-t-10 클래스가 포함된 div 태그들을 찾아서 그 안에 포함된 텍스트 데이터를 추출하고, 
            # 특정 문자열이 포함된 경우 각각의 리스트에 해당 문자열이 포함된 텍스트 데이터를 저장하는 역할을 한다.
            list_test = soup_test.find_all('div', attrs={"class" : "card m-t-10"})

            list_list_test = list()
            for k_list_test in list_test :
                cleantext = k_list_test.text
                k_list_test = re.sub("\n",'', cleantext) # \n 삭제.
                list_list_test.append(k_list_test)
            
            for k_list_list_test in list_list_test :        
                if '미추진 사유' in k_list_list_test[:15] :
                    cleantext_reason.append(k_list_list_test)
                elif '상세 내용' in k_list_list_test[:15] :
                    cleantext_content.append(k_list_list_test[6:])
                elif '제안의 시작' in k_list_list_test[:15] :
                    cleantext_cuase.append(k_list_list_test[14:]) # '제안의 시작(문제정의)[16:]' 빼기
                elif '주요제안' in k_list_list_test[:15] :
                    cleantext_suggestion.append(k_list_list_test[12:]) # '주요제안(문제정의)[12:]' 빼기
                elif '해결방안' in k_list_list_test[:15] :
                    cleantext_solution.append(k_list_list_test[6:])          
                elif '공감투표' in k_list_list_test[:15] :
                    cleantext_vote.append(k_list_list_test[10:])
                elif '관련 자료' in k_list_list_test[:15] :
                    cleantext_reference.append(k_list_list_test[12:])
                elif '댓글' in k_list_list_test[:15] :
                    pass
                else : #그리고 마지막 부분에서는 mt-t-10 클래스가 없는 경우에는 아무 작업도 수행하지 않고 넘어가도록 처리하고 있습니다. 이 부분은 예외 처리를 위한 부분으로, mt-t-10 클래스가 없는 경우에는 해당하는 정보가 없으므로 데이터를 추출하지 않아도 되기 때문.
                    pass
        else :
            pass

        if not cleantext_content :
            cleantext_content = np.nan
        else :
            cleantext_content = cleantext_content[0]
        # cleantext_content(상세 내용)마무리
        if not cleantext_cuase :
            cleantext_cuase = np.nan
        else :
            cleantext_cuase = cleantext_cuase[0]
        # cleantext_cuase(제안의 시작)마무리
        if not cleantext_suggestion :
            cleantext_suggestion = np.nan
        else :
            cleantext_suggestion = cleantext_suggestion[0]
        # cleantext_suggestion(주요제안(문제정의))마무리
        if not cleantext_solution :
            cleantext_solution = np.nan
        else :
            cleantext_solution = cleantext_solution[0]
        # cleantext_solution(해결방안)마무리
        if not cleantext_vote :
            cleantext_vote = np.nan
        else :
            cleantext_vote = cleantext_vote[0]
        # cleantext_vote(공감투표 참여안내)마무리
        if not cleantext_reference :
            cleantext_reference = np.nan
        else :
            cleantext_reference = cleantext_reference[0]
        # cleantext_reference(참고자료)마무리

            # 데이터프레임에 추가
            new_row =   {
                        'id 값' : id                         # 1. id
                    ,'page' : page                       # 페이지
                    ,'제목' : title                         # 2. 제목(title)
                    ,'분류' : category                       # 3. 분류(category)
                    ,'프로젝트 시작' : start                   # 4. 기간 - 프로젝트 시작
                    ,'프로젝트 종류' : status                   # 5. 단계 - 프로젝트 종류
                    ,'상세 내용' : cleantext_content             # 6. 내용 - 상세내용
                    ,'제안의 시작' : cleantext_cuase              # 7. 내용 - 제안의시작
                    ,'주요제안(문제정의)' : cleantext_suggestion    # 8. 내용 - 주요제안(문제정의)
                    ,'해결방안' : cleantext_solution                 # 9. 내용 - 해결방안
                    ,'링크' : path_link                               # 10. 출처 - 링크
                    ,'미추진 사유' : cleantext_reason                   # 11. 기타 - 마주친 사유
                    ,'공감투표 참여안내' : cleantext_vote                 # 12. 기타 - 공감투표 참여안내
                    ,'참고자료' : cleantext_reference                      # 13. 기타 - 참고자료
                    }
        
            df = df.append(new_row, ignore_index=True) # 새로운 행 추가

            print(page)
            print("id : " + id + "(" "link : " + path_link + ")")                # 1. id    # 10. 출처 - 링크   
            print("[" + category + "]"" - ""|" + status + "| - " + title)        # 2. 제목(title) # 3. 분류(category) # 5. 단계 - 프로젝트 종류
            print("date : " + str(start))       # 4. 기간 - 프로젝트 시작      
            print("======================")

            # 데이터프레임 df를 csv 파일로 저장하는 코드
            df = pd.read_csv("test_index.csv", encoding="utf-8-sig") # 파일 읽어오기
            # encoding="utf-8-sig"는 csv 파일을 UTF-8 인코딩으로 저장하도록 설정
            df.drop_duplicates(subset=['page', '제목', '분류', '프로젝트 시작', '프로젝트 종류'])

            df = df.append(new_row,ignore_index=True) # 새로운 행 추가

            # 중복 제거된 데이터 저장하기
            df.to_csv("test_index.csv", encoding="utf-8-sig", index=False)
            # to_csv() 함수를 이용해 df 데이터프레임을 csv 파일로 변환

            d.back() # d.back()은 이전 페이지로 돌아가는 것
            sleep(1) # 1초간의 지연을 추가
    df # 데이터프레임을 확인


################################################################## /RESPONSE ##################################################################
for l in range(2, 9+1):
    xpath_tmp = f'/html/body/div[1]/section/div/div/div[2]/div/div/div/div/nav/div[2]/ul/li[{l}]/a'
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

# 더보기 무한 클릭
    path_more ='/html/body/div[1]/section/div/div/div[2]/div/div/div/div/div[7]/div[2]/a'
    while True :
        try :
            d.find_element(By.XPATH,path_more).click()
        except :
            break

# 새로운 데이터프레임 생성
    col = [
        'id 값'                        # 1. id
        ,'page'                         # 페이지(INDEX, PROJECT, PROPOSE, RESPONSE)
        ,'제목'                           # 2. 제목(title)
        ,'분류'                            # 3. 분류(category)
        ,'프로젝트 시작'                     # 4. 기간 - 프로젝트 시작
        ,'프로젝트 종류'                      # 5. 단계 - 프로젝트 종류
        ,'상세 내용'                           # 6. 내용 - 상세내용
        ,'제안의 시작'                          # 7. 내용 - 제안의시작
        ,'주요제안(문제정의)'                     # 8. 내용 - 주요제안(문제정의)
        ,'해결방안'                                # 9. 내용 - 해결방안
        ,'링크'                                      # 10. 출처 - 링크
        ,'미추진 사유'                                 # 11. 기타 - 마주친 사유
        ,'공감투표 참여안내'                             # 12. 기타 - 공감투표 참여안내
        ,'참고자료'                                       # 13. 기타 - 참고자료
        ]
    df = pd.DataFrame(columns=col)

# 프로젝트 진입 주소 수집
    html_2 = d.page_source
    soup_2 = BeautifulSoup(html_2, "html.parser")
    list_issueTit = soup_2.find_all('div', attrs={"class" : "issue-tit"})

    list_tag_issueTit = list()
    response = "/RESPONSE" #sub /RESPONSE(제안Page)
    page = response.split('/')[-1]

    for l_list_issueTit in list_issueTit :
        list_tag_issueTit.append(l_list_issueTit.a['href'])

    for l_list_tag_issueTit in list_tag_issueTit :

        # 프로젝트 진입
        d.get(f'https://jejudsi.kr{l_list_tag_issueTit}{response}')
        
        path_link = f'https://jejudsi.kr{l_list_tag_issueTit}{response}'

        sry = f'https://jejudsi.kr{l_list_tag_issueTit}{response}에서 데이터를 불러오지 못했습니다.'

        ##### 링크에서 id값 추출 #####
        code = path_link.split('/')[-2]
        upperid = code.upper()
        id = "jejudsi_" + upperid

        # 프로젝트 종류/진행상황
        # 데이터 불러오지 못할 경우 다음으로 넘기기
        path_status ='/html/body/div[1]/section/div[1]/div/p[1]/span'
        try :
            req = requests.get(path_status,verify=False)
            html = req.text
            soup = BeautifulSoup(html, "html.parser")
        except:
            pass
        
        # 데이터 불러오지 못할 경우 다음으로 넘기기
        try:
            status = d.find_element(By.XPATH, path_status).text
            sleep(2)
        except:
            pass

        # 데이터 불러오지 못할 경우 다음으로 넘기기
        try :
            req = requests.get(address_jejudsi,verify=False)
            html = req.text 
            soup = BeautifulSoup(html, "html.parser")
            sleep(2)
        except:
            pass

        # 프로젝트 시작 시점
        try :        
            path_start = '/html/body/div[1]/section/div[2]/div/div[3]/div[1]/div[1]/div/div[2]/h3'
            start = d.find_element(By.XPATH, path_start).text
            start = start[9:19]
        except :
            start = np.nan

        # a태그에서 href 속성값이 파일 경로인 것만을 찾아보자.
        links = soup.find_all ('a', href = re.compile('\.(pdf|docx|xlsx)$'))
        # 추출한 링크 출력하기.

        # 프로젝트 제목
        title = d.find_element(By.CLASS_NAME, 'text-center').text

        if (title == np.nan) :
            title = "페이지 없음."
        else :
            pass

        # 내용 수집
        html_test = d.page_source
        soup_test = BeautifulSoup(html_test, "html.parser")

        # mt-3 섹션
        list_test = soup_test.find_all('div', attrs={"class" : "card mt-3"})

        list_list_test = list()
        for l_list_test in list_test :
            cleantext = l_list_test.text
            l_list_test = re.sub("\n|\t", "", cleantext) # \n, \t 삭제
            list_list_test.append(l_list_test)
        list_list_test

        cleantext_reason = list()
        cleantext_content = list()
        cleantext_cuase = list()
        cleantext_suggestion = list()
        cleantext_solution = list()
        cleantext_vote = list()
        cleantext_reference = list()

        for l_list_list_test in list_list_test :
            if '미추진 사유' in l_list_list_test[:15] :
                cleantext_reason.append(l_list_list_test)
            elif '상세 내용' in l_list_list_test[:15] :
                cleantext_content.append(l_list_list_test[6:]) # 6번째 글자부터 저장
            elif '제안의 시작' in l_list_list_test[:15] :
                cleantext_cuase.append(l_list_list_test[14:]) # '제안의 시작(문제정의)[16:]' 빼기
            elif '주요제안' in l_list_list_test[:15] :
                cleantext_suggestion.append(l_list_list_test[12:]) # '주요제안(문제정의)[12:]' 빼기
            elif '해결방안' in l_list_list_test[:15] :
                cleantext_solution.append(l_list_list_test[6:])
            elif '공감투표' in l_list_list_test[:15] :
                cleantext_vote.append(l_list_list_test[10:])
            elif '관련 자료' in l_list_list_test[:15] :
                cleantext_reference.append(l_list_list_test[12:])
            elif '댓글' in l_list_list_test[:15] :
                pass
        else :
            pass

        if not (cleantext_reason and \
              cleantext_content and \
              cleantext_cuase and \
              cleantext_suggestion and \
              cleantext_solution and \
              cleantext_vote and \
              cleantext_reference) :
            
            # mt-t-10 섹션
            # mt-t-10 클래스가 포함된 div 태그들을 찾아서 그 안에 포함된 텍스트 데이터를 추출하고, 
            # 특정 문자열이 포함된 경우 각각의 리스트에 해당 문자열이 포함된 텍스트 데이터를 저장하는 역할을 한다.
            list_test = soup_test.find_all('div', attrs={"class" : "card m-t-10"})

            list_list_test = list()
            for l_list_test in list_test :
                cleantext = l_list_test.text
                l_list_test = re.sub("\n",'', cleantext) # \n 삭제.
                list_list_test.append(l_list_test)
            
            for l_list_list_test in list_list_test :        
                if '미추진 사유' in l_list_list_test[:15] :
                    cleantext_reason.append(l_list_list_test)
                elif '상세 내용' in l_list_list_test[:15] :
                    cleantext_content.append(l_list_list_test[6:])
                elif '제안의 시작' in l_list_list_test[:15] :
                    cleantext_cuase.append(l_list_list_test[14:]) # '제안의 시작(문제정의)[16:]' 빼기
                elif '주요제안' in l_list_list_test[:15] :
                    cleantext_suggestion.append(l_list_list_test[12:]) # '주요제안(문제정의)[12:]' 빼기
                elif '해결방안' in l_list_list_test[:15] :
                    cleantext_solution.append(l_list_list_test[6:])          
                elif '공감투표' in l_list_list_test[:15] :
                    cleantext_vote.append(l_list_list_test[10:])
                elif '관련 자료' in l_list_list_test[:15] :
                    cleantext_reference.append(l_list_list_test[12:])
                elif '댓글' in l_list_list_test[:15] :
                    pass
                else : #그리고 마지막 부분에서는 mt-t-10 클래스가 없는 경우에는 아무 작업도 수행하지 않고 넘어가도록 처리하고 있습니다. 이 부분은 예외 처리를 위한 부분으로, mt-t-10 클래스가 없는 경우에는 해당하는 정보가 없으므로 데이터를 추출하지 않아도 되기 때문.
                    pass
        else :
            pass

        if not cleantext_content :
            cleantext_content = np.nan
        else :
            cleantext_content = cleantext_content[0]
        # cleantext_content(상세 내용)마무리
        if not cleantext_cuase :
            cleantext_cuase = np.nan
        else :
            cleantext_cuase = cleantext_cuase[0]
        # cleantext_cuase(제안의 시작)마무리
        if not cleantext_suggestion :
            cleantext_suggestion = np.nan
        else :
            cleantext_suggestion = cleantext_suggestion[0]
        # cleantext_suggestion(주요제안(문제정의))마무리
        if not cleantext_solution :
            cleantext_solution = np.nan
        else :
            cleantext_solution = cleantext_solution[0]
        # cleantext_solution(해결방안)마무리
        if not cleantext_vote :
            cleantext_vote = np.nan
        else :
            cleantext_vote = cleantext_vote[0]
        # cleantext_vote(공감투표 참여안내)마무리
        if not cleantext_reference :
            cleantext_reference = np.nan
        else :
            cleantext_reference = cleantext_reference[0]
        # cleantext_reference(참고자료)마무리

            # 데이터프레임에 추가
        new_row =   {'id 값' : id                         # 1. id
                    ,'page' : page                       # 페이지
                    ,'제목' : title                         # 2. 제목(title)
                    ,'분류' : category                       # 3. 분류(category)
                    ,'프로젝트 시작' : start                   # 4. 기간 - 프로젝트 시작
                    ,'프로젝트 종류' : status                   # 5. 단계 - 프로젝트 종류
                    ,'상세 내용' : cleantext_content             # 6. 내용 - 상세내용
                    ,'제안의 시작' : cleantext_cuase              # 7. 내용 - 제안의시작
                    ,'주요제안(문제정의)' : cleantext_suggestion    # 8. 내용 - 주요제안(문제정의)
                    ,'해결방안' : cleantext_solution                 # 9. 내용 - 해결방안
                    ,'링크' : path_link                               # 10. 출처 - 링크
                    ,'미추진 사유' : cleantext_reason                   # 11. 기타 - 마주친 사유
                    ,'공감투표 참여안내' : cleantext_vote                 # 12. 기타 - 공감투표 참여안내
                    ,'참고자료' : cleantext_reference                      # 13. 기타 - 참고자료
                    }
        
        df = df.append(new_row, ignore_index=True) # 새로운 행 추가

        print(page)
        print("id : " + id + "(" "link : " + path_link + ")")                # 1. id    # 10. 출처 - 링크   
        print("[" + category + "]"" - ""|" + status + "| - " + title)        # 2. 제목(title) # 3. 분류(category) # 5. 단계 - 프로젝트 종류
        print("date : " + str(start))       # 4. 기간 - 프로젝트 시작      
        print("======================")

        # 데이터프레임 df를 csv 파일로 저장하는 코드
        df = pd.read_csv("test_index.csv", encoding="utf-8-sig") # 파일 읽어오기
        # encoding="utf-8-sig"는 csv 파일을 UTF-8 인코딩으로 저장하도록 설정
        df.drop_duplicates(subset=['page', '제목', '분류', '프로젝트 시작', '프로젝트 종류'])

        df = df.append(new_row,ignore_index=True) # 새로운 행 추가

        # 중복 제거된 데이터 저장하기
        df.to_csv("test_index.csv", encoding="utf-8-sig", index=False)
        # to_csv() 함수를 이용해 df 데이터프레임을 csv 파일로 변환
        
        d.back() # d.back()은 이전 페이지로 돌아가는 것
        sleep(1) # 1초간의 지연을 추가
    df # 데이터프레임을 확인

""" /제주 가치더함
1. id
2. 제목(title)
3. 분류(category)
4. 기간 - 프로젝트 시작
5. 단계 - 프로젝트 종류
6. 내용 - 상세내용
7. 내용 - 제안의시작
8. 내용 - 주요제안(문제정의)
9. 내용 - 해결방안
10. 출처 - 링크
11. 기타 - 마주친 사유
12. 기타 - 공감투표 참여안내
13. 기타 - 참고자료 """
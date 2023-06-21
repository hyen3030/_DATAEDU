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


################################################################## /PROJECT ##################################################################
for k in range(2, 9+1):
    xpath_tmp = f'/html/body/div[1]/section/div/div/div[2]/div/div/div/div/nav/div[2]/ul/li[{k}]/a'
    sleep(3)
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
            new_row = {
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
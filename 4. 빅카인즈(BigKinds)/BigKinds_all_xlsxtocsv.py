import pandas as pd
import glob
import os

# 통합할 csv파일이 있는 폴더의 경로
folder_path = 'E:/ICT인턴쉽/2023-1/보고서 작성_프로젝트 폴더/_빅카인즈/세계일보'
xlsx_files = [file for file in os.listdir(folder_path) if file.endswith('.xlsx')]

all_files = glob.glob(folder_path + "/*.csv")  # 수정한 부분: "/" 추가

# 각 xlsx 파일을 csv 파일로 변환
for file in xlsx_files:
    # xlsx 파일 읽기
    file_path = os.path.join(folder_path, file)
    xlsx_file = pd.read_excel(file_path)
    
    # csv 파일 쓰기
    csv_file = os.path.join(folder_path, f'{os.path.splitext(file)[0]}.csv')
    xlsx_file.to_csv(csv_file, encoding='utf-8-sig', index=None, header=True)


""" df = pd.DataFrame({
    '뉴스식별자',
    '일자',
    '언론사',
    '기고자',
    '제목',
    '통합 분류1',
    '통합 분류2',
    '통합 분류3',
    '사건/사고 분류1',
    '사건/사고 분류2',
    '사건/사고 분류3',
    '인물',
    '위치',
    '기관',
    '키워드',
    '특성추출(가중치순 상위 50개)',
    '본문',
    'URL',
    '분석제외 여부'
})

df_list = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header = 0)
    df_list.append(df)

if len(df_list) > 0:
    merged_df = pd.concat(df_list, axis=0, ignore_index=True)
    merged_df.to_cs('merged.csv', index=False)
else:
    print("Error : No dataframe to concatenate")

 """


#all_files = glob.glob(folder_path + "E:\ICT인턴쉽\2023-1\보고서 작성_프로젝트 폴더\_빅카인즈\국민일보") #국민일보
#all_files = glob.glob(folder_path + "E:\ICT인턴쉽\2023-1\보고서 작성_프로젝트 폴더\_빅카인즈\내일신문") #내일신문
#all_files = glob.glob(folder_path + "E:\ICT인턴쉽\2023-1\보고서 작성_프로젝트 폴더\_빅카인즈\동아일보") #동아일보
#all_files = glob.glob(folder_path + "E:\ICT인턴쉽\2023-1\보고서 작성_프로젝트 폴더\_빅카인즈\문화일보") #문화일보
#all_files = glob.glob(folder_path + "E:\ICT인턴쉽\2023-1\보고서 작성_프로젝트 폴더\_빅카인즈\서울신문") #서울신문

#all_files = glob.glob(folder_path + "E:\ICT인턴쉽\2023-1\보고서 작성_프로젝트 폴더\_빅카인즈\세계일보") #세계일보
#all_files = glob.glob(folder_path + "E:\ICT인턴쉽\2023-1\보고서 작성_프로젝트 폴더\_빅카인즈\조선일보") #조선일보
#all_files = glob.glob(folder_path + "E:\ICT인턴쉽\2023-1\보고서 작성_프로젝트 폴더\_빅카인즈\중앙일보") #중앙일보
#all_files = glob.glob(folder_path + "E:\ICT인턴쉽\2023-1\보고서 작성_프로젝트 폴더\_빅카인즈\한겨레") #한겨레
import pandas as pd
import glob
import os

# 통합할 csv파일이 있는 폴더의 경로
folder_path = 'E:/ICT인턴쉽/2023-1/보고서 작성_프로젝트 폴더/국민신문고'

all_files = glob.glob(folder_path + "/*.csv")  # 수정한 부분: "/" 추가

df_list = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0, encoding='utf-8-sig', engine='python')  # engine='python' 추가
    df_list.append(df)

if len(df_list) > 0:
    merged_df = pd.concat(df_list, axis=0, ignore_index=True)
    merged_df.to_csv('경주시-국민신문고.csv', encoding='utf-8-sig', index=False)
else:
    print("Error : No dataframe to concatenate")
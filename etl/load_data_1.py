import pandas as pd
import glob
import os

folder_path=BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PROCESSED_DIR = os.path.join(BASE_DIR, 'processed')

file_paths = glob.glob(os.path.join(DATA_DIR, '*2020*.xlsx'))
# dfs = [pd.read_excel(file, skiprows=3).iloc[:,:9] for file in file_paths]
# df = pd.concat(dfs, ignore_index=True)
# df.to_csv('final_data_1.csv', index=False, encoding='utf-8-sig')
# df = pd.read_csv('final_data_1.csv')
# print("CSV 파일 저장 완료!")

# import os
# print(os.getcwd())
for file in file_paths:
    dfs = pd.read_excel(file).iloc[:,:9]
    dfs.to_excel(file,index=False)

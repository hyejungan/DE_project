import pandas as pd
import glob
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
DATA_DIR = os.path.join(BASE_DIR, 'data')
PROCESSED_DIR = os.path.join(BASE_DIR, 'processed')

file_paths = glob.glob(os.path.join(DATA_DIR, '*.xlsx'))
dfs = [pd.read_excel(file, skiprows=3) for file in file_paths]
df = pd.concat(dfs, ignore_index=True)

# 한글 인코딩 깨짐 방지
df.to_csv(os.path.join(PROCESSED_DIR, 'final_data.csv'), index=False, encoding='utf-8-sig')

# 이후 불러오기
df = pd.read_csv(os.path.join(PROCESSED_DIR, 'final_data.csv'))

import pandas as pd
import glob
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
DATA_DIR = os.path.join(BASE_DIR, 'data')
PROCESSED_DIR = os.path.join(BASE_DIR, 'processed')

file_paths = glob.glob(os.path.join(DATA_DIR, '*.xlsx'))
dfs = [pd.read_excel(file, skiprows=3) for file in file_paths]
df = pd.concat(dfs, ignore_index=True)

df.to_csv(os.path.join(PROCESSED_DIR, 'final_data.csv'), index=False)

# 다음엔 이걸 바로 불러와서 분석/모델링
df = pd.read_csv(os.path.join(PROCESSED_DIR, 'final_data.csv'))
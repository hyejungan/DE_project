import pandas as pd

df = pd.read_csv('processed/final_data.csv')
print(df.info())
print(df.describe())
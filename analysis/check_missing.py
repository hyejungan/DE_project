import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def detect_outliers_iqr(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower) | (df[col] > upper)]
    print(f"[{col}] 이상치 수: {len(outliers)}")
    return outliers

df = pd.read_csv('../processed/final_data.csv')
cols_to_check = ['환자수', '내원일수', '청구건수', '요양급여비용총액', '보험자부담금']

for col in cols_to_check:
    detect_outliers_iqr(df, col)

for col in cols_to_check:
    plt.figure(figsize=(8, 4))
    sns.boxplot(x=df[col])
    plt.title(f'{col} 이상치 시각화')
    plt.show()
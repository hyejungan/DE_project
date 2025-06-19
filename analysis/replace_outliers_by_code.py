import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('../processed/final_data.csv')

cols_to_check = ['환자수', '내원일수', '청구건수', '요양급여비용총액', '보험자부담금']

df_cleaned = df.copy()

for code, group in df.groupby('코드'):
    for col in cols_to_check:
        Q1 = group[col].quantile(0.25)
        Q3 = group[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        indices = group.index

        below_idx = df_cleaned.loc[indices][df_cleaned.loc[indices][col] < lower].index
        df_cleaned.loc[below_idx, col] = lower

        above_idx = df_cleaned.loc[indices][df_cleaned.loc[indices][col] > upper].index
        df_cleaned.loc[above_idx, col] = upper

def count_outliers_groupwise(df, group_col, col):
    count = 0
    for _, group in df.groupby(group_col):
        Q1 = group[col].quantile(0.25)
        Q3 = group[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        out = group[(group[col] < lower) | (group[col] > upper)]
        count += len(out)
    return count

for col in cols_to_check:
    count = count_outliers_groupwise(df_cleaned, '코드', col)
    print(f"{col} 이상치 수 (그룹 기준): {count}")

for col in cols_to_check:
    plt.figure(figsize=(6, 4))
    sns.boxplot(x=df_cleaned[col])
    plt.title(f'{col} 사분위수 및 이상치 확인')
    plt.xlabel(col)
    plt.grid(True)
    plt.show()

#이상치 대치 완료 후 새 파일로 저장
df_cleaned.to_csv('../processed/final_data_outliers_replaced.csv', index=False)
print("✅ 이상치 대치된 데이터 저장 완료: final_data_outliers_replaced.csv")

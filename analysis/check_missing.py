import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 로딩
df = pd.read_csv('processed/final_data.csv')

# 분석 대상 수치형 컬럼
cols_to_check = ['환자수', '내원일수', '청구건수', '요양급여비용총액', '보험자부담금', '환자부담금','연도']

# 1. 결측치 확인
print("✅ 결측치 확인:")
missing = df.isnull().sum()
missing = missing[missing > 0]
if not missing.empty:
    for col, count in missing.items():
        print(f"{col} : {count}개")
else:
    print("결측치 없음")

# 2. 중복 확인
print("\n✅ 중복 행 확인:")
duplicates = df[df.duplicated()]
print(f"중복된 행 수: {len(duplicates)}")
if not duplicates.empty:
    print("중복된 데이터 샘플:")
    print(duplicates.head())

# 3. 전체 이상치 탐지 (IQR)
def detect_outliers_iqr(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower) | (df[col] > upper)]
    # print(f"[{col}] 이상치 수: {len(outliers)}")
    return outliers

all_outliers = []

print("\n✅ 전체 데이터 기준 이상치 탐지:")
for col in cols_to_check:
    outliers = detect_outliers_iqr(df, col)
    if not outliers.empty:
        temp = outliers.copy()
        temp['이상치컬럼'] = col
        all_outliers.append(temp)

# 전체 이상치 저장
if all_outliers:
    all_outliers_df = pd.concat(all_outliers).drop_duplicates()
    all_outliers_df.to_csv('processed/all_outliers.csv', index=False, encoding='utf-8-sig')
    print("\n[완료] 전체 이상치 파일: 'processed/all_outliers.csv'")
else:
    print("전체 이상치 없음.")

# 4. 이상치 시각화
for col in cols_to_check:
    plt.figure(figsize=(8, 4))
    sns.boxplot(x=df[col])
    plt.title(f'{col} 이상치 시각화')
    plt.show()

# 5. 진단코드별 이상치 탐지 (출력은 개수 요약만)
grouped_outliers = []
grouped = df.groupby('코드')
grouped_outlier_count = 0

print("\n✅ 진단코드별 이상치 탐지 중...")

for code, group in grouped:
    for col in cols_to_check:
        Q1 = group[col].quantile(0.25)
        Q3 = group[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = group[(group[col] < lower) | (group[col] > upper)]

        if not outliers.empty:
            grouped_outlier_count += len(outliers)
            temp = outliers.copy()
            temp['이상치컬럼'] = col
            grouped_outliers.append(temp)

# 저장 및 최종 요약
if grouped_outliers:
    grouped_outliers_df = pd.concat(grouped_outliers).drop_duplicates()
    grouped_outliers_df.to_csv('processed/grouped_outliers_by_code.csv', index=False, encoding='utf-8-sig')
    print(f"\n[완료] 진단코드별 이상치 총합: {len(grouped_outliers_df)}개")
    print("저장 경로: 'processed/grouped_outliers_by_code.csv'")
else:
    print("진단코드별 이상치 없음.")

# 6. 진단코드별 이상치 중복 여부 확인
if grouped_outliers:
    duplicates_in_grouped = grouped_outliers_df[grouped_outliers_df.duplicated()]
    print("\n✅ 진단코드별 이상치 데이터 중 중복 확인:")
    print(f"중복된 행 수: {len(duplicates_in_grouped)}")
    
    if not duplicates_in_grouped.empty:
        print("중복된 행 샘플:")
        print(duplicates_in_grouped.head())
        
        # 중복 데이터 따로 저장
        duplicates_in_grouped.to_csv('processed/duplicates_in_grouped_outliers.csv', index=False, encoding='utf-8-sig')
        print("중복 이상치 저장됨: 'processed/duplicates_in_grouped_outliers.csv'")
    else:
        print("중복된 행 없음.")

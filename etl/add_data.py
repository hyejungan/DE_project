import pandas as pd
import glob
import os
import re

# 1. 현재 스크립트 기준으로 data 폴더 경로 설정
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

# 2. 엑셀 파일 목록 가져오기 (지정된 패턴에 맞는 파일만)
file_list = glob.glob(os.path.join(base_path, "다빈도질병통계_질별연령별10세구간별_*.xlsx"))

# 3. 각 파일 처리
for file_path in file_list:
    file_name = os.path.basename(file_path)  # 파일명만 추출

    # 3-1. 정규표현식으로 연도(4자리)와 연령대(0_9 등) 추출
    match = re.search(r"_(\d{4})\((\d+_\d*)\)", file_name)
    if match:
        year = match.group(1)        # 연도
        age_range = match.group(2)   # 연령대 (예: 0_9)
    else:
        year = None
        age_range = None

    # 3-2. 전체 엑셀 파일 읽기 (header=None으로 모든 데이터를 그대로 불러옴)
    df_all = pd.read_excel(file_path, header=None)

    # 3-3. 상위 3줄(메타데이터 또는 설명) 분리 → 리스트로 저장
    df_header = df_all.iloc[:3].values.tolist()

    # 3-4. 4번째 줄부터 실제 데이터
    df_data = df_all.iloc[3:].copy()
    df_data.columns = df_data.iloc[0]  # 첫 번째 행을 컬럼명으로 지정
    df_data = df_data[1:].reset_index(drop=True)  # 컬럼명 행 제거하고 인덱스 재설정

    # 3-5. 연도, 연령대 컬럼 추가
    df_data["연도"] = year
    df_data["연령대"] = age_range

    # 3-6. 엑셀로 저장 (기존 파일에 덮어쓰기)
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        # 1) 상위 3줄을 한 줄씩 수동으로 작성
        for row_idx, row in enumerate(df_header):
            pd.DataFrame([row]).to_excel(writer, index=False, header=False, startrow=row_idx)
        
        # 2) 그 아래에 df_data를 추가 (4번째 줄부터)
        df_data.to_excel(writer, index=False, startrow=3)

    print(f"✅ 처리 완료: {file_name}")
import pandas as pd
import glob
import os
import re

# 1. 현재 스크립트 기준으로 data 폴더 경로 설정
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

# 2. 엑셀 파일 목록 가져오기
file_list = glob.glob(os.path.join(base_path, "다빈도질병통계_질별연령별10세구간별_*.xlsx"))

# 3. 각 파일 처리
for file_path in file_list:
    file_name = os.path.basename(file_path)

    # 3-1. 연도와 연령대 추출
    match = re.search(r"_(\d{4})\((\d+_\d*)\)", file_name)
    if match:
        year = match.group(1)
        age_range = match.group(2)
    else:
        year = None
        age_range = None

    # 3-2. 전체 엑셀 파일 읽기
    df_all = pd.read_excel(file_path, header=None)

    # 3-3. 상위 3줄 메타데이터
    df_header = df_all.iloc[:3].values.tolist()

    # 3-4. 데이터 부분 분리 및 정리
    df_data = df_all.iloc[3:].copy()
    df_data.columns = df_data.iloc[0]
    df_data = df_data[1:].reset_index(drop=True)

    # 3-5. 숫자 컬럼 변환
    for col in ["요양급여비용총액", "보험자부담금"]:
        df_data[col] = pd.to_numeric(df_data[col], errors="coerce")

    # 3-6. 환자부담금 계산
    df_data["환자부담금"] = df_data["요양급여비용총액"] - df_data["보험자부담금"]

    # 3-7. 연도, 연령대 추가
    df_data["연도"] = year
    df_data["연령대"] = age_range

    # 3-8. 컬럼 순서 조정: 환자부담금 → 연도 → 연령대 순서 되도록
    cols = list(df_data.columns)
    if "환자부담금" in cols and "연도" in cols and "연령대" in cols:
        # 제거하고 순서대로 다시 넣기
        cols.remove("연도")
        cols.remove("연령대")
        cols.remove("환자부담금")
        cols += ["환자부담금", "연도", "연령대"]
        df_data = df_data[cols]

    # 3-9. 엑셀로 저장
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        for row_idx, row in enumerate(df_header):
            pd.DataFrame([row]).to_excel(writer, index=False, header=False, startrow=row_idx)
        df_data.to_excel(writer, index=False, startrow=3)

    print(f"✅ 처리 완료: {file_name}")

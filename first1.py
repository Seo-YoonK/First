# streamlit_app.py

import streamlit as st
import pandas as pd

st.set_page_config(page_title="2025년 5월 연령별 인구 분석", layout="wide")
st.title("👥 2025년 5월 연령별 인구 현황 분석")

# 1. CSV 파일 불러오기 (EUC-KR 인코딩)
file_path = "202505_202505_연령별인구현황_월간.csv"

try:
    df = pd.read_csv(file_path, encoding='euc-kr')
except Exception as e:
    st.error(f"CSV 파일을 불러오는 중 오류 발생: {e}")
    st.stop()

# 2. 원본 데이터 보여주기
st.subheader("📄 원본 데이터 미리보기")
st.dataframe(df)

# 3. 연령별 열 추출 및 전처리
age_cols = [col for col in df.columns if col.startswith("2025년05월_계_")]
age_renamed = {col: col.replace("2025년05월_계_", "") for col in age_cols}

df_age = df[["행정구역"] + age_cols + ["총인구수"]].copy()
df_age.rename(columns=age_renamed, inplace=True)

# 4. 총인구수 기준 상위 5개 행정구역 추출
top5 = df_age.sort_values(by="총인구수", ascending=False).head(5)

# 5. 시각화를 위한 데이터 변환 (행정구역별 연령 분포)
top5_long = top5.set_index("행정구역").drop(columns="총인구수").T
top5_long.index.name = "연령"
top5_long.reset_index(inplace=True)

# 6. 연령 순서 정렬 (숫자로 변환 가능할 경우)
try:
    top5_long["연령"] = top5_long["연령"].astype(int)
    top5_long.sort_values(by="연령", inplace=True)
except:
    pass

# 7. 선 그래프 시각화
st.subheader("📈 상위 5개 지역의 연령별 인구 분포 (선 그래프)")
st.line_chart(top5_long.set_index("연령"))

# 8. 전처리된 데이터도 보여주기
st.subheader("🧾 상위 5개 행정구역의 연령별 인구 데이터")
st.dataframe(top5)

import streamlit as st
import pandas as pd

st.set_page_config(page_title="2025년 5월 연령별 인구 분석", layout="wide")
st.title("👥 2025년 5월 연령별 인구 현황 분석")

# 1. CSV 파일 경로 및 불러오기
file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding='euc-kr')

# 2. 열 이름 확인 및 추출
region_col = [col for col in df.columns if "행정구역" in col][0]
total_col = [col for col in df.columns if "총인구수" in col][0]
age_cols = [col for col in df.columns if "2025년05월_계_" in col and "총인구수" not in col]

# 3. 연령 열 이름 정제
age_renamed = {col: col.replace("2025년05월_계_", "") for col in age_cols}

# 4. 분석용 데이터프레임 구성
df_age = df[[region_col] + age_cols + [total_col]].copy()
df_age.rename(columns=age_renamed, inplace=True)
df_age.rename(columns={region_col: "행정구역", total_col: "총인구수"}, inplace=True)

# 5. 상위 5개 행정구역 추출
top5 = df_age.sort_values(by="총인구수", ascending=False).head(5)

# 6. 시각화용 데이터 변환
top5_long = top5.set_index("행정구역").drop(columns="총인구수").T
top5_long.index.name = "연령"
top5_long.reset_index(inplace=True)

# 7. 연령 숫자 정렬
try:
    top5_long["연령"] = top5_long["연령"].astype(int)
    top5_long.sort_values("연령", inplace=True)
except:
    pass

# 8. 시각화
st.subheader("📈 상위 5개 지역의 연령별 인구 분포")
st.line_chart(top5_long.set_index("연령"))

# 9. 원본 및 전처리 데이터 표시
st.subheader("📄 원본 데이터")
st.dataframe(df)

st.subheader("🧾 상위 5개 지역 데이터")
st.dataframe(top5)

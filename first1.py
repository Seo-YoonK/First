import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="2025년 5월 연령별 인구 분석", layout="wide")
st.title("👥 2025년 5월 연령별 인구 현황 분석")

file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding='euc-kr')

# '총인구수' 숫자 변환
total_col_name = [col for col in df.columns if "총인구수" in col][0]
df['총인구수'] = df[total_col_name].str.replace(',', '').astype(int)

# 연령 관련 컬럼 추출
age_columns = [col for col in df.columns if "2025년05월_계_" in col and "총인구수" not in col]

# 컬럼명 간단하게 정리 (100세 이상은 그대로 두기)
new_columns = []
for col in age_columns:
    if '100세 이상' in col:
        new_columns.append('100세 이상')
    else:
        new_columns.append(col.replace("2025년05월_계_", ""))

# 행정구역 컬럼명 찾기
region_col = [col for col in df.columns if "행정구역" in col][0]

# 분석용 데이터프레임 생성
df_age = df[[region_col] + age_columns + ['총인구수']].copy()
df_age.columns = ["행정구역"] + new_columns + ['총인구수']

# 상위 5개 행정구역 추출
top5 = df_age.sort_values(by='총인구수', ascending=False).head(5)

# 시각화용 데이터 준비 (행정구역이 컬럼, 연령이 인덱스)
top5_long = top5.set_index("행정구역").drop(columns="총인구수").T
top5_long.index.name = "연령"
top5_long.reset_index(inplace=True)

# 연령 숫자 변환 시도 (성공한 것만)
def try_int(x):
    try:
        return int(x)
    except:
        return np.nan

top5_long['연령_num'] = top5_long['연령'].map(try_int)

# 숫자 변환 실패한(예: '100세 이상') 행은 숫자 최대값 + 1 로 뒤로 보냄
max_age = top5_long['연령_num'].max()
top5_long['연령_num'] = top5_long['연령_num'].fillna(max_age + 1)

# 연령_num 기준으로 정렬
top5_long = top5_long.sort_values('연령_num')

# 숫자 변환 (행정구역 컬럼)
for col in top5_long.columns:
    if col not in ['연령', '연령_num']:
        top5_long[col] = pd.to_numeric(top5_long[col], errors='coerce').fillna(0)

# 인덱스 설정 (x축은 원본 '연령' 문자열 유지)
chart_df = top5_long.set_index('연령')

# 시각화
st.subheader("📈 상위 5개 지역의 연령별 인구 분포")
st.line_chart(chart_df)

# 데이터 확인용 출력
st.subheader("📄 원본 데이터")
st.dataframe(df)

st.subheader("🧾 상위 5개 지역 데이터")
st.dataframe(top5)

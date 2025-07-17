import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="2025년 5월 연령별 인구 분석", layout="wide")
st.title("👥 2025년 5월 연령별 인구 현황 분석")

# 파일 경로 (본인 환경에 맞게 수정)
file_path = "202505_202505_연령별인구현황_월간.csv"

# 1. 데이터 읽기
df = pd.read_csv(file_path, encoding='euc-kr')

# 2. 총인구수 컬럼 찾기 및 숫자형 변환
total_col_name = [col for col in df.columns if "총인구수" in col][0]
df['총인구수'] = df[total_col_name].str.replace(',', '').astype(int)

# 3. 연령별 컬럼 리스트(2025년05월_계_ 접두사 포함) 추출
age_columns = [col for col in df.columns if "2025년05월_계_" in col and "총인구수" not in col]

# 4. 컬럼명 정리 - 접두사 제거, '100세 이상'은 그대로 유지
new_columns = []
for col in age_columns:
    if '100세 이상' in col:
        new_columns.append('100세 이상')
    else:
        new_columns.append(col.replace("2025년05월_계_", ""))

# 5. 행정구역 컬럼명 추출
region_col = [col for col in df.columns if "행정구역" in col][0]

# 6. 분석용 데이터프레임 생성 및 컬럼명 변경
df_age = df[[region_col] + age_columns + ['총인구수']].copy()
df_age.columns = ["행정구역"] + new_columns + ['총인구수']

# 7. 상위 5개 행정구역 선정 (총인구수 기준)
top5 = df_age.sort_values(by='총인구수', ascending=False).head(5)

# 8. 시각화용 데이터 변환: 행정구역은 컬럼, 연령은 행
top5_long = top5.set_index("행정구역").drop(columns="총인구수").T
top5_long.index.name = "연령"
top5_long = top5_long.reset_index()

# 9. 연령 숫자형으로 변환 실패 시 NaN 처리
def convert_age(x):
    try:
        return int(x)
    except:
        return np.nan

top5_long['연령_num'] = top5_long['연령'].map(convert_age)

# 10. 연령_num 결측치는 임시로 150 (충분히 큰 숫자)로 설정 (맨 뒤로)
top5_long['연령_num'] = top5_long['연령_num'].fillna(150)

# 11. 연령_num 기준 정렬
top5_long = top5_long.sort_values('연령_num')

# 12. 숫자 변환 및 결측치 0 채우기
for col in top5_long.columns:
    if col not in ['연령', '연령_num']:
        top5_long[col] = pd.to_numeric(top5_long[col], errors='coerce').fillna(0)

# 13. 연령 순서에 맞게 x축 카테고리 생성 (0~100 + 100세 이상)
age_order = [str(i) for i in range(0, 101)] + ['100세 이상']

# 14. 인덱스를 연령 문자형으로 설정, 연령 컬럼도 카테고리로 변환하여 순서 유지
top5_long['연령'] = pd.Categorical(top5_long['연령'], categories=age_order, ordered=True)
top5_long = top5_long.sort_values('연령')
chart_df = top5_long.set_index('연령')

# 15. 그래프 출력
st.subheader("📈 상위 5개 지역의 연령별 인구 분포")
st.line_chart(chart_df)

# 16. 원본 및 상위 5개 데이터 출력
st.subheader("📄 원본 데이터")
st.dataframe(df)

st.subheader("🧾 상위 5개 지역 데이터")
st.dataframe(top5)

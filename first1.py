import streamlit as st
import pandas as pd

st.set_page_config(page_title="2025년 5월 연령별 인구 분석", layout="wide")
st.title("👥 2025년 5월 연령별 인구 현황 분석")

# 1. 데이터 불러오기
file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding='euc-kr')

# 2. 총인구수 숫자 변환
total_col_name = [col for col in df.columns if "총인구수" in col][0]
df['총인구수'] = df[total_col_name].str.replace(',', '').astype(int)

# 3. 연령 관련 컬럼명 추출
age_columns = [col for col in df.columns if "2025년05월_계_" in col and "총인구수" not in col]

# 4. '100세 이상' 처리 및 접두사 제거
new_columns = []
for col in age_columns:
    if '100세 이상' in col:
        new_columns.append('100세 이상')
    else:
        new_columns.append(col.replace("2025년05월_계_", ""))

# 5. 행정구역 컬럼명 찾기
region_col = [col for col in df.columns if "행정구역" in col][0]

# 6. 분석용 데이터프레임 구성 및 컬럼명 변경
df_age = df[[region_col] + age_columns + ['총인구수']].copy()
df_age.columns = ["행정구역"] + new_columns + ['총인구수']

# 7. 상위 5개 행정구역 추출
top5 = df_age.sort_values(by='총인구수', ascending=False).head(5)

# 8. 시각화용 데이터 변환 (행정구역이 컬럼, 연령이 행)
top5_long = top5.set_index("행정구역").drop(columns="총인구수").T
top5_long.index.name = "연령"
top5_long.reset_index(inplace=True)

# 9. 연령 순서 리스트 만들기 (숫자순 + '100세 이상' 마지막)
age_order = [str(i) for i in range(0, 101)]  # 0~100세 숫자형 문자열
if '100세 이상' in top5_long['연령'].values:
    age_order.append('100세 이상')

# 10. '연령'을 카테고리 타입으로 변환하여 정렬 보장
top5_long['연령'] = pd.Categorical(top5_long['연령'], categories=age_order, ordered=True)
top5_long.sort_values('연령', inplace=True)

# 11. 나머지 컬럼 숫자 변환, 결측치는 0으로
for col in top5_long.columns:
    if col != '연령':
        top5_long[col] = pd.to_numeric(top5_long[col], errors='coerce').fillna(0)

# 12. 인덱스 설정
chart_df = top5_long.set_index('연령')

# 13. 시각화 출력
st.subheader("📈 상위 5개 지역의 연령별 인구 분포")
st.line_chart(chart_df)

# 14. 원본 및 상위 5개 데이터 출력
st.subheader("📄 원본 데이터")
st.dataframe(df)

st.subheader("🧾 상위 5개 지역 데이터")
st.dataframe(top5)

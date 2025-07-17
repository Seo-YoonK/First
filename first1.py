import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.set_page_config(page_title="2025년 5월 연령별 인구 분석", layout="wide")
st.title("👥 2025년 5월 연령별 인구 현황 분석")

file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding='euc-kr')

# 총인구수 숫자 변환
total_col_name = [col for col in df.columns if "총인구수" in col][0]
df['총인구수'] = df[total_col_name].str.replace(',', '').astype(int)

# 연령별 컬럼 추출
age_columns = [col for col in df.columns if "2025년05월_계_" in col and "총인구수" not in col]

# 컬럼명 정리
new_columns = []
for col in age_columns:
    if '100세 이상' in col:
        new_columns.append('100세 이상')
    else:
        new_columns.append(col.replace("2025년05월_계_", ""))

region_col = [col for col in df.columns if "행정구역" in col][0]

df_age = df[[region_col] + age_columns + ['총인구수']].copy()
df_age.columns = ["행정구역"] + new_columns + ['총인구수']

# 상위 5개 행정구역 추출
top5 = df_age.sort_values(by='총인구수', ascending=False).head(5)

# 데이터 변환: 행정구역은 컬럼, 연령은 행
top5_long = top5.set_index("행정구역").drop(columns="총인구수").T.reset_index()
top5_long.rename(columns={'index': '연령'}, inplace=True)

# 연령을 숫자로 변환 가능하면 숫자로 변환, '100세 이상'은 101로 대체
def convert_age(x):
    try:
        return int(x)
    except:
        return 101  # 100세 이상 구간 숫자로 대체

top5_long['연령_num'] = top5_long['연령'].map(convert_age)

# 연령 숫자 기준 오름차순 정렬
top5_long = top5_long.sort_values('연령_num')

# Melt (긴 형태)로 변환 (시각화에 용이)
df_melt = top5_long.melt(id_vars=['연령', '연령_num'], var_name='행정구역', value_name='인구수')

# 인구수 숫자형 변환 및 결측 0 처리
df_melt['인구수'] = pd.to_numeric(df_melt['인구수'], errors='coerce').fillna(0)

# 연령 순서 지정용 카테고리 (0~100 + 100세 이상)
age_order = [str(i) for i in range(0, 101)] + ['100세 이상']
df_melt['연령'] = pd.Categorical(df_melt['연령'], categories=age_order, ordered=True)

# Altair 차트 생성
chart = alt.Chart(df_melt).mark_line(point=True).encode(
    x=alt.X('연령:N', title='연령', sort=age_order),
    y=alt.Y('인구수:Q', title='인구 수'),
    color='행정구역:N',
    tooltip=['행정구역', '연령', '인구수']
).properties(
    width=900,
    height=500
).interactive()

st.subheader("📈 상위 5개 지역의 연령별 인구 분포 (Altair 차트)")
st.altair_chart(chart, use_container_width=True)

# 원본 및 상위 5개 데이터 출력
st.subheader("📄 원본 데이터")
st.dataframe(df)

st.subheader("🧾 상위 5개 지역 데이터")
st.dataframe(top5)

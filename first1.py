import streamlit as st
import pandas as pd

st.set_page_config(page_title="2025년 5월 연령별 인구 분석", layout="wide")
st.title("👥 2025년 5월 연령별 인구 현황 분석")

if True:
    # 1. CSV 파일 불러오기
    file_path = "202505_202505_연령별인구현황_월간.csv"
    df = pd.read_csv(file_path, encoding='euc-kr')

    # 2. '총인구수' 컬럼 문자열 쉼표 제거 후 숫자 변환
    total_col_name = [col for col in df.columns if "총인구수" in col][0]
    df['총인구수'] = df[total_col_name].str.replace(',', '').astype(int)

    # 3. 연령 관련 컬럼명 추출 ('2025년05월_계_' 포함하고 '총인구수' 제외)
    age_columns = [col for col in df.columns if "2025년05월_계_" in col and "총인구수" not in col]

    # 4. '100세 이상' 컬럼명 단순화 및 나머지 접두사 제거
    new_columns = []
    for col in age_columns:
        if '100세 이상' in col:
            new_columns.append('100세 이상')
        else:
            new_columns.append(col.replace("2025년05월_계_", ""))

    # 5. '행정구역' 컬럼명 찾기
    region_col = [col for col in df.columns if "행정구역" in col][0]

    # 6. 분석용 데이터프레임 생성 및 컬럼명 교체
    df_age = df[[region_col] + age_columns + ['총인구수']].copy()
    df_age.columns = ["행정구역"] + new_columns + ['총인구수']

    # 7. 총인구수 기준 상위 5개 행정구역 추출
    top5 = df_age.sort_values(by='총인구수', ascending=False).head(5)

    # 8. 시각화용 데이터 변환 (행정구역은 컬럼, 연령은 인덱스)
    top5_long = top5.set_index("행정구역").drop(columns="총인구수").T
    top5_long.index.name = "연령"
    top5_long.reset_index(inplace=True)

    # 9. 연령 숫자형 변환 및 정렬 (100세 이상 → 100)
    top5_long['연령'] = top5_long['연령'].replace({'100세 이상': '100'})
    top5_long['연령'] = pd.to_numeric(top5_long['연령'], errors='coerce')

    # 10. 변환 실패한 행(연령이 NaN) 제거
    top5_long = top5_long.dropna(subset=['연령'])

    # 11. 연령 기준 정렬
    top5_long = top5_long.sort_values('연령')

    # 12. 인덱스를 연령으로 설정
    chart_df = top5_long.set_index('연령')

    # 13. 시각화
    st.subheader("📈 상위 5개 지역의 연령별 인구 분포")
    st.line_chart(chart_df)

    # 14. 원본 데이터 및 상위 5개 데이터 보여주기
    st.subheader("📄 원본 데이터")
    st.dataframe(df)

    st.subheader("🧾 상위 5개 지역 데이터")
    st.dataframe(top5)

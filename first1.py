import streamlit as st
import pandas as pd

st.set_page_config(page_title="2025년 5월 연령별 인구 분석", layout="wide")
st.title("👥 2025년 5월 연령별 인구 현황 분석")

if True:
    # 1. CSV 파일 불러오기
    file_path = "202505_202505_연령별인구현황_월간.csv"
    df = pd.read_csv(file_path, encoding='euc-kr')

    # 2. '총인구수' 컬럼 문자열 치환 후 숫자 변환
    # 예: "2025년05월_계_총인구수" 컬럼의 쉼표 제거 후 int 변환
    df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)

    # 3. 연령 관련 컬럼만 추출 (예: "2025년05월_계_" 포함, 총인구수 제외)
    age_columns = [col for col in df.columns if "2025년05월_계_" in col and "총인구수" not in col]

    # 4. 100세 이상 컬럼 처리 예시
    new_columns = []
    for col in age_columns:
        if '100세 이상' in col:
            # '100세 이상' 컬럼명을 '100'으로 단순화
            new_columns.append('100세 이상')
        else:
            # '2025년05월_계_' 접두사 제거
            new_columns.append(col.replace("2025년05월_계_", ""))

    # 5. 분석용 데이터프레임 만들기
    # '행정구역' 컬럼 찾기
    region_col = [col for col in df.columns if "행정구역" in col][0]

    df_age = df[[region_col] + age_columns + ['총인구수']].copy()
    df_age.columns = ["행정구역"] + new_columns + ['총인구수']

    # 6. 상위 5개 행정구역 추출
    top5 = df_age.sort_values(by='총인구수', ascending=False).head(5)

    # 7. 시각화용 데이터 변환
    top5_long = top5.set_index("행정구역").drop(columns="총인구수").T
    top5_long.index.name = "연령"
    top5_long.reset_index(inplace=True)

    # 8. 연령을 숫자형으로 변환 및 정렬 시도
    try:
        # '100세 이상'을 100으로 변환해서 정렬 편하게
        top5_long['연령'] = top5_long['연령'].replace({'100세 이상': '100'}).astype(int)
        top5_long.sort_values("연령", inplace=True)
    except (ValueError, TypeError):
        pass

    # 9. 시각화
    st.subheader("📈 상위 5개 지역의 연령별 인구 분포")
    st.line_chart(top5_long.set_index("연령"))

    # 10. 원본 및 전처리 데이터 출력
    st.subheader("📄 원본 데이터")
    st.dataframe(df)

    st.subheader("🧾 상위 5개 지역 데이터")
    st.dataframe(top5)

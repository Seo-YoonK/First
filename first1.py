import streamlit as st
import pandas as pd

st.set_page_config(page_title="2025년 5월 연령별 인구 분석", layout="wide")
st.title("👥 2025년 5월 연령별 인구 현황 분석")

if True:
    # 1. 데이터 읽기
    file_path = "202505_202505_연령별인구현황_월간.csv"
    df = pd.read_csv(file_path, encoding='euc-kr')

    # 2. 총인구수 문자열 숫자로 변환
    total_col_name = [col for col in df.columns if "총인구수" in col][0]
    df['총인구수'] = df[total_col_name].str.replace(',', '').astype(int)

    # 3. 연령 관련 컬럼명 추출 (총인구수 제외)
    age_columns = [col for col in df.columns if "2025년05월_계_" in col and "총인구수" not in col]

    # 4. 100세 이상 컬럼명 정리 및 나머지 접두사 제거
    new_columns = []
    for col in age_columns:
        if '100세 이상' in col:
            new_columns.append('100세 이상')
        else:
            new_columns.append(col.replace("2025년05월_계_", ""))

    # 5. 행정구역 컬럼명 찾기
    region_col = [col for col in df.columns if "행정구역" in col][0]

    # 6. 분석용 데이터프레임 생성 및 컬럼명 교체
    df_age = df[[region_col] + age_columns + ['총인구수']].copy()
    df_age.columns = ["행정구역"] + new_columns + ['총인구수']

    # 7. 총인구수 상위 5개 행정구역 추출
    top5 = df_age.sort_values(by='총인구수', ascending=False).head(5)

    # 8. 시각화용 데이터 준비
    top5_long = top5.set_index("행정구역").drop(columns="총인구수").T
    top5_long.index.name = "연령"
    top5_long.reset_index(inplace=True)

    # 9. 연령 '100세 이상' → '100' 변환 및 숫자형 변환
    top5_long['연령'] = top5_long['연령'].replace({'100세 이상': '100'})
    top5_long['연령'] = pd.to_numeric(top5_long['연령'], errors='coerce')

    # 10. 변환 실패(NA) 행 제거
    top5_long.dropna(subset=['연령'], inplace=True)

    # 11. 나머지 컬럼들도 숫자형인지 확인, 숫자가 아니면 변환 시도
    for col in top5_long.columns:
        if col != '연령':
            top5_long[col] = pd.to_numeric(top5_long[col], errors='coerce')

    # 12. 결측치가 생겼으면 0으로 채우기
    top5_long.fillna(0, inplace=True)

    # 13. 연령 오름차순 정렬 및 인덱스 설정
    top5_long.sort_values('연령', inplace=True)
    chart_df = top5_long.set_index('연령')

    # 14. 디버깅용 출력 (원한다면 주석 처리 가능)
    st.write("### 시각화용 데이터 샘플")
    st.write(chart_df.head())

    # 15. 라인 차트 그리기
    st.subheader("📈 상위 5개 지역의 연령별 인구 분포")
    st.line_chart(chart_df)

    # 16. 원본 데이터 및 상위 5개 데이터 출력
    st.subheader("📄 원본 데이터")
    st.dataframe(df)

    st.subheader("🧾 상위 5개 지역 데이터")
    st.dataframe(top5)

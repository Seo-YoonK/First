import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 제목
st.title("2025년 5월 기준 연령별 인구 현황 및 지도")

# CSV 불러오기
if True:
    df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')

    # 총인구수 숫자 변환
    df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)

    # 연령별 컬럼 추출 및 이름 정리
    age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and ('세' in col or '100세 이상' in col)]
    new_columns = ['100세 이상' if '100세 이상' in col else col.replace('2025년05월_계_', '').replace('세', '') + '세' for col in age_columns]

    # 정리된 데이터프레임 구성
    df_age = df[['행정구역', '총인구수'] + age_columns].copy()
    df_age.columns = ['행정구역', '총인구수'] + new_columns

    # 시도 추출 함수
    def extract_province(name):
        if name.startswith("서울"):
            return "서울특별시"
        elif name.startswith("부산"):
            return "부산광역시"
        elif name.startswith("인천"):
            return "인천광역시"
        elif name.startswith("대구"):
            return "대구광역시"
        elif name.startswith("광주"):
            return "광주광역시"
        elif name.startswith("대전"):
            return "대전광역시"
        elif name.startswith("울산"):
            return "울산광역시"
        elif name.startswith("세종"):
            return "세종특별자치시"
        elif name.startswith("경기"):
            return "경기도"
        elif name.startswith("강원"):
            return "강원도"
        elif name.startswith("충북"):
            return "충청북도"
        elif name.startswith("충남"):
            return "충청남도"
        elif name.startswith("전북"):
            return "전라북도"
        elif name.startswith("전남"):
            return "전라남도"
        elif name.startswith("경북"):
            return "경상북도"
        elif name.startswith("경남"):
            return "경상남도"
        elif name.startswith("제주"):
            return "제주특별자치도"
        else:
            return name.split()[0]

    # 시도 컬럼 추가
    df_age['시도'] = df_age['행정구역'].apply(extract_province)

    # 시도별 총인구수 집계 → 상위 5개
    top5 = df_age.groupby('시도', as_index=False).agg({'총인구수': 'sum'}).sort_values(by='총인구수', ascending=False).head(5)

    # 시도별 위도, 경도 매핑
    coords = {
        "서울특별시": [37.5665, 126.9780],
        "부산광역시": [35.1796, 129.0756],
        "인천광역시": [37.4563, 126.7052],
        "대구광역시": [35.8714, 128.6014],
        "경기도": [37.4138, 127.5183],
        "광주광역시": [35.1595, 126.8526],
        "대전광역시": [36.3504, 127.3845],
        "울산광역시": [35.5384, 129.3114],
        "세종특별자치시": [36.4801, 127.2890],
        "강원도": [37.8228, 128.1555],
        "충청북도": [36.6357, 127.4917],
        "충청남도": [36.5184, 126.8000],
        "전라북도": [35.7167, 127.1442],
        "전라남도": [34.8161, 126.4630],
        "경상북도": [36.4919, 128.8889],
        "경상남도": [35.4606, 128.2132],
        "제주특별자치도": [33.4996, 126.5312],
    }

    # 좌표 매핑
    top5['lat'] = top5['시도'].map(lambda x: coords.get(x, [None, None])[0])
    top5['lon'] = top5['시도'].map(lambda x: coords.get(x, [None, None])[1])

    # 지도 출력
    if top5.empty:
        st.error("지도에 표시할 수 있는 도시가 없습니다. 행정구역 이름과 좌표 매핑을 확인하세요.")
        st.stop()

    m = folium.Map(location=[top5.iloc[0]['lat'], top5.iloc[0]['lon']], zoom_start=7)

    for _, row in top5.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=10,
            popup=f"{row['시도']}: {row['총인구수']:,}명",
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.5
        ).add_to(m)

    st.subheader("🗺️ 상위 5개 시도 인구 지도")
    st_folium(m, width=700, height=500)

    st.subheader("상위 5개 시도")
    st.write(top5[['시도', '총인구수']])

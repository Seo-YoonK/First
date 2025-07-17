import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 제목
st.title("2025년 5월 기준 연령별 인구 현황 및 지도")

# CSV 불러오기 (True로 고정)
if True:
    df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')

    # 인구수 정리
    df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)

    # 연령별 인구 컬럼만 선택
    age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and ('세' in col or '100세 이상' in col)]

    # 컬럼명 정리: '2025년05월_계_3세' → '3세'
    new_columns = []
    for col in age_columns:
        if '100세 이상' in col:
            new_columns.append('100세 이상')
        else:
            new_columns.append(col.replace('2025년05월_계_', '').replace('세', '') + '세')

    # 연령별 인구 데이터프레임 구성
    df_age = df[['행정구역', '총인구수'] + age_columns].copy()
    df_age.columns = ['행정구역', '총인구수'] + new_columns

    # 인구수 기준 상위 5개 도시
    top5 = df_age.sort_values(by='총인구수', ascending=False).head(5).copy()

    # 위도/경도 정보 수동 추가
    coords = {
        "서울특별시": [37.5665, 126.9780],
        "부산광역시": [35.1796, 129.0756],
        "인천광역시": [37.4563, 126.7052],
        "대구광역시": [35.8714, 128.6014],
        "경기도 수원시": [37.2636, 127.0286],
        # 필요시 추가
    }

    # 좌표 매핑
    top5['lat'] = top5['행정구역'].map(lambda x: coords.get(x, [None, None])[0])
    top5['lon'] = top5['행정구역'].map(lambda x: coords.get(x, [None, None])[1])

    # 좌표 없는 행 제거
    top5 = top5.dropna(subset=['lat', 'lon'])

    # ▷ 지도 표시
    if top5.empty:
        st.error("지도에 표시할 수 있는 도시가 없습니다. 행정구역 이름과 좌표 매핑을 확인하세요.")
        st.stop()

    # 지도 초기화
    m = folium.Map(location=[top5.iloc[0]['lat'], top5.iloc[0]['lon']], zoom_start=7)

    # 마커 추가
    for _, row in top5.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=10,
            popup=row['행정구역'],
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.5
        ).add_to(m)

    # 지도 보여주기
    st.subheader("🗺️ 상위 5개 도시 지도")
    st_folium(m, width=700, height=500)

st.subheader("상위 5개 행정구역 이름 확인용 (좌표 매핑용)")
st.write(top5['행정구역'].tolist())


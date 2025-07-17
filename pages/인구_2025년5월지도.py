import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.title("상위 5개 행정구역 인구수 기반 반투명 원형 마커 지도")

# 1. 데이터 불러오기 및 전처리
df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)

region_col = [col for col in df.columns if "행정구역" in col][0]

# 2. 상위 5개 행정구역 추출
top5 = df[[region_col, '총인구수']].sort_values(by='총인구수', ascending=False).head(5)

# 3. 행정구역별 위도/경도 좌표 직접 입력 (필요시 수정)
coords = {
    "서울특별시": (37.5665, 126.9780),
    "부산광역시": (35.1796, 129.0756),
    "인천광역시": (37.4563, 126.7052),
    "대구광역시": (35.8714, 128.6014),
    "대전광역시": (36.3504, 127.3845),
}

top5['lat'] = top5[region_col].map(lambda x: coords.get(x, (None, None))[0])
top5['lon'] = top5[region_col].map(lambda x: coords.get(x, (None, None))[1])

top5 = top5.dropna(subset=['lat', 'lon'])

# 4. folium 지도 생성 (중심점: 첫 도시)
m = folium.Map(location=[top5.iloc[0]['lat'], top5.iloc[0]['lon']], zoom_start=7)

# 5. 반투명 원형 마커 추가
for _, row in top5.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=15,  # 원 크기
        popup=f"{row[region_col]}: {row['총인구수']:,}명",
        color='blue',       # 테두리 색
        fill=True,
        fill_color='blue',  # 채우기 색
        fill_opacity=0.4,   # 투명도 (0 완전 투명 ~ 1 완전 불투명)
        tooltip=row[region_col]
    ).add_to(m)

# 6. Streamlit에 지도 표시
st_folium(m, width=700, height=500)

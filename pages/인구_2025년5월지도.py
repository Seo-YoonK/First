# top5 데이터 예시 (행정구역 이름은 df_age 기준으로 정확히 일치해야 함)
coords = {
    "서울특별시": [37.5665, 126.9780],
    "부산광역시": [35.1796, 129.0756],
    "대구광역시": [35.8714, 128.6014],
    "인천광역시": [37.4563, 126.7052],
    "광주광역시": [35.1595, 126.8526],
    # 필요한 도시 추가 가능
}

# 위경도 컬럼 추가
top5['lat'] = top5['행정구역'].map(lambda x: coords.get(x, [None, None])[0])
top5['lon'] = top5['행정구역'].map(lambda x: coords.get(x, [None, None])[1])

# 위경도 누락 제거
top5 = top5.dropna(subset=['lat', 'lon'])

# 비어 있는지 다시 확인
if top5.empty:
    st.error("위경도 정보가 매칭되지 않아 top5가 비어 있습니다.")
    st.stop()

# 지도 표시
import folium
from streamlit_folium import st_folium

m = folium.Map(location=[top5.iloc[0]['lat'], top5.iloc[0]['lon']], zoom_start=7)

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

st.subheader("🗺️ 상위 5개 도시 지도")
st_folium(m, width=700, height=500)

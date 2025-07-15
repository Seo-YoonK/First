# streamlit_app.py

import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from io import StringIO
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

st.set_page_config(page_title="데이터 분석 웹앱", layout="wide")
st.title("📊 웹앱 기반 데이터 분석 도구")

# 1. 파일 업로드
st.sidebar.header("📁 데이터 업로드")
file = st.sidebar.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if file is not None:
    # 파일 인코딩 처리
    try:
        df = pd.read_csv(file)
    except UnicodeDecodeError:
        file.seek(0)
        df = pd.read_csv(file, encoding='cp949')

    st.subheader("🔍 데이터 미리보기")
    st.dataframe(df)

    # 2. 데이터 필터링
    st.sidebar.header("🔎 데이터 필터링")
    filter_columns = st.sidebar.multiselect("필터할 열 선택 (범주형)", df.select_dtypes(include='object').columns)
    filtered_df = df.copy()
    for col in filter_columns:
        values = st.sidebar.multiselect(f"{col}에서 선택:", df[col].unique())
        if values:
            filtered_df = filtered_df[filtered_df[col].isin(values)]

    st.subheader("🗃️ 필터링된 데이터")
    st.dataframe(filtered_df)

    # 3. 지도 시각화
    if {'lat', 'lon'}.issubset(filtered_df.columns):
        st.subheader("🗺️ 지도 시각화")
        st.pydeck_chart(pdk.Deck(
            initial_view_state=pdk.ViewState(
                latitude=filtered_df['lat'].mean(),
                longitude=filtered_df['lon'].mean(),
                zoom=10,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=filtered_df,
                    get_position='[lon, lat]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=200,
                ),
            ],
        ))

    # 4. 그래프 그리기
    st.subheader("📈 그래프 그리기")
    numeric_cols = filtered_df.select_dtypes(include='number').columns
    graph_type = st.selectbox("그래프 종류", ["히스토그램", "산점도", "선그래프", "상관관계 히트맵"])

    if graph_type == "히스토그램":
        col = st.selectbox("히스토그램 열 선택", numeric_cols)
        fig, ax = plt.subplots()
        ax.hist(filtered_df[col], bins=20, color='skyblue')
        st.pyplot(fig)

    elif graph_type == "산점도":
        x = st.selectbox("X축", numeric_cols)
        y = st.selectbox("Y축", numeric_cols)
        fig = px.scatter(filtered_df, x=x, y=y, title="산점도")
        st.plotly_chart(fig)

    elif graph_type == "선그래프":
        x = st.selectbox("X축 (선)", numeric_cols)
        y = st.selectbox("Y축 (선)", numeric_cols)
        fig = px.line(filtered_df, x=x, y=y, title="선그래프")
        st.plotly_chart(fig)

    elif graph_type == "상관관계 히트맵":
        corr = filtered_df[numeric_cols].corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    # 5. 간단한 머신러닝
    st.subheader("🧠 간단한 머신러닝 분석")
    ml_mode = st.radio("모델 선택", ["회귀 분석", "KMeans 클러스터링"])

    if ml_mode == "회귀 분석":
        target = st.selectbox("예측 대상 (Y) 열", numeric_cols)
        features = st.multiselect("입력 변수 (X) 열", [col for col in numeric_cols if col != target])
        if features:
            X = filtered_df[features]
            y = filtered_df[target]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = LinearRegression()
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            st.write("MSE:", mean_squared_error(y_test, predictions))
            st.line_chart(pd.DataFrame({"실제값": y_test.values, "예측값": predictions}))

    elif ml_mode == "KMeans 클러스터링":
        k_features = st.multiselect("클러스터링할 열 선택", numeric_cols)
        if k_features:
            k = st.slider("클러스터 수 (K)", 2, 10, 3)
            kmeans = KMeans(n_clusters=k, n_init='auto')
            kmeans.fit(filtered_df[k_features])
            filtered_df['클러스터'] = kmeans.labels_
            st.write(filtered_df[['클러스터'] + list(k_features)])
            fig = px.scatter(filtered_df, x=k_features[0], y=k_features[1], color='클러스터', title="클러스터링 시각화")
            st.plotly_chart(fig)

    # 6. 결과 다운로드
    st.subheader("📥 결과 다운로드")
    csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📤 CSV 다운로드", data=csv, file_name="분석결과.csv", mime="text/csv")

else:
    st.info("왼쪽 사이드바에서 CSV 파일을 업로드해 주세요.")

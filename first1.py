import streamlit as st
st.title('나의 첫 웹 서비스 만들기!!')
name = st.text_input('이름을 입력해주세요 : ')
menu = st.selectbox('좋아하는 음식을 선택해주세요:', ['김치찌개','된장찌개','국밥','제육볶음','돈까스'])
if st.button('인사말 생성') : 
  st.write(name+'님! 당신이 좋아하는 음식은 '+menu+'이군요?! 저도 좋아요!!')

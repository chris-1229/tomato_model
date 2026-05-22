import streamlit as st
import pandas as pd
import numpy as np

# [참고] rf_model은 기존에 학습된 모델 객체 레이아웃이 사전에 로드되어 있어야 합니다.
# 예: import joblib; rf_model = joblib.load('model.pkl')

# 1. 웹 페이지 제목 설정
st.title("🌱 스마트팜 착과율 예측 시스템")
st.markdown("내부 온도, 내부 습도, 지온을 입력하여 예상 착과율을 확인하세요.")
st.write("---")

# 2. 사이드바 또는 메인 화면에 사용자 입력 받기
st.sidebar.header("📊 환경 데이터 입력")

# 수치 입력 방식 (슬라이더 또는 숫자 입력창 중 선택 가능)
temp = st.sidebar.slider("내부온도 (°C)", min_value=0.0, max_value=50.0, value=25.0, step=0.1)
humidity = st.sidebar.slider("내부습도 (%)", min_value=0.0, max_value=100.0, value=60.0, step=0.1)
soil_temp = st.sidebar.slider("지온 (°C)", min_value=0.0, max_value=50.0, value=20.0, step=0.1)

# 3. 데이터프레임 변환
input_data = pd.DataFrame([[temp, humidity, soil_temp]], columns=['내부온도', '내부습도', '지온'])

# 입력된 데이터 화면에 보여주기
st.subheader("📥 입력된 데이터 요약")
st.dataframe(input_data)

st.write("---")

# 4. 예측 및 결과 출력
st.subheader("🔮 착과율 예측 결과")

# 버튼을 누르면 예측 시작
if st.button("착과율 예측하기"):
    try:
        # 모델 예측
        predicted = rf_model.predict(input_data)
        
        # 결과를 보기 좋게 메트릭(Metric) 형태로 출력
        st.success("예측이 완료되었습니다!")
        st.metric(label="🎯 예측 착과율", value=f"{predicted[0]:.1f}%")
        
    except NameError:
        st.error("🚨 `rf_model`이 정의되지 않았습니다. 모델을 먼저 로드해주세요.")
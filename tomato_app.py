import streamlit as st
import pandas as pd
import numpy as np
import joblib  # pkl 파일을 불러오기 위한 라이브러리

# 1. 페이지 설정 및 모델 불러오기
st.set_page_config(page_title="스마트팜 착과율 예측", layout="centered")

@st.cache_resource  # 앱이 실행될 때 모델을 한 번만 로드하도록 캐싱합니다.
def load_model():
    # tomato_model.pkl 파일이 파이썬 스크립트와 같은 폴더에 있어야 합니다.
    return joblib.load("tomato_model.pkl")

try:
    rf_model = load_model()
    model_loaded = True
except Exception as e:
    st.error("🚨 `tomato_model.pkl` 파일을 찾을 수 없거나 로드하는 데 실패했습니다.")
    st.info("💡 모델 파일이 현재 스크립트와 같은 디렉토리에 있는지, 파일 이름이 정확한지 확인해주세요.")
    model_loaded = False

# 2. 웹 페이지 제목 설정
st.title("🌱 토마토 스마트팜 착과율 예측 시스템")
st.markdown("내부 온도, 내부 습도, 지온을 입력하여 예상 착과율을 확인하세요.")
st.write("---")

# 3. 사이드바에 사용자 입력 받기
st.sidebar.header("📊 환경 데이터 입력")

temp = st.sidebar.slider("내부온도 (°C)", min_value=0.0, max_value=50.0, value=25.0, step=0.1)
humidity = st.sidebar.slider("내부습도 (%)", min_value=0.0, max_value=100.0, value=60.0, step=0.1)
soil_temp = st.sidebar.slider("지온 (°C)", min_value=0.0, max_value=50.0, value=20.0, step=0.1)

# 4. 데이터프레임 변환
input_data = pd.DataFrame([[temp, humidity, soil_temp]], columns=['내부온도', '내부습도', '지온'])

# 입력된 데이터 화면에 보여주기
st.subheader("📥 입력된 데이터 요약")
st.dataframe(input_data)

st.write("---")

# 5. 예측 및 결과 출력
st.subheader("🔮 착과율 예측 결과")

# 버튼을 누르면 예측 시작
if st.button("착과율 예측하기"):
    if model_loaded:
        # 모델 예측
        predicted = rf_model.predict(input_data)
        
        # 결과를 메트릭(Metric) 형태로 출력
        st.success("예측이 완료되었습니다!")
        st.metric(label="🎯 예측 착과율", value=f"{predicted[0]:.1f}%")
    else:
        st.error("모델이 정상적으로 로드되지 않아 예측을 수행할 수 없습니다.")
import streamlit as st
import requests

st.title("디버깅 모드")

SERVICE_KEY = "c75b76458d74a659cad8ab94a533518104d201a1669219e32a7b3f9c46a46b84"
url = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev"
params = {"serviceKey": SERVICE_KEY, "LAWD_CD": "41140", "DEAL_YMD": "202605"}

try:
    response = requests.get(url, params=params, timeout=10)
    st.write("서버 응답:", response.status_code)
    st.text(response.text[:500]) # 서버가 보내는 내용을 500자만 보여줘
except Exception as e:
    st.write("에러 내용:", e)

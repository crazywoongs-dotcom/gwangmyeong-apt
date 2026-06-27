import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET

# 1. 여기에 인증키를 넣으세요!
SERVICE_KEY = "c75b76458d74a659cad8ab94a533518104d201a1669219e32a7b3f9c46a46b84"

st.set_page_config(page_title="광명 실거래가 대시보드", layout="wide")
st.title("🏙️ 광명/철산 실거래가 조회 (국토부 API)")

# 2. 데이터 가져오기 함수 (광명시 법정동코드: 41140)
@st.cache_data(ttl=3600)
def get_real_estate_data(key, region_code="41140", deal_ym="202605"):
    url = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev"
    params = {
        "serviceKey": key,
        "LAWD_CD": region_code,
        "DEAL_YMD": deal_ym
    }
    response = requests.get(url, params=params)
    root = ET.fromstring(response.content)
    
    items = []
    for item in root.findall(".//item"):
        items.append({
            "아파트": item.find("아파트").text,
            "전용면적": float(item.find("전용면적").text),
            "거래금액": int(item.find("거래금액").text.replace(",", "")),
            "층": item.find("층").text,
            "년": item.find("년").text,
            "월": item.find("월").text,
            "일": item.find("일").text
        })
    return pd.DataFrame(items)

# 3. 데이터 로드 및 화면 출력
try:
    df = get_real_estate_data(SERVICE_KEY)
    st.dataframe(df, use_container_width=True)
    st.success("데이터를 성공적으로 불러왔습니다!")
except Exception as e:
    st.error(f"데이터를 불러오지 못했습니다. 인증키를 확인해주세요. 에러내용: {e}")

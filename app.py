import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET

st.title("광명 실거래가 대시보드")

# 인증키를 따옴표 안에 넣으세요
SERVICE_KEY = "c75b76458d74a659cad8ab94a533518104d201a1669219e32a7b3f9c46a46b84"

url = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev"
params = {
    "serviceKey": SERVICE_KEY,
    "LAWD_CD": "41140",
    "DEAL_YMD": "202605"
}

try:
    response = requests.get(url, params=params)
    root = ET.fromstring(response.content)
    items = []
    for item in root.findall(".//item"):
        items.append({
            "아파트": item.find("아파트").text,
            "거래금액": item.find("거래금액").text.strip()
        })
    df = pd.DataFrame(items)
    st.table(df)
except Exception as e:
    st.write("데이터를 가져오는 중입니다. 잠시만 기다려 주세요.")

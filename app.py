import datetime
import numpy as np
import pandas as pd
import streamlit as st

# 1. 웹사이트 기본 설정
st.set_page_config(page_title="광명 신축 동향", layout="wide")
st.title("🏙️ 광명사거리~철산역 신축 아파트 동향")
st.caption("2024년 1월부터 현재까지의 평형별/거래유형별 시세 추이")

# 2. 화면에 보여줄 아파트 단지 목록
apartments = [
    "전체 단지 보기",
    "철산자이더헤리티지",
    "트리우스광명",
    "광명자이더샵포레나",
    "광명센트럴아이파크",
    "호반써밋그랜드에비뉴",
]

# 3. 데이터 준비 (2024년 1월 ~ 현재 가상 데이터)
@st.cache_data
def load_data():
    dates = pd.date_range(start="2024-01-01", end="2026-06-01", freq="MS")
    data_list = []
    np.random.seed(42)

    for d in dates:
        date_str = d.strftime("%Y-%m")
        for apt in apartments[1:]:
            for size in [59, 84]:
                # 매매
                base_p = 75000 if size == 59 else 105000
                p = base_p + int(np.random.randint(-3000, 4000))
                data_list.append([date_str, apt, size, "매매", p, 0])
                # 전세
                base_j = 45000 if size == 59 else 60000
                j = base_j + int(np.random.randint(-2000, 2000))
                data_list.append([date_str, apt, size, "전세", j, 0])
                # 월세
                r_rent = 120 if size == 59 else 160
                r_rent += int(np.random.randint(-10, 15))
                data_list.append([date_str, apt, size, "월세", 5000, r_rent])

    return pd.DataFrame(
        data_list, columns=["년월", "단지명", "평형", "거래유형", "보증금_매매가", "월세"]
    )

df = load_data()

# 4. 상단 필터
col1, col2, col3, col4 = st.columns(4)
with col1: selected_apt = st.selectbox("아파트 단지", apartments)
with col2: selected_size = st.radio("평형 선택", [59, 84], horizontal=True)
with col3: selected_type = st.radio("거래 유형", ["매매", "전세", "월세"], horizontal=True)
with col4: timeframe = st.selectbox("조회 기간", ["전체 기간", "최근 1년", "최근 6개월"])

# 5. 필터링
filtered_df = df[(df["평형"] == selected_size) & (df["거래유형"] == selected_type)].copy()
if selected_apt != "전체 단지 보기":
    filtered_df = filtered_df[filtered_df["단지명"] == selected_apt]

all_months = sorted(filtered_df["년월"].unique())
if timeframe == "최근 1년":
    filtered_df = filtered_df[filtered_df["년월"].isin(all_months[-12:])]
elif timeframe == "최근 6개월":
    filtered_df = filtered_df[filtered_df["년월"].isin(all_months[-6:])]

# 6. 차트
st.subheader("📈 시세 흐름 차트")
if selected_type == "월세":
    st.info("💡 월세 차트는 '보증금 5,000만 원' 고정 기준의 월세 금액(만원) 추이입니다.")
    chart_data = filtered_df.groupby(["년월", "단지명"])["월세"].mean().unstack()
else:
    chart_data = filtered_df.groupby(["년월", "단지명"])["보증금_매매가"].mean().unstack()
st.line_chart(chart_data)

# 7. 상세 데이터
st.subheader("📋 개별 거래 상세 내역")
display_df = filtered_df.sort_values(by="년월", ascending=False).reset_index(drop=True)
if selected_type == "월세":
    display_df["거래금액"] = display_df["보증금_매매가"].astype(str) + "/" + display_df["월세"].astype(str)
else:
    display_df["거래금액"] = display_df["보증금_매매가"].apply(lambda x: f"{x//10000}억 {x%10000}만" if x >= 10000 else f"{x}만")

st.dataframe(display_df[["년월", "단지명", "평형", "거래유형", "거래금액"]], use_container_width=True)

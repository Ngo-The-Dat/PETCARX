# Tra cứu lịch khám của thú cưng
import streamlit as st
import pandas as pd

from services.medical_record_service import (
    get_visit_history,
    get_visit_detail
)

st.title("Tra cứu lịch sử khám thú cưng")

matc = st.number_input(
    "Nhập mã thú cưng (MATC)",
    min_value=1,
    step=1
)

if "selected_makb" not in st.session_state:
    st.session_state.selected_makb = None

if st.button("Tra cứu lịch sử khám"):
    df_history = get_visit_history(matc)

    if df_history.empty:
        st.warning("Không tìm thấy lịch sử khám cho thú cưng này.")
    else:
        st.subheader("📅 Các lần khám trước đó")
        st.dataframe(df_history, use_container_width=True)

        makb_list = df_history["MAKB"].tolist()

        st.selectbox(
            "Chọn lần khám để xem chi tiết",
            makb_list,
            key="selected_makb"
        )

if st.session_state.selected_makb is not None:
    st.divider()
    st.subheader("🩺 Chi tiết bệnh án")

    df_detail = get_visit_detail(
        matc,
        st.session_state.selected_makb
    )

    if df_detail.empty:
        st.info("Không có chi tiết cho lần khám này.")
    else:
        st.markdown("### 📌 Thông tin lần khám")
        info_cols = ["MAKB", "MABACSI", "NGAYHENTAIKHAM"]
        st.dataframe(
            df_detail[info_cols].drop_duplicates(),
            use_container_width=True
        )

        st.markdown("### 🤒 Triệu chứng")
        st.dataframe(
            df_detail[["TRIEUCHUNG"]].dropna().drop_duplicates(),
            use_container_width=True
        )

        st.markdown("### 🧠 Chuẩn đoán")
        st.dataframe(
            df_detail[["CHUANDOAN"]].dropna().drop_duplicates(),
            use_container_width=True
        )

        st.markdown("### 💊 Toa thuốc")
        st.dataframe(
            df_detail[["MASP", "SOLUONG"]].dropna().drop_duplicates(),
            use_container_width=True
        )

if st.button("Quay lại"):
    st.switch_page("pages/doctor.py")
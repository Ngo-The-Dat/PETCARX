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

if st.button("Quay lại"):
    st.switch_page("pages/customer.py")

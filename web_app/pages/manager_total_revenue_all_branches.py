import streamlit as st
from services.report_service import get_total_revenue_all_branches

st.title("Thống kê doanh thu toàn bộ chi nhánh")

if st.button("Xem báo cáo"):
    df = get_total_revenue_all_branches()
    if df.empty:
        st.warning("Không có dữ liệu.")
    else:
        st.dataframe(df, use_container_width=True)
        st.bar_chart(df.set_index(df.columns[0]))

if st.button("Quay lại"):
    st.switch_page("pages/manager.py")

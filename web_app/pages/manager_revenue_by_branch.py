import streamlit as st
from services.report_service import get_revenue_by_branch, get_years_from_revenue

st.title("Thống kê doanh thu theo chi nhánh")

# Lấy danh sách năm từ bảng DOANHTHUCHINHANH
years = get_years_from_revenue()

if not years:
    st.warning("Không có dữ liệu năm trong hệ thống.")
else:
    selected_year = st.selectbox(
        "Chọn năm:",
        options=years,
        placeholder="Chọn một năm..."
    )

    if st.button("Xem báo cáo"):
        df = get_revenue_by_branch(int(selected_year))
        if df.empty:
            st.warning("Không có dữ liệu cho năm này.")
        else:
            st.dataframe(df, use_container_width=True)
            st.bar_chart(df.set_index(df.columns[0]))

if st.button("Quay lại"):
    st.switch_page("pages/manager.py")

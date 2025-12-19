import streamlit as st
from services.report_service import get_revenue_by_year, get_years_from_revenue

st.title("Thống kê doanh thu theo năm của mỗi chi nhánh")

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
        df = get_revenue_by_year(int(selected_year))
        if df.empty:
            st.warning("Không có dữ liệu cho năm này.")
        else:
            st.dataframe(df, use_container_width=True)
            # Vẽ biểu đồ nếu có dữ liệu
            try:
                chart_df = df.set_index(df.columns[0])
                st.bar_chart(chart_df[chart_df.columns[-1]])
            except Exception as e:
                st.info("Không thể hiển thị biểu đồ.")

if st.button("Quay lại"):
    st.switch_page("pages/manager.py")

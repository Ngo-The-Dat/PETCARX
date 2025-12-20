# Hiện ra danh sách các chức năng cho quản lý lựa chọn
import streamlit as st

st.title("Quản lý - Báo cáo thống kê")
st.write("Chọn chức năng:")

if st.button("Thống kê doanh thu theo năm của mỗi chi nhánh"):
    st.switch_page("pages/manager_revenue_by_year.py")

if st.button("Thống kê doanh thu theo bác sĩ"):
    st.switch_page("pages/manager_revenue_by_doctor.py")

if st.button("Thống kê số lượt khám theo chi nhánh"):
    st.switch_page("pages/manager_visit_count_by_branch.py")

if st.button("Thống kê doanh thu bán sản phẩm"):
    st.switch_page("pages/manager_product_sales_revenue.py")

if st.button("Thống kê doanh thu toàn bộ chi nhánh"):
    st.switch_page("pages/manager_total_revenue_all_branches.py")
    
if st.button("Thông kê doanh thu theo 1 chi nhánh"):
    st.switch_page("pages/manager_revenue_by_branch.py")

if st.button("Quay lại"):
    st.switch_page("app.py")
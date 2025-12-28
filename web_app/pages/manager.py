# Hiện ra danh sách các chức năng cho quản lý lựa chọn
import streamlit as st

st.set_page_config(layout="wide")
st.title("📊 Quản lý - Báo cáo thống kê")
st.caption("Chọn chức năng")

buttons = [
    ("📅 Doanh thu theo năm từng chi nhánh", "pages/manager_revenue_by_year.py"),
    ("🩺 Doanh thu theo bác sĩ", "pages/manager_revenue_by_doctor.py"),
    ("👥 Số lượt khám theo chi nhánh", "pages/manager_visit_count_by_branch.py"),
    ("🛒 Doanh thu bán sản phẩm", "pages/manager_product_sales_revenue.py"),
    ("🏢 Tổng doanh thu toàn bộ chi nhánh", "pages/manager_total_revenue_all_branches.py"),
    ("🏭 Doanh thu theo 1 chi nhánh", "pages/manager_revenue_by_branch.py"),
]


def render_buttons(items):
    if len(items) > 4:
        col1, col2 = st.columns(2)
        split = (len(items) + 1) // 2
        with col1:
            for label, page in items[:split]:
                if st.button(label, use_container_width=True):
                    st.switch_page(page)
        with col2:
            for label, page in items[split:]:
                if st.button(label, use_container_width=True):
                    st.switch_page(page)
    else:
        for label, page in items:
            if st.button(label, use_container_width=True):
                st.switch_page(page)


with st.container():
    render_buttons(buttons)

st.divider()
if st.button("⬅️ Quay lại", use_container_width=True):
    st.switch_page("app.py")
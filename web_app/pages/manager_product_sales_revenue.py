import streamlit as st
from services.report_service import get_product_sales_revenue
from services.product_service import get_all_products

st.title("Thống kê doanh thu bán sản phẩm")

# Lấy danh sách sản phẩm
products = get_all_products()
product_options = {sp[1]: sp[1] for sp in products}  # TENSP: TENSP

selected_product = st.selectbox(
    "Chọn hoặc nhập tên sản phẩm",
    options=list(product_options.keys()),
    placeholder="Chọn hoặc nhập tên sản phẩm",
    accept_new_options=True
)

if st.button("Xem báo cáo"):
    if not selected_product:
        st.warning("Vui lòng chọn sản phẩm.")
    else:
        df = get_product_sales_revenue(selected_product)
        if df.empty:
            st.warning("Không tìm thấy dữ liệu cho sản phẩm này.")
        else:
            st.dataframe(df, use_container_width=True)

if st.button("Quay lại"):
    st.switch_page("pages/manager.py")

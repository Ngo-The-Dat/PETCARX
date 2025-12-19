import streamlit as st
from services.product_service import search_product_name, get_all_products

st.title("Tìm kiếm sản phẩm")

# Lấy danh sách sản phẩm
products = get_all_products()
product_names = [sp[1] for sp in products]

selected_product = st.selectbox(
    "Chọn hoặc nhập tên sản phẩm:",
    options=[""] + product_names,
    index=0,
    placeholder="Nhập để tìm kiếm..."
)

if st.button("Tìm kiếm"):
    if not selected_product:
        st.warning("Vui lòng chọn sản phẩm.")
    else:
        df = search_product_name(selected_product)
        if df.empty:
            st.warning("Không tìm thấy sản phẩm.")
        else:
            st.success(f"Tìm thấy {len(df)} sản phẩm")
            st.dataframe(df, use_container_width=True)

if st.button("Quay lại"):
    st.switch_page("pages/customer.py")



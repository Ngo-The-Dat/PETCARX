# Hiện ra danh sách các chức năng cho khách hàng lựa chọn
import streamlit as st

st.set_page_config(layout="wide")
st.title("🧍‍♂️ Khách hàng")
st.caption("Chọn chức năng")

buttons = [
    ("🛍️ Tìm kiếm sản phẩm", "pages/customer_search_product.py"),
    ("📅 Tra cứu lịch bác sĩ", "pages/customer_search_doctor_schedule.py"),
    ("🧾 Xem lịch sử mua hàng", "pages/customer_product_medical_history.py"),
    ("🐶 Xem lịch sử khám của thú cưng", "pages/customer_pet_medical_history.py"),
]


def render_buttons(items):
    if len(items) > 4:
        col1, col2 = st.columns(2)
        split = (len(items) + 1) // 2
        with col1:
            for label, page in items[:split]:
                if st.button(label, use_container_width=False):
                    st.switch_page(page)
        with col2:
            for label, page in items[split:]:
                if st.button(label, use_container_width=False):
                    st.switch_page(page)
    else:
        for label, page in items:
            if st.button(label, use_container_width=False):
                st.switch_page(page)


with st.container():
    render_buttons(buttons)

st.divider()
if st.button("⬅️ Quay lại", use_container_width=True):
    st.switch_page("app.py")
# Hiện ra danh sách các chức năng cho khách hàng lựa chọn
import streamlit as st

st.title("Customer")
st.write("Chọn chức năng:")

if st.button("Tìm kiếm sản phẩm"):
    st.switch_page("pages/customer_search_product.py")

if st.button("Tra cứu lịch bác sĩ"):
    st.switch_page("pages/customer_search_doctor_schedule.py")

if st.button("Xem lịch sử mua hàng"):
    st.switch_page("pages/customer_product_medical_history.py")

if st.button("Xem lịch sử khám của thú cưng"):
    st.switch_page("pages/customer_pet_medical_history.py")
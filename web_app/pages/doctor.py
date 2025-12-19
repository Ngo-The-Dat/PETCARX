import streamlit as st

st.title("Doctor")
st.write("Chọn chức năng:")

if st.button("Tra cứu lịch sử khám của thú cưng"):
    st.switch_page("pages/doctor_pet_medical_history.py")

if st.button("Tra cứu thuốc"):
    st.switch_page("pages/search_product.py")

if st.button("Tạo bệnh án mới"):
    st.switch_page("pages/create_pet_medical_record.py.py")
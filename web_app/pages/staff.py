# hiện ra danh sách các chức năng cho nhân viên bán hàng lựa chọn
import streamlit as st

st.title("Nhân viên")
st.write("Chọn chức năng:")

if st.button("Tra cứu thú cưng"):
    st.switch_page("pages/staff_search_pet.py")
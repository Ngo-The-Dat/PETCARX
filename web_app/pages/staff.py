# hiện ra danh sách các chức năng cho nhân viên bán hàng lựa chọn
import streamlit as st

st.title("Nhân viên")
st.write("Chọn chức năng:")

if st.button("Tra cứu thú cưng"):
    st.switch_page("pages/staff_search_pet.py")
    
if st.button("Tra cứu khách hàng theo số điện thoại"):
    st.switch_page("pages/staff_search_customer_by_phone_number.py")
    
if st.button("Danh sách tài khoản khách hàng thuộc cấp bậc"):
    st.switch_page("pages/staff_customer_accounts_by_tier.py")
    
if st.button("Tạo hóa đơn cho khách hàng"):
    st.switch_page("pages/staff_create_invoice.py")
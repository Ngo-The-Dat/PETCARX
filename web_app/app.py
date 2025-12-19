# import streamlit as st

# st.set_page_config(
#     page_title="PETCARX Management",
#     layout="wide"
# )

# st.title("Hệ thống quản lý PETCARX")
# st.write("Chọn chức năng bên trái để thao tác")

import streamlit as st

st.set_page_config(page_title="Role-based Demo", layout="centered")

st.title("Hệ thống quản lý")
st.write("Chọn vai trò để tiếp tục:")

col1, col2 = st.columns(2)

with col1:
    if st.button("👤 Customer"):
        st.switch_page("pages/customers/customer_home.py")

    if st.button("🧑‍⚕️ Doctor"):
        st.switch_page("pages/doctors/doctor_home.py")

with col2:
    if st.button("🧑‍💼 Manager"):
        st.switch_page("pages/managers/manager_home.py")

    if st.button("🛒 Sales"):
        st.switch_page("pages/sales/sales_home.py")
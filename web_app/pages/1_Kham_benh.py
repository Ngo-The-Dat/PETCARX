import streamlit as st
from services.khambenh_service import kham_benh_toan_dien

st.header("Khám bệnh & Kê đơn")

# input UI
makb = st.number_input("Mã khám bệnh", step=1)
matc = st.number_input("Mã thú cưng", step=1)
mabacsi = st.number_input("Mã bác sĩ", step=1)

# dynamic list triệu chứng, thuốc...
# submit → gọi service

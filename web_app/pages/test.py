import streamlit as st
from services.schedule_service import get_doctor_schedule


ten = st.text_input("Họ tên")
# macn = st.number_input("MACN")

# if ten:
df = get_doctor_schedule(ten)
df = df.loc[:,~df.columns.duplicated()]

if df.empty:
    st.info("Không có dữ liệu cho mã thú cưng này.")
else:
    st.dataframe(df, hide_index=True)
# else:
st.info("Nhập thông tin.")
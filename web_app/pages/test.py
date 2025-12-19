import streamlit as st
from services.report_service import get_total_revenue_all_branches


# ten = st.text_input("Họ tên")
# macn = st.number_input("MACN")

# if ten:
df = get_total_revenue_all_branches()
df = df.loc[:,~df.columns.duplicated()]

if df.empty:
    st.info("Không có dữ liệu cho mã thú cưng này.")
else:
    st.dataframe(df, hide_index=True)
# else:
st.info("Nhập thông tin.")
import streamlit as st
from services.lichsu_service import lich_su_thu_cung

st.header("Lịch sử khám bệnh và tiêm phòng của thú cưng")

matc = st.number_input("Mã thú cưng", step=1)

if matc:
    df = lich_su_thu_cung(matc)
    df = df.loc[:,~df.columns.duplicated()]
    
    if df.empty:
        st.info("Không có dữ liệu cho mã thú cưng này.")
    else:
        st.dataframe(df, hide_index=True)
else:
    st.info("Nhập mã thú cưng để xem báo cáo.")
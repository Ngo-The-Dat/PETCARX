from services.taikhoan_capdo_service import danhsach_taikhoan_capdo
import streamlit as st

st.header("Danh sách tài khoản thuộc mã cấp độ")

macapdo = st.number_input(label="Mã cấp độ", step=1)

if macapdo:
    df = danhsach_taikhoan_capdo(macapdo)

    if df.empty:
        st.info("Không có dữ liệu cho năm này.")
    else:
        df = df.loc[:,~df.columns.duplicated()]
        st.dataframe(df)
else:
    st.info("Nhập mã cấp độ để xem báo cáo.")
from services.capbac_service import danhsach_taikhoan_capbac
import streamlit as st

st.header("Danh sách tài khoản thuộc mã cấp độ")

macapbac = st.number_input(label="Mã cấp độ", step=1, max_value=3, min_value=1)

if macapbac:
    df = danhsach_taikhoan_capbac(macapbac)

    if df.empty:
        st.info("Không có dữ liệu cho năm này.")
    else:
        df = df.loc[:,~df.columns.duplicated()]
        st.dataframe(df)
else:
    st.info("Nhập mã cấp độ để xem báo cáo.")

if st.button("Quay lại"):
    st.switch_page("pages/staff.py")
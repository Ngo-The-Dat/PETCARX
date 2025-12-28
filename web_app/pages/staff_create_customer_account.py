import streamlit as st
from datetime import date

from services.customer_service import tao_tai_khoan_moi_cho_kh

st.set_page_config(layout="wide")
st.title("🆕 Tạo tài khoản hội viên mới")

with st.form("create_customer_form"):
    col1, col2 = st.columns(2)
    with col1:
        hoten = st.text_input("Họ tên")
        sdt = st.text_input("Số điện thoại (10 số)")
        email = st.text_input("Email")
    with col2:
        cccd = st.text_input("CCCD (12 số)")
        gioitinh = st.selectbox("Giới tính", options=["Nam", "Nữ"], index=0)
        ngaysinh = st.date_input("Ngày sinh", value=date(2000, 1, 1), format="YYYY-MM-DD")

    submitted = st.form_submit_button("💾 Tạo tài khoản")

    if submitted:
        if not all([hoten, sdt, email, cccd]):
            st.warning("Vui lòng nhập đầy đủ thông tin bắt buộc.")
        elif len(sdt) != 10 or not sdt.isdigit():
            st.warning("Số điện thoại phải gồm 10 chữ số.")
        elif len(cccd) != 12 or not cccd.isdigit():
            st.warning("CCCD phải gồm 12 chữ số.")
        else:
            try:
                tao_tai_khoan_moi_cho_kh(hoten, sdt, email, cccd, gioitinh, ngaysinh)
                st.success("Đã tạo tài khoản hội viên thành công.")
            except Exception as exc:
                st.error(f"Lỗi tạo tài khoản: {exc}")

if st.button("Quay lại"):
    st.switch_page("pages/staff.py")

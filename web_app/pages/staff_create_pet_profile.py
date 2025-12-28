import streamlit as st
from datetime import date

from services.pet_service import tao_ho_so_thu_cung

st.set_page_config(layout="wide")
st.title("🐾 Tạo hồ sơ thú cưng")

with st.form("create_pet_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        matk = st.number_input("Mã tài khoản (MATK)", min_value=1, step=1)
        ten = st.text_input("Tên thú cưng")
    with c2:
        loai = st.text_input("Loài")
        giong = st.text_input("Giống")
        ngaysinh = st.date_input("Ngày sinh", value=date(2022, 1, 1), format="YYYY-MM-DD")
    with c3:
        gioitinh = st.selectbox("Giới tính", options=["Nam", "Nữ"], index=0)
        tinhtrang = st.selectbox("Tình trạng sức khỏe", options=["Khỏe", "Bệnh"], index=0)

    submitted = st.form_submit_button("💾 Tạo hồ sơ")

    if submitted:
        if not all([matk, ten, loai, giong]):
            st.warning("Vui lòng nhập đầy đủ thông tin bắt buộc.")
        else:
            try:
                tao_ho_so_thu_cung(
                    int(matk),
                    ten,
                    loai,
                    giong,
                    ngaysinh,
                    gioitinh,
                    tinhtrang,
                )
                st.success("Đã tạo hồ sơ thú cưng thành công.")
            except Exception as exc:
                st.error(f"Lỗi tạo hồ sơ thú cưng: {exc}")

if st.button("Quay lại"):
    st.switch_page("pages/staff.py")

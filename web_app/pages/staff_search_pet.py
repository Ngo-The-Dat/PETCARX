import streamlit as st
import pandas as pd

from services.pet_service import get_pet_by_id

st.set_page_config(page_title="Tra cứu thú cưng", layout="centered")

st.title("🐶 Tra cứu thông tin thú cưng")
st.write("Nhập mã thú cưng (MATC) để xem thông tin chi tiết.")

matc = st.number_input(
    "Mã thú cưng (MATC)",
    min_value=1,
    step=1
)

if st.button("🔍 Tra cứu"):
    df_pet = get_pet_by_id(matc)

    if df_pet.empty:
        st.warning("Không tìm thấy thú cưng với mã đã nhập.")
    else:
        st.subheader("📋 Thông tin thú cưng")

        # Hiển thị dạng key-value (đẹp hơn nếu chỉ 1 dòng)
        pet_info = df_pet.iloc[0]

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Mã thú cưng:**", pet_info.get("MATC", ""))
            st.write("**Tên thú cưng:**", pet_info.get("TEN", ""))
            st.write("**Loài:**", pet_info.get("LOAI", ""))
            st.write("**Giống:**", pet_info.get("GIONG", ""))

        with col2:
            st.write("**Ngày sinh:**", pet_info.get("NGAYSINH", ""))
            st.write("**Giới tính:**", pet_info.get("GIOITINH", ""))
            st.write("**Tình trạng sức khoẻ:**", pet_info.get("TINHTRANGSUCKHOE", ""))
            st.write("**Khách hàng sở hữu:**", pet_info.get("HOTEN", ""))

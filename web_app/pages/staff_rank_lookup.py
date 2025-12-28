import streamlit as st

from services.capbac_service import xacdinh_capbac_theo_sdt
from services.customer_service import get_all_customers

st.set_page_config(layout="centered")
st.title("🔎 Xác định cấp bậc hội viên")

# Lấy danh sách khách hàng để gợi ý SĐT
customers = get_all_customers()
options = [""]
display_to_sdt = {}
if customers:
    display_to_sdt = {f"{sdt} - {hoten}": sdt for sdt, hoten in customers}
    options += list(display_to_sdt.keys())

with st.form("rank_form"):
    selected = st.selectbox(
        "Chọn / nhập số điện thoại",
        options=options,
        index=0,
        placeholder="Gõ để tìm kiếm SĐT...",
    )
    submitted = st.form_submit_button("Tra cứu")

    if submitted:
        if not selected:
            st.warning("Vui lòng chọn số điện thoại.")
        else:
            sdt = display_to_sdt.get(selected, selected)
            try:
                rank = xacdinh_capbac_theo_sdt(sdt)
                if rank:
                    st.success(f"Cấp bậc hiện tại: {rank}")
                else:
                    st.info("Không tìm thấy khách hàng hoặc chưa có cấp bậc.")
            except Exception as exc:
                st.error(f"Lỗi tra cứu: {exc}")

if st.button("Quay lại"):
    st.switch_page("pages/staff.py")

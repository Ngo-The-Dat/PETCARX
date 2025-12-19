import streamlit as st
from services.report_service import get_revenue_by_doctor, get_all_doctors

st.title("Thống kê doanh thu theo bác sĩ")

# Lấy danh sách bác sĩ
doctors = get_all_doctors()

if not doctors:
    st.warning("Không có dữ liệu bác sĩ trong hệ thống.")
else:
    doctor_options = {bs[1]: bs[1] for bs in doctors}  # HOTEN: HOTEN
    
    selected_doctor = st.selectbox(
        "Chọn bác sĩ:",
        options=list(doctor_options.keys()),
        placeholder="Chọn một bác sĩ..."
    )

    if st.button("Xem báo cáo"):
        if not selected_doctor:
            st.warning("Vui lòng chọn bác sĩ.")
        else:
            df = get_revenue_by_doctor(selected_doctor)
            if df.empty:
                st.warning("Không tìm thấy dữ liệu cho bác sĩ này.")
            else:
                st.dataframe(df, use_container_width=True)

if st.button("Quay lại"):
    st.switch_page("pages/manager.py")

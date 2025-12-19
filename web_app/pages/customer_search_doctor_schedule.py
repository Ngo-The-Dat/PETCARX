import streamlit as st
from services.schedule_service import get_doctor_schedule
from services.report_service import get_all_doctors

st.title("Tra cứu lịch bác sĩ")

# Lấy danh sách bác sĩ
doctors = get_all_doctors()
doctor_names = [bs[1] for bs in doctors] if doctors else []

if not doctor_names:
    st.warning("Không có dữ liệu bác sĩ trong hệ thống.")
else:
    selected_doctor = st.selectbox(
        "Chọn bác sĩ:",
        options=[""] + doctor_names,
        index=0,
        placeholder="Chọn một bác sĩ..."
    )

    if st.button("Xem lịch"):
        if not selected_doctor:
            st.warning("Vui lòng chọn bác sĩ.")
        else:
            df = get_doctor_schedule(selected_doctor)
            if df.empty:
                st.info("Bác sĩ hiện không có lịch hẹn.")
            else:
                st.success(f"Tìm thấy {len(df)} lịch hẹn")
                st.dataframe(df, use_container_width=True)

if st.button("Quay lại"):
    st.switch_page("pages/customer.py")

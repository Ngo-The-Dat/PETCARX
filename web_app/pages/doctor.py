import streamlit as st

st.set_page_config(layout="wide")
st.title("👩‍⚕️ Bác sĩ")
st.caption("Chọn chức năng")

buttons = [
    ("📜 Tra cứu lịch sử khám của thú cưng", "pages/doctor_pet_medical_history.py"),
    ("💊 Tra cứu thuốc", "pages/doctor_search_pills.py"),
    ("🩺 Tạo bệnh án mới", "pages/doctor_create_pet_medical_record.py"),
]


def render_buttons(items):
    if len(items) > 4:
        col1, col2 = st.columns(2)
        split = (len(items) + 1) // 2
        with col1:
            for label, page in items[:split]:
                if st.button(label, use_container_width=False):
                    st.switch_page(page)
        with col2:
            for label, page in items[split:]:
                if st.button(label, use_container_width=False):
                    st.switch_page(page)
    else:
        for label, page in items:
            if st.button(label, use_container_width=False):
                st.switch_page(page)


with st.container():
    render_buttons(buttons)

st.divider()
if st.button("⬅️ Quay lại", use_container_width=True):
    st.switch_page("app.py")
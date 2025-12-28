# hiện ra danh sách các chức năng cho nhân viên bán hàng lựa chọn
import streamlit as st

st.set_page_config(layout="wide")
st.title("💼 Nhân viên")
st.caption("Chọn tác vụ cần thực hiện")

buttons = [
    ("🔍 Tra cứu thú cưng", "pages/staff_search_pet.py"),
    ("📞 Tra cứu khách hàng theo số điện thoại", "pages/staff_search_customer_by_phone_number.py"),
    ("⭐ Danh sách tài khoản theo cấp bậc", "pages/staff_customer_accounts_by_tier.py"),
    ("🧾 Tạo hóa đơn cho khách hàng", "pages/staff_create_invoice.py"),
    ("👤 Tạo tài khoản hội viên mới", "pages/staff_create_customer_account.py"),
    ("🐾 Tạo hồ sơ thú cưng", "pages/staff_create_pet_profile.py"),
]


def render_buttons(items):
    if len(items) > 4:
        col1, col2 = st.columns(2)
        split = (len(items) + 1) // 2
        with col1:
            for label, page in items[:split]:
                if st.button(label, use_container_width=True):
                    st.switch_page(page)
        with col2:
            for label, page in items[split:]:
                if st.button(label, use_container_width=True):
                    st.switch_page(page)
    else:
        for label, page in items:
            if st.button(label, use_container_width=True):
                st.switch_page(page)


with st.container():
    render_buttons(buttons)

st.divider()
if st.button("⬅️ Quay lại", use_container_width=True):
    st.switch_page("app.py")
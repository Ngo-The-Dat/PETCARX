import streamlit as st
from services.product_service import get_all_pills, search_pills

st.title("Tra cứu thuốc")

# Lấy danh sách thuốc
pills = get_all_pills()
pill_names = [pill[1] for pill in pills] if pills else []

if not pill_names:
    st.warning("Không có dữ liệu thuốc trong hệ thống.")
else:
    selected_pill = st.selectbox(
        "Chọn hoặc nhập tên thuốc:",
        options=[""] + pill_names,
        index=0,
        placeholder="Nhập để tìm kiếm..."
    )

    if st.button("Tìm kiếm"):
        if not selected_pill:
            st.warning("Vui lòng chọn thuốc.")
        else:
            df = search_pills(selected_pill)
            if df.empty:
                st.warning("Không tìm thấy thuốc.")
            else:
                st.success(f"Tìm thấy {len(df)} kết quả")
                st.dataframe(df, use_container_width=True)

if st.button("Quay lại"):
    st.switch_page("pages/doctor.py")
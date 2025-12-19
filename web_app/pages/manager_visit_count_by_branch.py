import streamlit as st
from services.report_service import get_visit_count_by_branch, get_all_branches

st.title("Thống kê số lượt khám theo chi nhánh")

# Lấy danh sách chi nhánh
branches = get_all_branches()

if not branches:
    st.warning("Không có dữ liệu chi nhánh trong hệ thống.")
else:
    branch_options = {cn[1]: cn[0] for cn in branches}  # TEN: MACN
    
    selected_branch = st.selectbox(
        "Chọn chi nhánh:",
        options=list(branch_options.keys()),
        placeholder="Chọn một chi nhánh..."
    )

    if st.button("Xem báo cáo"):
        if not selected_branch:
            st.warning("Vui lòng chọn chi nhánh.")
        else:
            macn = branch_options[selected_branch]
            df = get_visit_count_by_branch(int(macn))
            if df.empty:
                st.warning("Không có dữ liệu cho chi nhánh này.")
            else:
                st.dataframe(df, use_container_width=True)

if st.button("Quay lại"):
    st.switch_page("pages/manager.py")

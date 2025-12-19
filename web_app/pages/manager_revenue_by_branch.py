import streamlit as st
from services.report_service import get_revenue_by_branch, get_all_branches, get_years_from_revenue

st.title("Thống kê doanh thu theo chi nhánh")

# Lấy danh sách chi nhánh
branches = get_all_branches()
# Lấy danh sách năm
years = get_years_from_revenue()

if not branches:
    st.warning("Không có dữ liệu chi nhánh trong hệ thống.")
elif not years:
    st.warning("Không có dữ liệu năm trong hệ thống.")
else:
    # Tạo options cho chi nhánh: TEN -> MACN
    branch_options = {cn[1]: cn[0] for cn in branches}
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_branch = st.selectbox(
            "Chọn chi nhánh:",
            options=list(branch_options.keys()),
            placeholder="Chọn một chi nhánh..."
        )
    
    with col2:
        selected_year = st.selectbox(
            "Chọn năm:",
            options=years,
            placeholder="Chọn một năm..."
        )

    if st.button("Xem báo cáo"):
        if not selected_branch or not selected_year:
            st.warning("Vui lòng chọn chi nhánh và năm.")
        else:
            macn = branch_options[selected_branch]
            df = get_revenue_by_branch(int(macn), int(selected_year))
            if df.empty:
                st.warning("Không có dữ liệu cho chi nhánh và năm này.")
            else:
                st.success(f"Doanh thu chi nhánh {selected_branch} năm {selected_year}")
                st.dataframe(df, use_container_width=True)
                # Vẽ biểu đồ nếu có dữ liệu
                try:
                    chart_df = df.set_index(df.columns[0])
                    st.bar_chart(chart_df[chart_df.columns[-1]])
                except Exception:
                    pass

if st.button("Quay lại"):
    st.switch_page("pages/manager.py")

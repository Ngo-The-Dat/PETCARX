import streamlit as st
from services.customer_service import tim_kiem_khach_hang, get_all_customers

st.header("🔍 Tìm kiếm khách hàng theo SĐT")

# Lấy danh sách khách hàng
customers = get_all_customers()

if not customers:
    st.warning("Không có dữ liệu khách hàng trong hệ thống.")
else:
    # Tạo options: hiển thị SDT - Họ tên
    customer_options = {f"{c[0]} - {c[1]}": c[0] for c in customers}
    
    selected_customer = st.selectbox(
        "Chọn số điện thoại khách hàng:",
        options=[""] + list(customer_options.keys()),
        index=0,
        placeholder="Chọn hoặc nhập để tìm..."
    )

    # Nút tìm kiếm
    if st.button("🔍 Tìm kiếm", type="primary"):
        if not selected_customer:
            st.warning("⚠️ Vui lòng chọn khách hàng")
        else:
            sdt = customer_options[selected_customer]
            # Tìm kiếm khách hàng
            df = tim_kiem_khach_hang(sdt)
            
            if df.empty:
                st.info(f"ℹ️ Không tìm thấy khách hàng với SĐT: {sdt}")
            else:
                st.success(f"✅ Tìm thấy {len(df)} khách hàng")
                
                # Hiển thị thông tin khách hàng
                for idx, row in df.iterrows():
                    with st.container():
                        st.markdown("---")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**👤 Họ tên:** {row['HOTEN']}")
                            st.markdown(f"**📱 SĐT:** {row['SDT']}")
                            st.markdown(f"**📧 Email:** {row['EMAIL']}")
                            st.markdown(f"**🆔 CCCD:** {row['CCCD']}")
                        
                        with col2:
                            st.markdown(f"**🎂 Ngày sinh:** {row['NGAYSINH']}")
                            st.markdown(f"**⚧ Giới tính:** {row['GIOITINH']}")
                            st.markdown(f"**💳 Mã tài khoản:** {row['MATK']}")
                            st.markdown(f"**⭐ Cấp bậc:** {row['MACAPBAC']}")
                        
                        # Thông tin điểm và chi tiêu
                        st.markdown("### 💰 Thông tin tài khoản")
                        col3, col4 = st.columns(2)
                        with col3:
                            st.metric("Điểm Loyalty", f"{row['DIEM_LOYALTY']:,}")
                        with col4:
                            st.metric("Số tiền đã tiêu", f"{row['SOTIENDATIEU']:,} VNĐ")

# Hiển thị hướng dẫn
with st.expander("ℹ️ Hướng dẫn sử dụng"):
    st.markdown("""
    **Cách tìm kiếm:**
    1. Nhập số điện thoại gồm 10 chữ số
    2. Nhấn nút "Tìm kiếm"
    3. Xem thông tin chi tiết khách hàng
    
    **Thông tin hiển thị:**
    - Thông tin cá nhân: Họ tên, SĐT, Email, CCCD, Ngày sinh, Giới tính
    - Thông tin tài khoản: Mã tài khoản, Cấp bậc thành viên
    - Thông tin giao dịch: Điểm Loyalty, Tổng số tiền đã chi tiêu
    """)

if st.button("Quay lại"):
    st.switch_page("pages/staff.py")
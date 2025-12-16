import streamlit as st
from services.khachhang_service import tim_kiem_khach_hang

st.header("🔍 Tìm kiếm khách hàng theo SĐT")

# Input số điện thoại
sdt = st.text_input(
    "Số điện thoại", 
    placeholder="Nhập 10 số",
    max_chars=10,
    help="Nhập số điện thoại gồm 10 chữ số"
)

# Nút tìm kiếm
if st.button("🔍 Tìm kiếm", type="primary"):
    if not sdt:
        st.warning("⚠️ Vui lòng nhập số điện thoại")
    elif len(sdt) != 10:
        st.warning("⚠️ Số điện thoại phải có 10 chữ số")
    elif not sdt.isdigit():
        st.warning("⚠️ Số điện thoại chỉ được chứa chữ số")
    else:
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

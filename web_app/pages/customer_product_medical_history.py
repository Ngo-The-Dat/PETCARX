import streamlit as st
from services.customer_service import tim_kiem_khach_hang, get_all_customers
from services.order_service import get_lich_su_mua_hang

st.header("🛒 Lịch sử mua hàng của khách hàng")

# Lấy danh sách khách hàng
customers = get_all_customers()

if not customers:
    st.warning("Không có dữ liệu khách hàng trong hệ thống.")
else:
    # Tạo options: hiển thị SDT - Họ tên
    customer_options = {f"{c[0]}": c[0] for c in customers}
    
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
        df_kh = tim_kiem_khach_hang(sdt)
        
        if df_kh.empty:
            st.info(f"ℹ️ Không tìm thấy khách hàng với SĐT: {sdt}")
        else:
            # Lấy thông tin khách hàng đầu tiên
            kh = df_kh.iloc[0]
            matk = int(kh['MATK'])  # Convert to Python int to avoid numpy.int64 error
            
            # Hiển thị thông tin khách hàng
            st.success(f"✅ Tìm thấy khách hàng: {kh['HOTEN']}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Mã tài khoản", matk)
            with col2:
                st.metric("Điểm Loyalty", f"{kh['DIEM_LOYALTY']:,}")
            with col3:
                st.metric("Tổng chi tiêu", f"{kh['SOTIENDATIEU']:,} VNĐ")
            
            st.markdown("---")
            
            # Lấy lịch sử mua hàng
            df_orders = get_lich_su_mua_hang(matk)
            
            if df_orders.empty:
                st.info("ℹ️ Khách hàng chưa có lịch sử mua hàng")
            else:
                st.subheader(f"📋 Lịch sử mua hàng ({len(df_orders)} giao dịch)")
                
                # Hiển thị bảng lịch sử
                st.dataframe(
                    df_orders,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "MAHD": "Mã HĐ",
                        "NGAYLAP": "Ngày lập",
                        "TONGTIEN": st.column_config.NumberColumn(
                            "Tổng tiền",
                            format="%d VNĐ"
                        ),
                        "HINHTHUCTHANHTOAN": "Hình thức TT",
                        "TENCHINHANH": "Chi nhánh",
                        "DIACHICHINHANH": "Địa chỉ",
                        "TENSANPHAM": "Sản phẩm",
                        "SOLUONGSP": "SL",
                        "DONGIASP": st.column_config.NumberColumn(
                            "Đơn giá SP",
                            format="%d VNĐ"
                        ),
                        "THANHTIEN": st.column_config.NumberColumn(
                            "Thành tiền",
                            format="%d VNĐ"
                        ),
                        "TENDICHVU": "Dịch vụ",
                        "DONGIADV": st.column_config.NumberColumn(
                            "Đơn giá DV",
                            format="%d VNĐ"
                        ),
                        "TENTHUCUNG": "Thú cưng"
                    }
                )
                
                # Thống kê
                st.markdown("### 📊 Thống kê")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    total_orders = df_orders['MAHD'].nunique()
                    st.metric("Tổng số đơn hàng", total_orders)
                
                with col2:
                    total_amount = df_orders['TONGTIEN'].sum()
                    st.metric("Tổng giá trị", f"{total_amount:,} VNĐ")
                
                with col3:
                    avg_amount = df_orders['TONGTIEN'].mean()
                    st.metric("Giá trị TB/đơn", f"{avg_amount:,.0f} VNĐ")

# Hiển thị hướng dẫn
with st.expander("ℹ️ Hướng dẫn sử dụng"):
    st.markdown("""
    **Cách xem lịch sử mua hàng:**
    1. Nhập số điện thoại khách hàng (10 chữ số)
    2. Nhấn nút "Tìm kiếm"
    3. Xem lịch sử mua hàng chi tiết
    
    **Thông tin hiển thị:**
    - Thông tin hóa đơn: Mã HĐ, Ngày lập, Tổng tiền, Hình thức thanh toán
    - Chi nhánh: Tên và địa chỉ chi nhánh
    - Sản phẩm: Tên, số lượng, đơn giá, thành tiền
    - Dịch vụ: Tên dịch vụ, đơn giá, thú cưng sử dụng
    - Thống kê: Tổng số đơn, tổng giá trị, giá trị trung bình
    """)
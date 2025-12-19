import streamlit as st
from services.hoadon_service import (
    get_all_chi_nhanh,
    tao_hoa_don_toan_dien,
    get_sanpham_by_chinhanh,
    get_dichvu_by_chinhanh,
    get_nhanvien_by_chucvu,
    get_goi_tiem_by_chinhanh,
    get_thu_cung_by_khachhang
)

st.set_page_config(layout="wide")
st.title("🧾 Hóa đơn & Thanh toán toàn diện")

# =========================
# 1. Thông tin hóa đơn
# =========================
st.subheader("Thông tin hóa đơn")

col1, col2, col3 = st.columns(3)

with col1:
    matk = st.number_input("Mã tài khoản (MATK)", min_value=1, step=1)

with col2:
    all_chinhanh = get_all_chi_nhanh()
    macn = st.selectbox(
        label="Mã chi nhánh (MACN)", 
        options=[cn['MACN'] for cn in all_chinhanh], 
        format_func=lambda x: f"{x} - {next((cn['TEN'] for cn in all_chinhanh if cn['MACN'] == x), '')}" if x is not None else ""
    )

with col3:   
    makm = st.number_input("Mã khuyến mãi (MAKM) - 0 nếu không áp dụng", min_value=0, step=1)
    
st.divider()

# Lấy danh sách sản phẩm và dịch vụ
all_sanpham = []
all_dichvu = []
all_nhanvien = []
all_goitiem = []
all_thucung = []

# Kiểm tra nếu chi nhánh thay đổi, reset lại session state
if "last_macn" not in st.session_state:
    st.session_state.last_macn = macn

if st.session_state.last_macn != macn:
    st.session_state.last_macn = macn
    st.session_state.sanpham = []
    st.session_state.dichvu = []
    st.session_state.nhanvien = []

# Reset dịch vụ khi đổi tài khoản để tránh giữ MATC/dịch vụ cũ
if "last_matk" not in st.session_state:
    st.session_state.last_matk = matk
if st.session_state.last_matk != matk:
    st.session_state.last_matk = matk
    st.session_state.dichvu = []

if macn >= 1:
    try:
        all_sanpham = get_sanpham_by_chinhanh(macn)
        all_dichvu = get_dichvu_by_chinhanh(macn)
        all_nhanvien = get_nhanvien_by_chucvu(macn, "Nhân viên tiếp tân")
        all_goitiem = get_goi_tiem_by_chinhanh(macn)
        all_thucung = get_thu_cung_by_khachhang(matk)
    except Exception as e:
        st.error(f"Lỗi khi tải dữ liệu: {e}")

st.subheader("Nhân viên lập hóa đơn")
nvlap = st.selectbox(
    label="Nhân viên lập", 
    options=[nv['MANV'] for nv in all_nhanvien], 
    format_func=lambda x: next((f"{nv['MANV']} - {nv['HOTEN']}" for nv in all_nhanvien if nv['MANV'] == x), "")             
    )

st.subheader("Hình thức thanh toán")
hinhthucthanhtoan = st.selectbox(label="Hình thức thanh toán",options=("Tiền mặt", "Chuyển khoản"), placeholder="Chọn phương thức thanh toán")



# =========================
# 2. Sản phẩm
# =========================
st.subheader("Sản phẩm")

if "sanpham" not in st.session_state:
    st.session_state.sanpham = []

if all_sanpham:
    for i in range(len(st.session_state.sanpham)):
        c1, c2, c3, c4 = st.columns([3.5, 1, 1.2, 0.8])
        with c1:
            selected_sp = st.selectbox(
                f"Chọn sản phẩm #{i+1}",
                options=[sp['MASP'] for sp in all_sanpham],
                format_func=lambda x: next((f"{sp['TEN']} ({sp['LOAI']}) - {sp['GIABAN']:,.0f} VNĐ" for sp in all_sanpham if sp['MASP'] == x), ""),
                key=f"sp_select_{i}"
            )
            st.session_state.sanpham[i]['MASP'] = selected_sp
            # Tự động điền đơn giá
            sp_info = next((sp for sp in all_sanpham if sp['MASP'] == selected_sp), None)
            if sp_info:
                st.session_state.sanpham[i]['DONGIA'] = float(sp_info['GIABAN'])
        
        with c2:
            st.session_state.sanpham[i]['SOLUONG'] = st.number_input(
                f"Số lượng #{i+1}",
                min_value=1,
                step=1,
                value=st.session_state.sanpham[i].get('SOLUONG', 1),
                key=f"slsp_{i}"
            )
        
        with c3:
            st.markdown(
                f"""
                <div style="margin-top:29px; font-weight:600;">
                    Đơn giá {i+1}: {st.session_state.sanpham[i]['DONGIA']:,.0f} VNĐ
                </div>
                """,
                unsafe_allow_html=True
            )

        with c4:
            if st.button("🗑", key=f"rm_sp_{i}"):
                del st.session_state.sanpham[i]
                st.rerun()

if all_sanpham:
    if st.button("➕ Thêm sản phẩm"):
        st.session_state.sanpham.append({
            'MASP': all_sanpham[0]['MASP'], 
            'SOLUONG': 1, 
            'DONGIA': float(all_sanpham[0]['GIABAN'])
        })
        st.rerun()
else:
    st.info("💡 Vui lòng chọn mã chi nhánh để xem danh sách sản phẩm")

st.divider()

# =========================
# 3. Dịch vụ
# =========================
st.subheader("Dịch vụ")

if "dichvu" not in st.session_state:
    st.session_state.dichvu = []

if not all_thucung:
    st.warning("Khách hàng này không có thú cưng. Không thể chọn dịch vụ.")
    # Xóa mọi dịch vụ đã thêm (nếu có) để tránh lỗi MATC NULL
    if st.session_state.dichvu:
        st.session_state.dichvu = []
else:
    # Chỉ cho phép thao tác dịch vụ khi có thú cưng
    if all_dichvu:
        for i in range(len(st.session_state.dichvu)):
            c1, c2, c3 = st.columns([3, 2.4, 0.8])

            with c1:
                selected_dv = st.selectbox(
                    f"Chọn dịch vụ #{i+1}",
                    options=[dv['MADV'] for dv in all_dichvu],
                    format_func=lambda x: next(
                        dv['TENDV'] for dv in all_dichvu if dv['MADV'] == x
                    ),
                    key=f"dv_{i}"
                )
                st.session_state.dichvu[i]['MADV'] = selected_dv

                dv_info = next((dv for dv in all_dichvu if dv['MADV'] == selected_dv), None)
                if dv_info is None:
                    st.error("⚠️ Dịch vụ không tồn tại")
                    st.stop()
                loaidv = dv_info.get('LOAIDV', 'Khám bệnh')

            with c2:
                # Mã thú cưng cho từng dòng dịch vụ (selectbox)
                if all_thucung:
                    labels_tc = {tc['MATC']: f"{tc['MATC']} - {tc.get('TEN','')}" for tc in all_thucung}
                    matc_selected = st.selectbox(
                        f"Thú cưng #{i+1}",
                        options=[tc['MATC'] for tc in all_thucung],
                        format_func=lambda x: labels_tc.get(x, str(x)),
                        key=f"matc_{i}"
                    )
                    st.session_state.dichvu[i]['MATC'] = matc_selected
                else:
                    # Không có thú cưng nào
                    st.info("💡 Vui lòng thêm thú cưng vào tài khoản để chọn dịch vụ")

                if loaidv == "Khám bệnh":
                    st.number_input(
                        "Giá",
                        value=int(dv_info['GIANIEMYET']),
                        disabled=True,
                        key=f"gia_kham_{i}"
                    )

                elif loaidv == "Tiêm lẻ":
                    vx = st.selectbox(
                        "Vắc xin",
                        options=[sp['MASP'] for sp in all_sanpham if sp['LOAI'] == 'Vắc xin'],
                        format_func=lambda x: next(
                            f"{sp['TEN']}"
                            for sp in all_sanpham if sp['MASP'] == x
                        ),
                        key=f"vx_{i}"
                    )
                    st.session_state.dichvu[i]['MAVX'] = vx
                    # Hiển thị giá vắc xin đã chọn
                    vx_info = next((sp for sp in all_sanpham if sp['MASP'] == vx), None)
                    if vx_info:
                        st.markdown(f"**Giá vắc xin:** {vx_info['GIABAN']:,.0f} VNĐ")

                elif loaidv == "Tiêm gói":
                    gt = st.selectbox(
                        "Gói tiêm",
                        options=[g['MAGT'] for g in all_goitiem],
                        format_func=lambda x: next(
                            g['TENGOITIEM'] for g in all_goitiem if g['MAGT'] == x
                        ),
                        key=f"goi_{i}"
                    )
                    st.session_state.dichvu[i]['MAGT'] = gt
                    st.caption("Giá gói sẽ được tính tự động khi lưu")

            with c3:
                if st.button("🗑", key=f"rm_dv_{i}"):
                    del st.session_state.dichvu[i]
                    st.rerun()

    if all_dichvu and all_thucung:
        if st.button("➕ Thêm dịch vụ"):
            st.session_state.dichvu.append({
                'MADV': all_dichvu[0]['MADV'],
                'MATC': all_thucung[0]['MATC']
            })
            st.rerun()
    else:
        st.info("💡 Vui lòng chọn mã chi nhánh để xem danh sách dịch vụ")

st.divider()

# =========================
# 4. Submit
# =========================
if st.button("💾 Tạo hóa đơn", type="primary"):
    try:
        # Lọc dữ liệu rỗng
        ds_sanpham = [
            (int(x["MASP"]), int(x["SOLUONG"]), float(x["DONGIA"]))
            for x in st.session_state.sanpham
            if x.get("MASP") is not None
        ]
        
        # Đóng gói dịch vụ thành (MATC, LOAI, MASP) phù hợp SP
        ds_dichvu = []
        for x in st.session_state.dichvu:
            if x.get("MADV") is None:
                continue
            madv = int(x["MADV"])
            dv_info = next((dv for dv in all_dichvu if dv['MADV'] == madv), None)
            if not dv_info:
                continue
            loaidv = dv_info.get('LOAIDV', 'Khám bệnh')
            if loaidv == 'Khám bệnh':
                loai = 'Khám'
                masp_param = madv
            elif loaidv == 'Tiêm lẻ':
                loai = 'Tiêm lẻ'
                masp_param = x.get('MAVX')
            elif loaidv == 'Tiêm gói':
                loai = 'Tiêm gói'
                masp_param = x.get('MAGT')
            else:
                continue

            if masp_param is None:
                st.warning("⚠️ Vui lòng chọn đầy đủ thông tin dịch vụ")
                st.stop()

            matc_line = x.get('MATC')
            if matc_line is None:
                st.warning("⚠️ Vui lòng nhập mã thú cưng cho dịch vụ")
                st.stop()
            ds_dichvu.append((int(matc_line), loai, int(masp_param)))

        if not ds_sanpham and not ds_dichvu:
            st.warning("⚠️ Vui lòng nhập ít nhất một sản phẩm hoặc dịch vụ")
            st.stop()

        makm_value = int(makm) if makm > 0 else None

        # =========================
        # DATA ĐỒNG BỘ SERVICE
        # =========================
        data = {
            "matk": int(matk),
            "macn": int(macn),
            "makm": makm_value,
            "nvlap": int(nvlap),
            "sanpham": ds_sanpham,
            "dichvu": ds_dichvu,
            "hinhthucthanhtoan": hinhthucthanhtoan
        }

        tao_hoa_don_toan_dien(data)

        # reset form
        st.session_state.sanpham = []
        st.session_state.dichvu = []
        
        st.success("✅ Tạo hóa đơn thành công!")
        st.balloons()

    except Exception as e:
        st.error(f"❌ Lỗi khi tạo hóa đơn: {str(e)}")
        st.exception(e)
        st.exception(e)
 
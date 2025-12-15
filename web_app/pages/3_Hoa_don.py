import streamlit as st
from services.hoadon_service import (
    tao_hoa_don_toan_dien,
    get_all_sanpham,
    get_sanpham_by_chinhanh,
    get_all_dichvu,
    get_dichvu_by_chinhanh
)

st.set_page_config(layout="wide")
st.title("🧾 Hóa đơn & Thanh toán toàn diện")

# =========================
# 1. Thông tin hóa đơn
# =========================
st.subheader("Thông tin hóa đơn")

col1, col2 = st.columns(2)

with col1:
    matk = st.number_input("Mã tài khoản (MATK)", min_value=1, step=1)

with col2:
    macn = st.number_input("Mã chi nhánh (MACN)", min_value=1, step=1)

st.divider()

# Lấy danh sách sản phẩm và dịch vụ
all_sanpham = []
all_dichvu = []

# Kiểm tra nếu chi nhánh thay đổi, reset lại session state
if "last_macn" not in st.session_state:
    st.session_state.last_macn = macn

if st.session_state.last_macn != macn:
    st.session_state.last_macn = macn
    st.session_state.sanpham = []
    st.session_state.dichvu = []

if macn >= 1:
    try:
        all_sanpham = get_sanpham_by_chinhanh(macn)
        all_dichvu = get_dichvu_by_chinhanh(macn)
    except Exception as e:
        st.error(f"Lỗi khi tải dữ liệu: {e}")

# =========================
# 2. Sản phẩm
# =========================
st.subheader("Sản phẩm")

if "sanpham" not in st.session_state:
    st.session_state.sanpham = []

if all_sanpham:
    for i in range(len(st.session_state.sanpham)):
        c1, c2, c3 = st.columns([3, 1, 2])
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
            st.number_input(
                f"Đơn giá #{i+1}",
                value=int(st.session_state.sanpham[i].get('DONGIA', 0)),
                disabled=True,
                key=f"dgsp_{i}",
                step=1
            )

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

if all_dichvu:
    for i in range(len(st.session_state.dichvu)):
        c1, c2, c3 = st.columns([3, 1, 2])
        with c1:
            selected_dv = st.selectbox(
                f"Chọn dịch vụ #{i+1}",
                options=[dv['MADV'] for dv in all_dichvu],
                format_func=lambda x: next((f"{dv['TENDV']} - {dv['GIANIEMYET']:,.0f} VNĐ" for dv in all_dichvu if dv['MADV'] == x), ""),
                key=f"dv_select_{i}"
            )
            st.session_state.dichvu[i]['MADV'] = selected_dv
            # Tự động điền đơn giá
            dv_info = next((dv for dv in all_dichvu if dv['MADV'] == selected_dv), None)
            if dv_info:
                st.session_state.dichvu[i]['DONGIA'] = float(dv_info['GIANIEMYET'])
        
        with c2:
            st.session_state.dichvu[i]['MATC'] = st.number_input(
                f"Mã thú cưng #{i+1}",
                min_value=1,
                step=1,
                value=st.session_state.dichvu[i].get('MATC', 1),
                key=f"matcdv_{i}"
            )
        
        with c3:
            st.number_input(
                f"Đơn giá #{i+1}",
                value=int(st.session_state.dichvu[i].get('DONGIA', 0)),
                disabled=True,
                key=f"dgdv_{i}",
                step=1
            )

if all_dichvu:
    if st.button("➕ Thêm dịch vụ"):
        st.session_state.dichvu.append({
            'MADV': all_dichvu[0]['MADV'], 
            'MATC': 1, 
            'DONGIA': float(all_dichvu[0]['GIANIEMYET'])
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
        
        ds_dichvu = [
            (int(x["MADV"]), int(x["MATC"]), float(x["DONGIA"]))
            for x in st.session_state.dichvu
            if x.get("MADV") is not None and x.get("MATC") is not None
        ]

        if not ds_sanpham and not ds_dichvu:
            st.warning("⚠️ Vui lòng nhập ít nhất một sản phẩm hoặc dịch vụ")
            st.stop()

        # =========================
        # DATA ĐỒNG BỘ SERVICE
        # =========================
        data = {
            "matk": int(matk),
            "macn": int(macn),
            "sanpham": ds_sanpham,
            "dichvu": ds_dichvu
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
 
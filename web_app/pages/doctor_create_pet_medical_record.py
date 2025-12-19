import streamlit as st
from services.khambenh_service import kham_benh_toan_dien
from services.staff_manage_service import get_doctors


st.set_page_config(layout="wide")
st.title("Tạo hô sơ khám bệnh mới")

# =========================
# 1. Thông tin hồ sơ khám
# =========================
st.subheader("Thông tin hồ sơ khám")

col1, col2, col3 = st.columns(3)

with col1:
    matc = st.number_input("Mã thú cưng (MATC)", min_value=1, step=1)

with col2:
    df_doctors = get_doctors()

    if df_doctors.empty:
        st.warning("Không có bác sĩ nào trong hệ thống.")
        mabacsi = None
    else:
        # Tạo mapping: tên hiển thị -> mã bác sĩ
        doctor_map = {
            f"{row['MANV']} - {row['HOTEN']}": row['MANV']
            for _, row in df_doctors.iterrows()
        }

        selected_doctor = st.selectbox(
            "Chọn bác sĩ",
            options=list(doctor_map.keys())
        )

        mabacsi = doctor_map[selected_doctor]


with col3:
    ngay_tai_kham = st.date_input("Ngày hẹn tái khám")

st.divider()

# =========================
# 2. Triệu chứng
# =========================
st.subheader("Triệu chứng")

if "trieuchung" not in st.session_state:
    st.session_state.trieuchung = [""]

for i in range(len(st.session_state.trieuchung)):
    st.session_state.trieuchung[i] = st.text_input(
        f"Triệu chứng {i+1}",
        value=st.session_state.trieuchung[i],
        key=f"tc_{i}"
    )

if st.button("➕ Thêm triệu chứng"):
    st.session_state.trieuchung.append("")

st.divider()

# =========================
# 3. Chẩn đoán
# =========================
st.subheader("Chẩn đoán")

if "chuandoan" not in st.session_state:
    st.session_state.chuandoan = [""]

for i in range(len(st.session_state.chuandoan)):
    st.session_state.chuandoan[i] = st.text_input(
        f"Chẩn đoán {i+1}",
        value=st.session_state.chuandoan[i],
        key=f"cd_{i}"
    )

if st.button("➕ Thêm chẩn đoán"):
    st.session_state.chuandoan.append("")

st.divider()

# =========================
# 4. Thuốc kê đơn
# =========================
st.subheader("Thuốc kê đơn")

if "thuoc" not in st.session_state:
    st.session_state.thuoc = [{"MASP": None, "SOLUONG": 1}]

for i, row in enumerate(st.session_state.thuoc):
    c1, c2 = st.columns(2)
    with c1:
        row["MASP"] = st.number_input(
            f"Mã thuốc (MASP) #{i+1}",
            min_value=1,
            step=1,
            key=f"masp_{i}"
        )
    with c2:
        row["SOLUONG"] = st.number_input(
            f"Số lượng #{i+1}",
            min_value=1,
            step=1,
            key=f"sl_{i}"
        )

if st.button("➕ Thêm thuốc"):
    st.session_state.thuoc.append({"MASP": None, "SOLUONG": 1})

st.divider()

# =========================
# 5. Submit
# =========================
if st.button("💾 Lưu hồ sơ khám", type="primary"):
    try:
        # Lọc dữ liệu rỗng
        ds_trieuchung = [x for x in st.session_state.trieuchung if x.strip()]
        ds_chuandoan = [x for x in st.session_state.chuandoan if x.strip()]
        ds_thuoc = [
            (int(x["MASP"]), int(x["SOLUONG"]))
            for x in st.session_state.thuoc
            if x["MASP"] is not None
        ]

        if not ds_trieuchung or not ds_chuandoan or not ds_thuoc:
            st.warning("⚠️ Vui lòng nhập đầy đủ triệu chứng, chẩn đoán và thuốc")
            st.stop()

        # =========================
        # DATA ĐỒNG BỘ SERVICE
        # =========================
        data = {
            "matc": int(matc),
            "mabacsi": int(mabacsi),
            "ngaytaikham": ngay_tai_kham,
            "trieuchung": ds_trieuchung,
            "chuandoan": ds_chuandoan,
            "thuoc": ds_thuoc
        }

        kham_benh_toan_dien(data)

        st.success("✅ Lưu hồ sơ khám bệnh thành công")

        # reset form
        st.session_state.trieuchung = [""]
        st.session_state.chuandoan = [""]
        st.session_state.thuoc = [{"MASP": None, "SOLUONG": 1}]

    except Exception as e:
        st.error("❌ Lỗi khi lưu hồ sơ khám")
        st.exception(e)

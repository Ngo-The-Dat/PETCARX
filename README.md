# 🐾 PETCARX

## 📖 Giới thiệu chung

**PETCARX** là đồ án xây dựng hệ thống quản lý chuỗi cửa hàng chăm sóc thú cưng, với trọng tâm nghiên cứu và triển khai các **biện pháp cải thiện hiệu quả truy vấn dữ liệu**.

Hệ thống được xây dựng dựa trên các công nghệ sau:

- **Frontend/Backend**: [Streamlit](https://streamlit.io/) — framework Python giúp xây dựng giao diện web nhanh chóng.
- **Database**: Microsoft SQL Server (local database).
- **Ngôn ngữ**: Python, T-SQL.

Hệ thống phục vụ bốn nhóm người dùng chính: **Khách hàng (Customer)**, **Bác sĩ (Doctor)**, **Quản lý (Manager)** và **Nhân viên (Staff)**, mỗi nhóm có các chức năng riêng phù hợp với vai trò của mình.

---

## ⚙️ Các chức năng chính

### 👤 Customer — Khách hàng
- Tìm kiếm sản phẩm.
- Tra cứu lịch bác sĩ.
- Xem lịch sử mua hàng.
- Xem lịch sử khám thú cưng.

### 🩺 Doctor — Bác sĩ
- Tra cứu lịch sử khám thú cưng.
- Tra cứu thuốc.
- Tạo bệnh án mới.

### 📊 Manager — Quản lý
- Xem doanh thu theo năm của từng chi nhánh.
- Xem doanh thu theo bác sĩ.
- Xem số lượt khám theo chi nhánh.
- Xem doanh thu bán sản phẩm.
- Xem tổng doanh thu toàn bộ các chi nhánh.
- Xem doanh thu theo một chi nhánh cụ thể.

### 🧑‍💼 Staff — Nhân viên
- Tra cứu thú cưng.
- Tra cứu khách hàng theo số điện thoại.
- Xem danh sách tài khoản theo cấp bậc.
- Tạo hóa đơn cho khách hàng.
- Tạo tài khoản hội viên mới.
- Tạo hồ sơ thú cưng.

---

## 🚀 Các biện pháp cải thiện hiệu quả truy suất

Để đảm bảo hệ thống hoạt động mượt mà khi dữ liệu tăng trưởng, nhóm đã đề xuất và triển khai các **Index** và **Partition** trên những bảng có tần suất truy vấn cao.

### 🔹 Bảng `TAIKHOANHOIVIEN`
- **Index đề xuất**:
  - `Non-Clustered Index` trên cột **SDT** — phục vụ Procedure `FIND_KH_THROUGH_SDT` (T1).
  - *Lý do*: Số điện thoại là thuộc tính dùng để tra cứu khách hàng với tần suất cao.
- **Partition đề xuất**:
  - Partition theo **MACAPBAC** — chia dữ liệu theo các cấp bậc (Cơ bản, Thân thiết, VIP).
  - *Lý do*: Giúp tối ưu hóa các báo cáo tình hình hội viên định kỳ hàng tháng.

### 🔹 Bảng `HOADON`
- **Index đề xuất**:
  - `Non-Clustered Index` trên cột **MATK** — phục vụ Procedure `sp_LichSuMuaHang` (T14).
  - *Lý do*: Khách hàng thường xuyên tra cứu lịch sử mua hàng trên web.
- **Partition đề xuất**:
  - Partition theo **NGAYLAP** (theo năm/quý).
  - *Lý do*: Số lượng hóa đơn rất lớn (~500.000 dòng trong dữ liệu mẫu), việc chia vùng theo thời gian giúp tăng tốc độ truy vấn báo cáo doanh thu hàng ngày/tháng/năm.

### 🔹 Bảng `DOANHTHUCHINHANH`
- **Partition đề xuất**:
  - Partition theo **NGAY** (theo năm).
  - *Lý do*: Phục vụ các kịch bản quản lý phân tích hiệu quả kinh doanh theo năm và báo cáo doanh thu toàn hệ thống.

### 🔹 Bảng `HOSOKHAMBENH` & `HOSOTIEMPHONG`
- **Index đề xuất**:
  - `Non-Clustered Index` trên cột **MATC** (Mã thú cưng) — phục vụ Procedure `sp_TraCuuLichSuKhamThuCung` (T7).
  - *Lý do*: Việc tra cứu lịch sử khám/tiêm diễn ra nhiều lần trong ngày khi bác sĩ tiếp nhận thú cưng.

### 🔹 Bảng `SANPHAM`
- **Index đề xuất**:
  - `Non-Clustered Index` trên cột **TEN** — phục vụ Procedure `search_product_name` (T13).
  - *Lý do*: Khách hàng thường xuyên tìm kiếm sản phẩm bằng tên trên web thông qua toán tử `LIKE`.

---

## 🛠️ Hướng dẫn cài đặt và khởi chạy hệ thống

### Bước 1 — Cài đặt thư viện phụ thuộc
Mở terminal tại thư mục gốc của dự án và chạy lệnh:
```bash
pip install -r .\web_app\requirements.txt
```

### Bước 2 — Khởi tạo cơ sở dữ liệu
Mở **SQL Server Management Studio (SSMS)** và thực thi lần lượt các file SQL sau theo đúng thứ tự:

1. `Database.sql` — tạo cấu trúc cơ sở dữ liệu (các bảng, ràng buộc, index, partition).
2. `insert_data.sql` — thêm dữ liệu mẫu vào hệ thống.
3. `proc_trigger.sql` — cài đặt các Stored Procedure và Trigger cần thiết.

### Bước 3 — Khởi chạy ứng dụng web
Sau khi cài đặt xong, chạy lệnh sau để mở trang web:
```bash
streamlit run .\web_app\app.py
```
Trình duyệt sẽ tự động mở ứng dụng tại địa chỉ `http://localhost:8501`.

---

## 📌 Ghi chú
- Đồ án tập trung vào việc **đánh giá và chứng minh hiệu quả** của các biện pháp tối ưu truy vấn (Index, Partition) thông qua so sánh thời gian thực thi trước và sau khi áp dụng.
- Dữ liệu mẫu được thiết kế với quy mô lớn (~500.000 dòng hóa đơn) để thể hiện rõ sự khác biệt về hiệu năng.
--Kịch bản mới Quy trình Khám bệnh & Kê đơn Toàn diện 
-- Triệu chứng (n dòng)
CREATE TYPE TVP_TrieuChung AS TABLE
(
    TRIEUCHUNG NVARCHAR(50)
)
GO

-- Chẩn đoán (n dòng)
CREATE TYPE TVP_ChuanDoan AS TABLE
(
    CHUANDOAN NVARCHAR(50)
)
GO

-- Thuốc (n dòng)
CREATE TYPE TVP_Thuoc AS TABLE
(
    MASP INT,
    SOLUONG INT
)
GO

CREATE TRIGGER trg_TruKhoThuoc
ON CHITIETTOATHUOC
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON

    DECLARE @MASP INT, @SOLUONG INT, @MACN INT, @TON INT

    SELECT TOP 1
        @MASP = i.MASP,
        @SOLUONG = i.SOLUONG,
        @MACN = ns.MACN
    FROM inserted i
    JOIN HOSOKHAMBENH kb ON i.MAKB = kb.MAKB
    JOIN NHANSU ns ON kb.MABACSI = ns.MANV

    -- Khóa tồn kho
    SELECT @TON = SOLUONGTONKHO
    FROM SANPHAM_CHINHANH WITH (UPDLOCK, HOLDLOCK)
    WHERE MASP = @MASP AND MACN = @MACN

    IF @TON < @SOLUONG
    BEGIN
        RAISERROR (N'Không đủ tồn kho thuốc', 16, 1)
        ROLLBACK TRANSACTION
        RETURN
    END

    UPDATE SANPHAM_CHINHANH
    SET SOLUONGTONKHO = SOLUONGTONKHO - @SOLUONG
    WHERE MASP = @MASP AND MACN = @MACN
END
GO

CREATE PROCEDURE sp_KhamBenh_ToanDien
    @MAKB INT,
    @MATC INT,
    @MABACSI INT,
    @NGAYTAIKHAM DATE,

    @DS_TRIEUCHUNG TVP_TrieuChung READONLY,
    @DS_CHUANDOAN TVP_ChuanDoan READONLY,
    @DS_THUOC TVP_Thuoc READONLY
AS
BEGIN
    SET XACT_ABORT ON
    BEGIN TRAN

    -- 1. MASTER
    INSERT INTO HOSOKHAMBENH(MAKB, MATC, MABACSI, NGAYHENTAIKHAM)
    VALUES (@MAKB, @MATC, @MABACSI, @NGAYTAIKHAM)

    -- 2. NHIỀU TRIỆU CHỨNG
    INSERT INTO HOSOTRIEUCHUNG(MAKB, TRIEUCHUNG)
    SELECT @MAKB, TRIEUCHUNG
    FROM @DS_TRIEUCHUNG

    -- 3. NHIỀU CHẨN ĐOÁN
    INSERT INTO HOSOCHUANDOAN(MAKB, CHUANDOAN)
    SELECT @MAKB, CHUANDOAN
    FROM @DS_CHUANDOAN

    -- 4. NHIỀU THUỐC (TRIGGER TỰ KIỂM KHO)
    INSERT INTO CHITIETTOATHUOC(MAKB, MASP, SOLUONG)
    SELECT @MAKB, MASP, SOLUONG
    FROM @DS_THUOC

    COMMIT
END
GO

--Kịch bản 7 Tra cứu Lịch sử Khám bệnh & Vắc-xin
CREATE INDEX idx_HoSoKham_MATC_NGAY
ON HOSOKHAMBENH(MATC)
GO

CREATE INDEX idx_HoSoTiem_MATC_NGAY
ON HOSOTIEMPHONG (MATC, NGAYTIEM)
GO

CREATE PROCEDURE sp_LichSuThuCung
    @MATC INT
AS
BEGIN
    SELECT *
    FROM HOSOKHAMBENH kb
    LEFT JOIN HOSOTIEMPHONG tp ON kb.MATC = tp.MATC
        AND tp.NGAYTIEM >= DATEADD(YEAR,-5,GETDATE())
    WHERE kb.MATC = @MATC
END
GO

--Kịch bản 8 Báo cáo Doanh thu & Hiệu suất Chi nhánh
CREATE PROCEDURE sp_BaoCaoDoanhThu
    @NAM INT
AS
BEGIN
    SELECT MACN,
           MONTH(NGAYLAP) AS THANG,
           SUM(TONGTIEN) AS DOANHTHU
    FROM HOADON
    WHERE YEAR(NGAYLAP) = @NAM
    GROUP BY MACN, MONTH(NGAYLAP)
END
GO

--Kịch bản 6 Tích điểm & Tự động Thăng hạng
CREATE OR ALTER TRIGGER trg_TichDiem_NangHang
ON HOADON
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON

    ------------------------------------------------------------------
    -- BƯỚC 1: CỘNG TIỀN VÀ ĐIỂM LOYALTY
    -- Chỉ áp dụng cho tài khoản vừa thanh toán (bảng inserted)
    ------------------------------------------------------------------
    UPDATE tk
    SET
        tk.SOTIENDATIEU = tk.SOTIENDATIEU + i.TONGTIEN,     -- Cộng tổng tiền đã tiêu
        tk.DIEM_LOYALTY = tk.DIEM_LOYALTY + (i.TONGTIEN / 50000)    -- Cộng điểm
    FROM TAIKHOANHOIVIEN tk
    JOIN inserted i ON tk.MATK = i.MATK


    ------------------------------------------------------------------
    -- BƯỚC 2: XÁC ĐỊNH CẤP BẬC CAO NHẤT ĐẠT ĐƯỢC
    -- Tìm cấp bậc có mức CHITIEUDAT lớn nhất
    -- nhưng KHÔNG vượt quá số tiền khách đã tiêu
    ------------------------------------------------------------------
    UPDATE tk
    SET MACAPBAC = cb.MACAPBAC
    FROM TAIKHOANHOIVIEN tk
    JOIN inserted i ON tk.MATK = i.MATK
    JOIN CAPBACTHANHVIEN cb
        ON cb.CHITIEUDAT = (
            SELECT MAX(CHITIEUDAT)
            FROM CAPBACTHANHVIEN
            WHERE CHITIEUDAT <= tk.SOTIENDATIEU
        )

    -- Nếu chưa đủ điều kiện của bất kỳ cấp nào,
    -- MACAPBAC sẽ giữ nguyên giá trị cũ
END
GO
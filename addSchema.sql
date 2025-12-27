USE PETCARX
GO

----1. Trừ tồn kho khi thêm chi tiết toa thuốc----
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

----2. Thêm hồ sơ khám bệnh----
CREATE PROCEDURE sp_KhamBenh_ToanDien
    @MATC INT,
    @MABACSI INT,
    @NGAYTAIKHAM DATE
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    DECLARE @MAKB INT;

    BEGIN TRAN;

    ----------------------------------------------------------------
    -- 1. SINH MAKB = MAX + 1 (CÓ KHÓA)
    ----------------------------------------------------------------
    SELECT @MAKB = ISNULL(MAX(MAKB), 0) + 1
    FROM HOSOKHAMBENH WITH (UPDLOCK, HOLDLOCK);

    ----------------------------------------------------------------
    -- 2. INSERT HỒ SƠ KHÁM
    ----------------------------------------------------------------
    INSERT INTO HOSOKHAMBENH
        (MAKB, MATC, MABACSI, NGAYHENTAIKHAM)
    VALUES
        (@MAKB, @MATC, @MABACSI, @NGAYTAIKHAM);

    ----------------------------------------------------------------
    -- 3. TRIỆU CHỨNG
    ----------------------------------------------------------------
    INSERT INTO HOSOTRIEUCHUNG
        (MAKB, TRIEUCHUNG)
    SELECT @MAKB, TRIEUCHUNG
    FROM #DS_TRIEUCHUNG;

    ----------------------------------------------------------------
    -- 4. CHẨN ĐOÁN
    ----------------------------------------------------------------
    INSERT INTO HOSOCHUANDOAN
        (MAKB, CHUANDOAN)
    SELECT @MAKB, CHUANDOAN
    FROM #DS_CHUANDOAN;

    ----------------------------------------------------------------
    -- 5. TOA THUỐC (TRIGGER TỰ TRỪ KHO)
    ----------------------------------------------------------------
    INSERT INTO CHITIETTOATHUOC
        (MAKB, MASP, SOLUONG)
    SELECT @MAKB, MASP, SOLUONG
    FROM #DS_THUOC;

    COMMIT;
END
GO

----3. Tra cứu lịch sử khám bệnh và tiêm phòng của thú cưng----
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

----4. Báo cáo doanh thu chi nhánh mỗi tháng theo năm----
CREATE PROCEDURE sp_BaoCaoDoanhThu
    @NAM INT
AS
BEGIN
    SELECT MACN,
        SUM(DOANHTHU) AS DOANHTHU
    FROM DOANHTHUCHINHANH
    WHERE YEAR(NGAY) = @NAM
    GROUP BY MACN, YEAR(NGAY)
    ORDER BY MACN ASC
END
GO

----5. Tích điểm & Tự động Thăng hạng khi thêm hóa đơn----
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

----6. Thêm doanh thu chi nhánh cuối ngày----
CREATE PROCEDURE ADD_DOANHTHUCHINHANH
AS
BEGIN
    INSERT INTO DOANHTHUCHINHANH
    SELECT MACN, NGAYLAP, ISNULL(SUM(TONGTIEN),0)
    FROM HOADON
    WHERE NGAYLAP = CAST(GETDATE() AS DATE)
    GROUP BY MACN, NGAYLAP
END
GO
EXEC ADD_DOANHTHUCHINHANH
GO

----7. Tìm kiếm khách hàng hội viên dựa trên sđt----
CREATE PROCEDURE FIND_KH_THROUGH_SDT
    @SDT CHAR(10)
AS
BEGIN
    SELECT *
    FROM TAIKHOANHOIVIEN
    WHERE SDT = @SDT
END
GO

----8. Danh sách tài khoản hội viên cấp độ----
CREATE PROC TAIKHOANHOIVIEN_CAPBAC
    @MACAPBAC INT
AS
BEGIN
    SELECT *
    FROM TAIKHOANHOIVIEN TK
        JOIN CAPBACTHANHVIEN CB ON TK.MACAPBAC = CB.MACAPBAC
    WHERE CB.MACAPBAC = @MACAPBAC
END
GO

----9. Tạo và cập nhập hoá đơn----
CREATE PROCEDURE sp_CreateInvoice
    @MATK INT,
    @MAKM INT,
    @HINHTHUCTHANHTOAN NVARCHAR(15),
    @MACN INT,
    @NVLAP INT
AS
BEGIN
    DECLARE @MAHD INT
    SELECT @MAHD = ISNULL(MAX(MAHD), 0) + 1
    FROM HOADON
    DECLARE @NGAYLAP DATE = CAST(GETDATE() AS DATE)
    DECLARE @TONGTIEN INT = 0

    IF NOT EXISTS(SELECT 1
    FROM NHANSU
    WHERE @NVLAP = MANV AND CHUCVU = N'Nhân viên tiếp tân')
        THROW 50001, N'Nhân viên không phải là tiếp tân', 1

    INSERT INTO HOADON
        (MAHD, MATK, MAKM, NGAYLAP, TONGTIEN, HINHTHUCTHANHTOAN, MACN, NVLAP)
    VALUES
        (@MAHD, @MATK, @MAKM, @NGAYLAP, @TONGTIEN, @HINHTHUCTHANHTOAN, @MACN, @NVLAP)
END
GO

CREATE PROCEDURE sp_CreateDetailInvoice_Product
    @MAHD INT,
    @MASP INT,
    @SOLUONG INT,
    @DONGIAHIENTAI INT
AS
BEGIN
    DECLARE @GIABAN INT
    SELECT @GIABAN = GIABAN
    FROM SANPHAM
    WHERE MASP = @MASP

    INSERT INTO CTHDSANPHAM (MAHD, MASP, DONGIAHIENTAI, SOLUONG, THANHTIEN)
    VALUES (@MAHD, @MASP, @DONGIAHIENTAI, @SOLUONG, @DONGIAHIENTAI * @SOLUONG)
END
GO

CREATE PROCEDURE sp_CreateDetailInvoice_Service
   @MAHD INT,
   @MATC INT,
   @LOAI NVARCHAR(10),
   @MASP INT
AS
BEGIN
    DECLARE @DONGIAHIENTAI INT
    IF N'Khám' = @LOAI
    BEGIN
        SELECT @DONGIAHIENTAI = GIANIEMYET
        FROM DICHVU
        WHERE MADV = @MASP

        INSERT INTO CTHDDV (MAHD, MATC, MADV, DONGIAHIENTAI)
        VALUES (@MAHD, @MATC, @MASP, @DONGIAHIENTAI)
    END
    ELSE 
    BEGIN
        DECLARE @MADV INT
        IF N'Tiêm gói' = @LOAI
        BEGIN
            SELECT @DONGIAHIENTAI = ISNULL(SUM(CT.SOLUONG * SP.GIABAN), 0) * (1 - GT.PHANTRAMGIAM)
            FROM CHITIETGOITIEM CT
            JOIN SANPHAM SP ON CT.MASP = SP.MASP
            JOIN GOITIEM GT ON CT.MAGT = GT.MAGT
            WHERE CT.MAGT = @MASP
            GROUP BY GT.PHANTRAMGIAM

            SELECT @MADV = MADV
            FROM DICHVU
            WHERE LOAIDV = N'Tiêm gói'

            INSERT INTO CTHDDV (MAHD, MATC, MADV, DONGIAHIENTAI, MADK)
            VALUES (@MAHD, @MATC, @MADV, @DONGIAHIENTAI, @MASP)
        END

        ELSE IF N'Tiêm lẻ' = @LOAI
        BEGIN
            SELECT @DONGIAHIENTAI = GIABAN
            FROM SANPHAM
            WHERE MASP = @MASP

            SELECT @MADV = MADV
            FROM DICHVU
            WHERE LOAIDV = N'Tiêm lẻ'

            INSERT INTO CTHDDV (MAHD, MATC, MADV, DONGIAHIENTAI, MATIEMLE)
            VALUES (@MAHD, @MATC, @MADV, @DONGIAHIENTAI, @MASP)
        END
    END
    
END
GO

CREATE TRIGGER trg_UpdateInvoiceTotal_CTHDSANPHAM
ON CTHDSANPHAM
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    ;
    WITH
        ChangedHD
        AS
        (
                            SELECT MAHD
                FROM inserted
            UNION
                SELECT MAHD
                FROM deleted
        )
    UPDATE hd
    SET TONGTIEN =
        ISNULL((
            SELECT SUM(DONGIAHIENTAI * SOLUONG)
    FROM CTHDSANPHAM sp
    WHERE sp.MAHD = hd.MAHD
        ), 0)
        +
        ISNULL((
            SELECT SUM(DONGIAHIENTAI)
    FROM CTHDDV dv
    WHERE dv.MAHD = hd.MAHD
        ), 0)
        - ISNULL(KM.SOTIENGIAM, 0)
    FROM HOADON hd
        JOIN ChangedHD c ON hd.MAHD = c.MAHD
        LEFT JOIN KHUYENMAI KM ON HD.MAKM = KM.MAKM
END
GO

CREATE TRIGGER trg_UpdateInvoiceTotal_CTHDDV
ON CTHDDV
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    ;
    WITH
        ChangedHD
        AS
        (
                            SELECT MAHD
                FROM inserted
            UNION
                SELECT MAHD
                FROM deleted
        )
    UPDATE hd
    SET TONGTIEN =
        ISNULL((
            SELECT SUM(DONGIAHIENTAI * SOLUONG)
    FROM CTHDSANPHAM sp
    WHERE sp.MAHD = hd.MAHD
        ), 0)
        +
        ISNULL((
            SELECT SUM(DONGIAHIENTAI)
    FROM CTHDDV dv
    WHERE dv.MAHD = hd.MAHD
        ), 0)
        - ISNULL(KM.SOTIENGIAM, 0)
    FROM HOADON hd
        JOIN ChangedHD c ON hd.MAHD = c.MAHD
        LEFT JOIN KHUYENMAI KM ON HD.MAKM = KM.MAKM
END
GO

CREATE OR ALTER PROCEDURE search_product_name
    @TEN NVARCHAR(50)
AS
BEGIN
    select *
    from SANPHAM
    where TEN LIKE '%' + @TEN + '%'
END
GO

CREATE PROCEDURE get_revenue_by_doctor
    @HOTEN NVARCHAR(50)
AS
BEGIN
    SELECT NS.HOTEN, SUM(DOANHTHU) AS TONG_DOANH_THU
    FROM DOANHTHUCHINHANH DT
        JOIN CHINHANH CN ON DT.MACN = CN.MACN
        JOIN NHANSU NS ON NS.MACN = CN.MACN AND CHUCVU = N'Bác sĩ thú y' AND NS.HOTEN = @HOTEN
    GROUP BY NS.HOTEN
END
GO

CREATE PROCEDURE get_visit_count_by_branch
    @MACN INT
AS
BEGIN
    SELECT CN.MACN, COUNT(*) AS SOLUOTKHAM
    FROM CHINHANH CN
        JOIN NHANSU NS ON CN.MACN = NS.MACN AND CHUCVU = N'Bác sĩ thú y'
        JOIN HOSOKHAMBENH HS ON HS.MABACSI = NS.MANV
    WHERE CN.MACN = @MACN
    GROUP BY CN.MACN
END
GO
CREATE PROCEDURE get_product_sales_revenue
    @TEN NVARCHAR(50)
AS
BEGIN
    SELECT SP.TEN, SUM(DOANHTHU) AS TONG_DOANH_THU
    FROM SANPHAM SP
        JOIN SANPHAM_CHINHANH SPCN ON SP.MASP = SPCN.MASP
        JOIN DOANHTHUCHINHANH DT ON DT.MACN = SPCN.MACN
    WHERE TEN = @TEN
    GROUP BY SP.TEN
END
GO
CREATE PROCEDURE get_total_revenue_all_branches
AS
BEGIN
    SELECT YEAR(NGAY) NAM, SUM(DOANHTHU) AS TONG_DOANH_THU
    FROM DOANHTHUCHINHANH
    GROUP BY YEAR(NGAY)
END
GO
CREATE PROCEDURE get_doctor_schedule
    @HOTEN NVARCHAR(50)
AS
BEGIN
    SELECT DISTINCT(HS.NGAYHENTAIKHAM)
    FROM NHANSU NS
        JOIN HOSOKHAMBENH HS ON NS.MANV = HS.MABACSI AND CHUCVU = N'Bác sĩ thú y' AND NS.HOTEN = @HOTEN
    ORDER BY NGAYHENTAIKHAM DESC
END
GO

CREATE PROC sp_TraCuuLichSuKhamThuCung
    @MATC INT
AS
BEGIN
    SELECT MAKB, MABACSI, NGAYHENTAIKHAM
    FROM HOSOKHAMBENH
    WHERE MATC = @MATC
END
GO

CREATE PROC sp_HoSoBenhAnThuCung
    @MATC INT,
    @MAKB INT
AS
BEGIN
    SELECT kb.MAKB, kb.MABACSI, kb.NGAYHENTAIKHAM,
        tc.TRIEUCHUNG,
        cd.CHUANDOAN,
        tt.MASP, tt.SOLUONG
    FROM HOSOKHAMBENH kb
        LEFT JOIN HOSOTRIEUCHUNG tc ON kb.MAKB = tc.MAKB
        LEFT JOIN HOSOCHUANDOAN cd ON kb.MAKB = cd.MAKB
        LEFT JOIN CHITIETTOATHUOC tt ON kb.MAKB = tt.MAKB
    WHERE kb.MATC = @MATC AND kb.MAKB = @MAKB
END
GO

CREATE OR ALTER PROC sp_TraCuuThuCung
    @MATC INT
AS
BEGIN
    SELECT TC.*, TK.HOTEN
    FROM THUCUNG AS TC
        LEFT JOIN TAIKHOANHOIVIEN AS TK ON TC.MATK = TK.MATK
    WHERE MATC = @MATC
END
GO

----Xem lịch sử mua hàng của khách hàng----
CREATE PROCEDURE sp_LichSuMuaHang
    @MATK INT
AS
BEGIN
    SELECT
        hd.MAHD,
        hd.NGAYLAP,
        hd.TONGTIEN,
        hd.HINHTHUCTHANHTOAN,
        cn.TEN AS TENCHINHANH,
        cn.DIACHI AS DIACHICHINHANH,
        sp.TEN AS TENSANPHAM,
        ctsp.SOLUONG AS SOLUONGSP,
        ctsp.DONGIAHIENTAI AS DONGIASP,
        ctsp.THANHTIEN,
        dv.TENDV AS TENDICHVU,
        ctdv.DONGIAHIENTAI AS DONGIADV,
        tc.TEN AS TENTHUCUNG
    FROM HOADON hd
        LEFT JOIN CHINHANH cn ON hd.MACN = cn.MACN
        LEFT JOIN CTHDSANPHAM ctsp ON hd.MAHD = ctsp.MAHD
        LEFT JOIN SANPHAM sp ON ctsp.MASP = sp.MASP
        LEFT JOIN CTHDDV ctdv ON hd.MAHD = ctdv.MAHD
        LEFT JOIN DICHVU dv ON ctdv.MADV = dv.MADV
        LEFT JOIN THUCUNG tc ON ctdv.MATC = tc.MATC
    WHERE hd.MATK = @MATK
    ORDER BY hd.NGAYLAP DESC, hd.MAHD DESC
END
GO

---- lấy danh sách bác sĩ----
CREATE PROCEDURE sp_GetDoctors
AS
BEGIN
    SELECT *
    FROM NHANSU
    WHERE CHUCVU = N'Bác sĩ thú y'
END
GO

CREATE PROC get_all_pills
AS
BEGIN
    SELECT *
    FROM SANPHAM
    WHERE LOAI = N'Thuốc'
END
GO

CREATE PROC search_pills
    @TEN NVARCHAR(50)
AS
BEGIN
    SELECT *
    FROM SANPHAM
    WHERE LOAI = N'Thuốc' AND TEN = @TEN
END
GO
CREATE OR ALTER PROC get_revenue_by_branch
    @MACN INT,
    @NAM INT
AS
BEGIN
    SELECT MONTH(NGAY), SUM(DOANHTHU) DOANHTHU
    FROM DOANHTHUCHINHANH
    WHERE MACN = @MACN AND YEAR(NGAY) = @NAM
    GROUP BY MONTH(NGAY)
    ORDER BY MONTH(NGAY) ASC
END
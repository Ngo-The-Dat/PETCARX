use PETCARX;

go
---------------------------------------------
-- BẬT QUYỀN IMPORT FILE
---------------------------------------------
EXEC sp_configure 'show advanced options',
1;

RECONFIGURE;

EXEC sp_configure 'xp_cmdshell',
1;

RECONFIGURE;

EXEC sp_configure 'Ad Hoc Distributed Queries',
1;

RECONFIGURE;
go

---------------------------------------------
-- Import dữ liệu từ file vào bảng
---------------------------------------------
BULK INSERT CHINHANH
FROM
    'D:PETCARX\data\CHINHANH.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE  = 20000,
        TABLOCK
    );

go 
BULK INSERT NHANSU
FROM
    'D:PETCARX\data\NHANSU.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT LICHSUCONGTAC
FROM
    'D:PETCARX\data\LICHSUCONGTAC.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT DOANHTHUCHINHANH
FROM
    'D:PETCARX\data\DOANHTHUCHINHANH.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT SANPHAM
FROM
    'D:PETCARX\data\SANPHAM.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT SANPHAM_CHINHANH
FROM
    'D:PETCARX\data\SANPHAM_CHINHANH.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT DICHVU
FROM
    'D:PETCARX\data\DICHVU.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT DICHVU_CHINHANH
FROM
    'D:PETCARX\data\DICHVU_CHINHANH.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT CAPBACTHANHVIEN
FROM
    'D:PETCARX\data\CAPBACTHANHVIEN.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT TAIKHOANHOIVIEN
FROM
    'D:PETCARX\data\TAIKHOANHOIVIEN.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT DANHGIA
FROM
    'D:PETCARX\data\DANHGIA.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT THUCUNG
FROM
    'D:PETCARX\data\THUCUNG.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT KHUYENMAI
FROM
    'D:PETCARX\data\KHUYENMAI.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT GOITIEM
FROM
    'D:PETCARX\data\GOITIEM.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT CHITIETGOITIEM
FROM
    'D:PETCARX\data\CHITIETGOITIEM.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT GOITIEM_CHINHANH
FROM
    'D:PETCARX\data\GOITIEM_CHINHANH.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT HOSOKHAMBENH
FROM
    'D:PETCARX\data\HOSOKHAMBENH.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT DANGKYGOITIEM
FROM
    'D:PETCARX\data\DANGKYGOITIEM.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT HOSOTIEMPHONG
FROM
    'D:PETCARX\data\HOSOTIEMPHONG.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT HOSOTRIEUCHUNG
FROM
    'D:PETCARX\data\HOSOTRIEUCHUNG.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT HOSOCHUANDOAN
FROM
    'D:PETCARX\data\HOSOCHUANDOAN.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT CHITIETTOATHUOC
FROM
    'D:PETCARX\data\CHITIETTOATHUOC.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT HOADON
FROM
    'D:PETCARX\data\HOADON.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT CTHDSANPHAM
FROM
    'D:PETCARX\data\CTHDSANPHAM.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );

go 
BULK INSERT CTHDDV
FROM
    'D:PETCARX\data\CTHDDV.csv'
WITH
    (
        FORMAT = 'CSV',
        FIRSTROW = 2,
        FIELDTERMINATOR = ',',
        ROWTERMINATOR = '\n',
        CODEPAGE = '65001',
        BATCHSIZE = 20000,
        TABLOCK
    );
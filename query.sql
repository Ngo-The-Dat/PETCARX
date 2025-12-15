-- file này dùng để chạy các câu query kiểm thử trên database PETCARX
USE PETCARX
GO

select * from HOSOKHAMBENH as h
left join HOSOTRIEUCHUNG as t on h.MAKB = t.MAKB
left join HOSOCHUANDOAN as c on h.MAKB = c.MAKB
left join CHITIETTOATHUOC as ct on h.MAKB = ct.MAKB
where h.MAKB = 150001;

select * from SANPHAM WHERE MASP = 38;
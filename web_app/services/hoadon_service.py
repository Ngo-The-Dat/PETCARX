from db.connection import get_connection

def tao_hoa_don_toan_dien(data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # -----------------------------
        # 1. Tạo hóa đơn
        # -----------------------------
        cursor.execute("""
            EXEC sp_CreateInvoice
                @MATK = ?,
                @MAKM = ?,
                @HINHTHUCTHANHTOAN = ?,
                @MACN = ?,
                @NVLAP = ?
        """, (
            int(data["matk"]),
            data.get("makm"),
            data["hinhthucthanhtoan"],
            int(data["macn"]),
            int(data["nvlap"])
        ))

        # Lấy MAHD vừa tạo
        cursor.execute("SELECT MAX(MAHD) FROM HOADON")
        mahd = cursor.fetchone()[0]

        # -----------------------------
        # 2. Thêm chi tiết sản phẩm
        # -----------------------------
        if data["sanpham"]:
            for sp in data["sanpham"]:
                cursor.execute("""
                    EXEC sp_CreateDetailInvoice_Product
                        @MAHD = ?,
                        @MASP = ?,
                        @SOLUONG = ?,
                        @DONGIAHIENTAI = ?
                """, (
                    mahd,
                    int(sp[0]),  # MASP
                    int(sp[1]),  # SOLUONG
                    int(sp[2]) # DONGIAHIENTAI
                ))

        # -----------------------------
        # 3. Thêm chi tiết dịch vụ
        # -----------------------------
        if data["dichvu"]:
            for dv in data["dichvu"]:
                # dv expected as tuple: (MATC or None, LOAI (nvarchar), MASP (int))
                cursor.execute("""
                    EXEC sp_CreateDetailInvoice_Service
                        @MAHD = ?,
                        @MATC = ?,
                        @LOAI = ?,
                        @MASP = ?
                """, (
                    mahd,
                    dv[0],           # MATC (can be None)
                    dv[1],           # LOAI (nvarchar): 'Khám' | 'Tiêm lẻ' | 'Tiêm gói'
                    int(dv[2])      # MASP (int): MADV or MAVX or MAGT depending on LOAI
                ))

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


def get_all_chi_nhanh():
    """Lấy danh sách tất cả chi nhánh"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT MACN, TEN
            FROM CHINHANH
        """)
        
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        return results
    
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def get_sanpham_by_chinhanh(macn: int):
    """Lấy danh sách sản phẩm có tồn kho tại chi nhánh"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT sp.MASP, sp.TEN, sp.GIABAN, sp.LOAI, spcn.SOLUONGTONKHO
            FROM SANPHAM sp
            INNER JOIN SANPHAM_CHINHANH spcn ON sp.MASP = spcn.MASP
            WHERE spcn.MACN = ? AND spcn.SOLUONGTONKHO > 0
            ORDER BY sp.TEN
        """, (int(macn),))
        
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        return results
    
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()

def get_dichvu_by_chinhanh(macn: int):
    """Lấy danh sách dịch vụ có tại chi nhánh"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT dv.MADV, dv.TENDV, dv.GIANIEMYET, dv.LOAIDV
            FROM DICHVU dv
            INNER JOIN DICHVU_CHINHANH dvcn ON dv.MADV = dvcn.MADV
            WHERE dvcn.MACN = ?
            ORDER BY dv.TENDV
        """, (int(macn),))
        
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        return results
    
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()
        
def get_nhanvien_by_chucvu(macn: int, chucvu: str = "Nhân viên tiếp tân"):
    # Lấy danh sách nhân viên thuộc 1 chức vụ nào đó
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
        SELECT MANV, HOTEN
        FROM NHANSU
        WHERE MACN = ?
        AND CHUCVU = ?""", (int(macn), chucvu))
    
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
    
        return results
    
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()
        
def get_goi_tiem_by_chinhanh(macn: int):
    """Lấy danh sách gói tiêm có tại chi nhánh"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT gt.MAGT, gt.TENGOITIEM
            FROM GOITIEM gt
            INNER JOIN GOITIEM_CHINHANH gtcn ON gt.MAGT = gtcn.MAGT
            WHERE gtcn.MACN = ?
            ORDER BY gt.TENGOITIEM
        """, (int(macn),))
        
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        return results
    
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()
        
def get_thu_cung_by_khachhang(matk: int):
    """Lấy danh sách thú cưng của khách hàng"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT MATC, TEN
            FROM THUCUNG
            WHERE MATK = ?
            ORDER BY TEN
        """, (int(matk),))
        
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        return results
    
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()    
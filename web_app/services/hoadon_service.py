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
                @MACN = ?
        """, (
            int(data["matk"]),
            int(data["macn"])
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
                    float(sp[2]) # DONGIAHIENTAI
                ))

        # -----------------------------
        # 3. Thêm chi tiết dịch vụ
        # -----------------------------
        if data["dichvu"]:
            for dv in data["dichvu"]:
                cursor.execute("""
                    EXEC sp_CreateDetailInvoice_Service
                        @MAHD = ?,
                        @MADV = ?,
                        @MATC = ?,
                        @DONGIAHIENTAI = ?
                """, (
                    mahd,
                    int(dv[0]),  # MADV
                    int(dv[1]),  # MATC
                    float(dv[2]) # DONGIAHIENTAI
                ))

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


def get_all_sanpham():
    """Lấy danh sách tất cả sản phẩm"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT MASP, TEN, GIABAN, LOAI
            FROM SANPHAM
            ORDER BY TEN
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


def get_all_dichvu():
    """Lấy danh sách tất cả dịch vụ"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT MADV, TENDV, GIANIEMYET
            FROM DICHVU
            ORDER BY TENDV
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


def get_dichvu_by_chinhanh(macn: int):
    """Lấy danh sách dịch vụ có tại chi nhánh"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT dv.MADV, dv.TENDV, dv.GIANIEMYET
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
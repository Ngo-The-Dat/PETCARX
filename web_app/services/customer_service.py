import pandas as pd

from db.connection import get_connection


def get_all_customers():
    """Lấy danh sách tất cả khách hàng (SDT, HOTEN)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SDT, HOTEN FROM TAIKHOANHOIVIEN ORDER BY HOTEN")
        rows = cursor.fetchall()
        if not rows:
            return []
        return rows

def tim_kiem_khach_hang(sdt: str) -> pd.DataFrame:
    """Tìm kiếm khách hàng theo số điện thoại."""
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
                EXEC FIND_KH_THROUGH_SDT
                    ?
            """,
            (sdt,),
        )
        
        rows = cursor.fetchall()
        if not rows:
            return pd.DataFrame()
        
        columns = [col[0] for col in cursor.description]
        return pd.DataFrame.from_records(rows, columns=columns)


def tao_tai_khoan_moi_cho_kh(hoten: str, sdt: str, email: str, cccd: str, gioitinh: str, ngaysinh):
    """Gọi TAO_TAIKHOANMOI_CHO_KH để tạo tài khoản hội viên mới."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "EXEC TAO_TAIKHOANMOI_CHO_KH ?, ?, ?, ?, ?, ?",
            (hoten, sdt, email, cccd, gioitinh, ngaysinh),
        )
        conn.commit()




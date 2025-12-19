import pandas as pd

from db.connection import get_connection


def get_lich_su_mua_hang(matk: int) -> pd.DataFrame:
    """Xem lịch sử mua hàng của khách hàng theo mã tài khoản.
    
    Args:
        matk: Mã tài khoản khách hàng
        
    Returns:
        DataFrame chứa lịch sử mua hàng bao gồm:
        - Thông tin hóa đơn (MAHD, NGAYLAP, TONGTIEN, HINHTHUCTHANHTOAN)
        - Thông tin chi nhánh (TENCHINHANH, DIACHICHINHANH)
        - Thông tin sản phẩm (TENSANPHAM, SOLUONGSP, DONGIASP, THANHTIEN)
        - Thông tin dịch vụ (TENDICHVU, DONGIADV, TENTHUCUNG)
    """
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
                EXEC sp_LichSuMuaHang
                    ?
            """,
            (matk,),
        )
        
        rows = cursor.fetchall()
        if not rows:
            return pd.DataFrame()
        
        columns = [col[0] for col in cursor.description]
        return pd.DataFrame.from_records(rows, columns=columns)
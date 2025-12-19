import pandas as pd

from db.connection import get_connection

# Tra cứu thú cưng (Tìm kiếm thú cưng)
def get_pet_by_id(matc: int) -> pd.DataFrame:
    """
    Gọi sp_TraCuuThuCung
    Trả về thông tin thú cưng theo MATC
    """
    conn = get_connection()

    query = "EXEC sp_TraCuuThuCung ?"
    df = pd.read_sql(query, conn, params=[matc])

    conn.close()
    return df


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




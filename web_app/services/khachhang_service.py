import pandas as pd

from db.connection import get_connection


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

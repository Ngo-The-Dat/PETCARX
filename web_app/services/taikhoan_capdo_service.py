from db.connection import get_connection
import pandas as pd

def danhsach_taikhoan_capdo(macapdo):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "EXEC TAIKHOAN_CAPBAC ?",
            (macapdo)
        )
        rows = cursor.fetchall()
        if not rows:
            return pd.DataFrame()
        columns = [col[0] for col in cursor.description]
        return pd.DataFrame.from_records(data=rows, columns=columns)
from db.connection import get_connection
import pandas as pd

def get_doctors() -> pd.DataFrame:
    """
    Gọi sp_GetDoctors
    Trả về danh sách bác sĩ thú y
    """
    conn = get_connection()

    query = "EXEC sp_GetDoctors"
    df = pd.read_sql(query, conn)

    conn.close()
    return df
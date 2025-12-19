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

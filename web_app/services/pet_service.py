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


def tao_ho_so_thu_cung(
    matk: int,
    ten: str,
    loai: str,
    giong: str,
    ngaysinh,
    gioitinh: str,
    tinhtrangsuckhoe: str,
):
    """Gọi TAO_HOSOTHUCUNG để tạo hồ sơ thú cưng mới."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "EXEC TAO_HOSOTHUCUNG ?, ?, ?, ?, ?, ?, ?",
            (matk, ten, loai, giong, ngaysinh, gioitinh, tinhtrangsuckhoe),
        )
        conn.commit()

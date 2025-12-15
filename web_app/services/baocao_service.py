import pandas as pd

from db.connection import get_connection


def bao_cao_doanh_thu_theo_nam(nam: int) -> pd.DataFrame:
    """Trả về DataFrame doanh thu theo tháng của từng chi nhánh trong năm."""

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
                EXEC sp_BaoCaoDoanhThu
                    ?
            """,
            (nam,),
        )

        rows = cursor.fetchall()
        if not rows:
            return pd.DataFrame(columns=["MACN", "THANG", "DOANHTHU"])

        columns = [col[0] for col in cursor.description]
        return pd.DataFrame.from_records(rows, columns=columns)

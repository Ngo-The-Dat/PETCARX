import pandas as pd

from db.connection import get_connection


def lich_su_thu_cung(matc: int) -> pd.DataFrame:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
                EXEC sp_LichSuThuCung
                    ?
            """,
            (matc),
        )

        rows = cursor.fetchall()
        if not rows:
            return pd.DataFrame()

        columns = [col[0] for col in cursor.description]
        return pd.DataFrame.from_records(rows, columns=columns)

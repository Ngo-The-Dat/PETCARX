# Tìm kiếm sản phẩm/tra cứu thuốc
import pandas as pd
from db.connection import get_connection

def search_product_name(ten: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
                EXEC search_product_name ?
            """,
            (ten),
        )

        rows = cursor.fetchall()
        if not rows:
            return pd.DataFrame()

        columns = [col[0] for col in cursor.description]
        return pd.DataFrame.from_records(rows, columns=columns)

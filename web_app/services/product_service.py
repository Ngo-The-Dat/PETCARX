# Tìm kiếm sản phẩm/tra cứu thuốc
import pandas as pd
from db.connection import get_connection

def get_all_products():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MASP, TEN FROM SANPHAM ORDER BY TEN")
        rows = cursor.fetchall()
        if not rows:
            return []
        return rows

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

def get_all_pills():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC get_all_pills")
        rows = cursor.fetchall()
        if not rows:
            return []
        return rows
    
def search_pills(ten: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
                EXEC search_pills ?
            """,
            (ten),
        )

        rows = cursor.fetchall()
        if not rows:
            return pd.DataFrame()

        columns = [col[0] for col in cursor.description]
        return pd.DataFrame.from_records(rows, columns=columns)
import pandas as pd
from db.connection import get_connection
# thống kê doanh thu theo chi nhánh
def get_revenue_by_branch(nam: int):
    with get_connection() as connect:
        cursor = connect.cursor()
        cursor.execute(
            """
            EXEC sp_BaoCaoDoanhThu ?
            """,
            (nam)
        )
        
        rows = cursor.fetchall()
        if not rows:
            return pd.DataFrame()
        
        columns = [col[0] for col in cursor.description]
        return pd.DataFrame.from_records(data=rows, columns=columns)



# thống kê doanh thu theo bác sĩ
def get_revenue_by_doctor(hoten: str):
    with get_connection() as connect:
        cursor = connect.cursor()
        cursor.execute(
            """
            EXEC get_revenue_by_doctor ?
            """,
            (hoten)
        )
        
        rows = cursor.fetchall()
        if not rows:
            return pd.DataFrame()
        
        columns = [col[0] for col in cursor.description]
        return pd.DataFrame.from_records(data=rows, columns=columns)

# thống kê số lượt khám của các chi nhánh
def get_visit_count_by_branch(macn: int):
    with get_connection() as connect:
        cursor = connect.cursor()
        cursor.execute(
            """
            EXEC get_visit_count_by_branch ?
            """,
            (macn)
        )
        
        rows = cursor.fetchall()
        if not rows:
            return pd.DataFrame()
        
        columns = [col[0] for col in cursor.description]
        return pd.DataFrame.from_records(columns=columns, data=rows)

# thống kê doanh thu bán sản phẩm
def get_product_sales_revenue(ten: str):
    with get_connection() as connect:
        cursor = connect.cursor()
        cursor.execute("EXEC get_product_sales_revenue ?", (ten))
        rows = cursor.fetchall()
        if not rows:
            return pd.DataFrame()
        
        columns = [col[0] for col in cursor.description]
        return pd.DataFrame.from_records(columns=columns, data=rows)

# thống kê doanh thu toàn bộ chi nhánh
def get_total_revenue_all_branches():
    with get_connection() as connect:
        cursor = connect.cursor()
        cursor.execute("EXEC get_total_revenue_all_branches")
        rows = cursor.fetchall()
        if not rows:
            return pd.DataFrame()
        
        columns = [col[0] for col in cursor.description]
        return pd.DataFrame.from_records(columns=columns, data=rows)
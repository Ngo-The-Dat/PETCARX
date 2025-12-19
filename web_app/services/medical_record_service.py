from db.connection import get_connection
import pandas as pd
# Tạo hồ sơ bệnh án
def kham_benh_toan_dien(data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # -----------------------------
        # 1. Tạo temp tables
        # -----------------------------
        cursor.execute("""
            CREATE TABLE #DS_TRIEUCHUNG (
                TRIEUCHUNG NVARCHAR(50)
            );
            CREATE TABLE #DS_CHUANDOAN (
                CHUANDOAN NVARCHAR(50)
            );
            CREATE TABLE #DS_THUOC (
                MASP INT,
                SOLUONG INT
            );
        """)

        # -----------------------------
        # 2. Đổ dữ liệu vào temp tables
        # -----------------------------
        if data["trieuchung"]:
            cursor.executemany(
                "INSERT INTO #DS_TRIEUCHUNG VALUES (?)",
                [(str(tc),) for tc in data["trieuchung"]]
            )

        if data["chuandoan"]:
            cursor.executemany(
                "INSERT INTO #DS_CHUANDOAN VALUES (?)",
                [(str(cd),) for cd in data["chuandoan"]]
            )

        if data["thuoc"]:
            cursor.executemany(
                "INSERT INTO #DS_THUOC VALUES (?, ?)",
                [
                    (int(t[0]), int(t[1]))
                    for t in data["thuoc"]
                ]
            )

        # -----------------------------
        # 3. Gọi stored procedure
        # -----------------------------
        cursor.execute("""
            EXEC sp_KhamBenh_ToanDien
                @MATC = ?,
                @MABACSI = ?,
                @NGAYTAIKHAM = ?
        """, (
            int(data["matc"]),
            int(data["mabacsi"]),
            data["ngaytaikham"]
        ))

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()

# Tra cứu lịch sử khám theo thú cưng(những lần khám của thú cưng)
def get_visit_history(matc: int) -> pd.DataFrame:
    """
    Gọi sp_TraCuuLichSuKhamThuCung
    Trả về danh sách các lần khám của thú cưng
    """
    conn = get_connection()

    query = "EXEC sp_TraCuuLichSuKhamThuCung ?"
    df = pd.read_sql(query, conn, params=[matc])

    conn.close()
    return df

# Tra cứu hồ sở bệnh án của thú cưng
def get_visit_detail(matc: int, makb: int) -> pd.DataFrame:
    """
    Gọi sp_HoSoBenhAnThuCung
    Trả về chi tiết bệnh án của 1 lần khám
    """
    conn = get_connection()

    query = "EXEC sp_HoSoBenhAnThuCung ?, ?"
    df = pd.read_sql(query, conn, params=[matc, makb])

    conn.close()
    return df

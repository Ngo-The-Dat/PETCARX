from db.connection import get_connection

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

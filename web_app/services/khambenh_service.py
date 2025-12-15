from db.connection import get_connection

def kham_benh_toan_dien(data: dict):
    conn = get_connection()
    conn.autocommit = False
    cursor = conn.cursor()

    try:
        # ===== 1. TẠO TEMP TABLE =====
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

        # ===== 2. INSERT TRIỆU CHỨNG =====
        cursor.executemany(
            "INSERT INTO #DS_TRIEUCHUNG (TRIEUCHUNG) VALUES (?)",
            [(str(x),) for x in data["tvp_trieuchung"]["TRIEUCHUNG"]]
        )

        # ===== 3. INSERT CHẨN ĐOÁN =====
        cursor.executemany(
            "INSERT INTO #DS_CHUANDOAN (CHUANDOAN) VALUES (?)",
            [(str(x),) for x in data["tvp_chuandoan"]["CHUANDOAN"]]
        )

        # ===== 4. INSERT THUỐC =====
        cursor.executemany(
            "INSERT INTO #DS_THUOC (MASP, SOLUONG) VALUES (?, ?)",
            [
                (int(row["MASP"]), int(row["SOLUONG"]))
                for _, row in data["tvp_thuoc"].iterrows()
            ]
        )

        # ===== 5. EXEC STORED PROCEDURE =====
        cursor.execute("""
            EXEC sp_KhamBenh_ToanDien
                @MAKB = ?,
                @MATC = ?,
                @MABACSI = ?,
                @NGAYTAIKHAM = ?
        """, (
            int(data["makb"]),
            int(data["matc"]),
            int(data["mabacsi"]),
            data["ngaytaikham"]
        ))

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()

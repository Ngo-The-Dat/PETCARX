from db.connection import get_connection

def kham_benh_toan_dien(data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1. Tạo hồ sơ khám
        cursor.execute("""
            EXEC sp_CreateMedicalRecord
                @MATC = ?,
                @MABACSI = ?,
                @NGAYTAIKHAM = ?
        """, (
            int(data["matc"]),
            int(data["mabacsi"]),
            data["ngaytaikham"]
        ))

        makb = cursor.fetchone()[0]

        # 2. Triệu chứng
        for tc in data.get("trieuchung", []):
            cursor.execute("""
                EXEC sp_AddSymptom
                    @MAKB = ?,
                    @TRIEUCHUNG = ?
            """, (makb, str(tc)))

        # 3. Chẩn đoán
        for cd in data.get("chuandoan", []):
            cursor.execute("""
                EXEC sp_AddDiagnosis
                    @MAKB = ?,
                    @CHUANDOAN = ?
            """, (makb, str(cd)))

        # 4. Toa thuốc
        for sp in data.get("thuoc", []):
            print("toa thuoc: ", sp)
            cursor.execute("""
                EXEC sp_AddPrescription
                    @MAKB = ?,
                    @MASP = ?,
                    @SOLUONG = ?
            """, (makb, int(sp[0]), int(sp[1])))

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()
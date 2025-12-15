from db.connection import get_connection

def kham_benh_toan_dien(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        EXEC sp_KhamBenh_ToanDien
            ?, ?, ?, ?, ?, ?, ?
    """, (
        data["makb"],
        data["matc"],
        data["mabacsi"],
        data["ngaytaikham"],
        data["tvp_trieuchung"],
        data["tvp_chuandoan"],
        data["tvp_thuoc"]
    ))

    conn.commit()
    conn.close()

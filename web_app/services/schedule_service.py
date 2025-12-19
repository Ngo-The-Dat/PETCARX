from db.connection import get_connection
import pandas as pd
# tra cứu lịch bác sĩ, dựa vào ngày hẹn tái khám của các hồ sơ bệnh án
def get_doctor_schedule(hoten: str):
    with get_connection() as connect:
        cursor = connect.cursor()
        cursor.execute("EXEC get_doctor_schedule ?", hoten)
        rows = cursor.fetchall()
        if not rows:
            return pd.DataFrame()
        columns = [col[0] for col in cursor.description]
        return pd.DataFrame.from_records(columns=columns, data=rows)
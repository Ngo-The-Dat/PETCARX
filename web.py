from sqlalchemy import create_engine, text
import streamlit as st
import pandas as pd
from os import getenv
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(getenv("SQL_CONNECTION_STRING"))
connetion = engine.connect()
# 2. Truy vấn dữ liệu cho báo cáo
st.title("Báo cáo Doanh thu Chi nhánh")
nam_selected = st.number_input("Chọn năm", value=2021)


select_query = """
SELECT *
FROM HOSOTIEMPHONG TP
JOIN THUCUNG TC ON TP.MATC = TC.MATC
JOIN SANPHAM SP ON TP.LOAIVACXIN = SP.MASP
WHERE TC.MATC = 8282
"""

# data = pd.read_sql_query(select_query, connection)
df = pd.read_sql(select_query, connetion)
df = pd.DataFrame.drop_duplicates(df)
df = df.loc[:,~df.columns.duplicated()]

st.dataframe(df)

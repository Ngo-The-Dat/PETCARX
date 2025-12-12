import sqlalchemy
import streamlit as st
import pandas as pd
from os import getenv
from dotenv import load_dotenv

load_dotenv()
engine = sqlalchemy.create_engine(getenv('SQL_CONNECTION_STRING'))
connetion = engine.connect()

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

df.to_csv('test.csv')
st.dataframe(df)

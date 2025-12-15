import pandas as pd

def tvp_trieu_chung(ds):
    return pd.DataFrame(ds, columns=["TRIEUCHUNG"])

def tvp_chuan_doan(ds):
    return pd.DataFrame(ds, columns=["CHUANDOAN"])

def tvp_thuoc(ds):
    return pd.DataFrame(ds, columns=["MASP", "SOLUONG"])

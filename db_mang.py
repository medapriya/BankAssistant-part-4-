import pandas as pd

def get_dbdata(acc_holder_name, requested):
    df = pd.read_excel("Bank_database.xls", sheet_name=acc_holder_name)
    return (df[requested][0])
    
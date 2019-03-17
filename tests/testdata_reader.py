import pandas as pd

_TEST_DATA_PATH = "tests/test_results.xlsx"

def read_dataframe(sheet_name, index_col=0, usecols=None):
    return pd.read_excel(_TEST_DATA_PATH, sheet_name, index_col=index_col, usecols=usecols)

def read_series(sheet_name, index_col=0, usecols=None):
    return pd.read_excel(_TEST_DATA_PATH, sheet_name, index_col=index_col, usecols=usecols, squeeze=True)

def read_dataframe_raw(sheet_name):
    return pd.read_excel(_TEST_DATA_PATH, sheet_name, header=None)
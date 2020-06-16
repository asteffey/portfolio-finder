"""Extracts tests data from Excel file used as source of truth."""

import os
from typing import List

import pandas as pd

_TEST_DATA_PATH = os.path.dirname(__file__) + "/test_results.xlsx"


def read_dataframe(sheet_name: str, index_col=None, usecols: List[str] = None) -> pd.DataFrame:
    """Reads an Excel sheet as a DataFrame.

    :param sheet_name: the Excel sheet name
    :param index_col: column to use as row label
    :param usecols: the column names to use

    :return a DataFrame of the sheet
    """
    return pd.read_excel(_TEST_DATA_PATH, sheet_name, index_col=index_col, usecols=usecols)

def read_series(sheet_name, usecols=None) -> pd.Series:
    """Reads an Excel sheet as a Series.

    :param sheet_name: the Excel sheet name
    :param usecols: the column names to use

    :return a Series of the sheet
    """
    return pd.read_excel(_TEST_DATA_PATH, sheet_name, index_col=0, usecols=usecols, squeeze=True)

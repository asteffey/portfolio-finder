from typing import Dict
import pandas as pd


def to_dataframe(series_by_allocation: Dict[tuple, pd.Series]) -> pd.DataFrame:
    """Converts dict of Series, by allocation, to a DataFrame.

    :param series_by_allocation: dict of series, by allocation
    :return: dataframe
    """
    dataframe = pd.concat(series_by_allocation, axis=1).T

    an_allocation = list(series_by_allocation.keys())[0]
    allocation_symbols = list(an_allocation._asdict().keys())
    dataframe.index.names = allocation_symbols

    return dataframe

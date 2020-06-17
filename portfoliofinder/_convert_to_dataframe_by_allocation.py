from typing import Dict
import pandas as pd


def _convert_to_dataframe_by_allocation(data_by_allocation: Dict[tuple, pd.Series]):
    dataframe = pd.concat(data_by_allocation, axis=1).T

    an_allocation = list(data_by_allocation.keys())[0]
    allocation_symbols = list(an_allocation._asdict().keys())
    dataframe.index.names = allocation_symbols

    return dataframe

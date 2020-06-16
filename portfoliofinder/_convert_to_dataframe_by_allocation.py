import pandas as pd


def _convert_to_dataframe_by_allocation(series_dict_by_allocation):
    df = pd.concat(series_dict_by_allocation, axis=1).T

    an_allocation = list(series_dict_by_allocation.keys())[0]
    allocation_symbols = list(an_allocation._asdict().keys())
    df.index.names = allocation_symbols

    return df

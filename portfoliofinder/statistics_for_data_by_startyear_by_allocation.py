import pandas as pd
from .stats import get_statistics_by_allocation


from ._convert_to_dataframe_by_allocation import _convert_to_dataframe_by_allocation

class StatisticsForDataByStartYearByAllocation():

    def __init__(self, data, statistics):
        self._dict = get_statistics_by_allocation(data, statistics)
        self._df = _convert_to_dataframe_by_allocation(self._dict)
        self._data_type = next(iter(self._dict.values())).name
        self._allocation_symbols = list(next(iter(self._dict.keys()))._fields)

    def to_dataframe(self) -> pd.DataFrame:
        return self._df.copy()

    def get_allocations_which_max_each_statistic(self) -> pd.DataFrame:
        max_value_of_each_statistic = self._df[self._df.columns].idxmax()
        df_by_max_of_statistic = self._df.loc[max_value_of_each_statistic].reset_index().set_index(max_value_of_each_statistic.index)
        to_allocation_symbols_and_value = generate_to_allocation_symbols_and_value_method(self._allocation_symbols, self._data_type)
        allocation_and_value_by_max_of_statistic = df_by_max_of_statistic.apply(to_allocation_symbols_and_value, axis=1)
        allocation_and_value_by_max_of_statistic.columns.name = ''
        return allocation_and_value_by_max_of_statistic

def generate_to_allocation_symbols_and_value_method(allocation_symbols, data_type):
    def to_allocation_symbols_and_value(row):
        res = row[allocation_symbols]
        res[data_type] = row[row.name]
        return res
    return to_allocation_symbols_and_value
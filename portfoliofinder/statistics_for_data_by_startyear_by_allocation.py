import pandas as pd
from .stats import get_statistics_by_allocation
from collections import namedtuple

from ._convert_to_dataframe_by_allocation import _convert_to_dataframe_by_allocation

class StatisticsForDataByStartYearByAllocation():

    def __init__(self, data, statistics):
        self._dict = get_statistics_by_allocation(data, statistics)
        self._df = _convert_to_dataframe_by_allocation(self._dict)

        data_type = next(iter(self._dict.values())).name
        allocation_symbols = list(next(iter(self._dict.keys()))._fields)
        self._Allocation = namedtuple('Allocation', allocation_symbols)
        self._to_allocation_symbols_and_value = generate_to_allocation_symbols_and_value_method(allocation_symbols, data_type)

    def to_dataframe(self) -> pd.DataFrame:
        return self._df.copy()

    def get_allocations_which_max_each_statistic(self) -> pd.DataFrame:
        allocation_symbols_which_max_each_statistic = self._df[self._df.columns].idxmax()
        return self._append_value_for_each_statistic_allocation(allocation_symbols_which_max_each_statistic)

    def get_allocations_which_min_each_statistic(self) -> pd.DataFrame:
        allocation_symbols_which_min_each_statistic = self._df[self._df.columns].idxmin()
        return self._append_value_for_each_statistic_allocation(allocation_symbols_which_min_each_statistic)

    def _append_value_for_each_statistic_allocation(self, allocation_symbol_for_each_statistic) -> pd.DataFrame:
        all_statistics_for_each_allocation = self._df.loc[
            allocation_symbol_for_each_statistic].reset_index().set_index(
            allocation_symbol_for_each_statistic.index)
        allocation_and_value_for_each_statistic = all_statistics_for_each_allocation.apply(
            self._to_allocation_symbols_and_value, axis=1)
        allocation_and_value_for_each_statistic.columns.name = ''
        return allocation_and_value_for_each_statistic

    def get_allocation_which_min_statistic(self, statistic) -> pd.Series:
        allocation_which_min_statistic = self._df.idxmin().loc[statistic]
        res = self._df.loc[allocation_which_min_statistic]
        res.name = str(self._Allocation(*res.name))
        return res

    def get_allocation_which_max_statistic(self, statistic) -> pd.Series:
        allocation_which_max_statistic = self._df.idxmax().loc[statistic]
        res = self._df.loc[allocation_which_max_statistic]
        res.name = str(self._Allocation(*res.name))
        return res

def generate_to_allocation_symbols_and_value_method(allocation_symbols, data_type):
    def to_allocation_symbols_and_value(row):
        res = row[allocation_symbols]
        res[data_type] = row[row.name]
        return res
    return to_allocation_symbols_and_value

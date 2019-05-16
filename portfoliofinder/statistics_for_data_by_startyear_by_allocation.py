import pandas as pd
from .stats import get_statistics_by_allocation
from collections import namedtuple
from .self_pickling import SelfPickling
from .stats import percentile_for

import mplcursors
import matplotlib.pyplot as plt

from ._convert_to_dataframe_by_allocation import _convert_to_dataframe_by_allocation

from typing import Type, TypeVar

T = TypeVar('T', bound='StatisticsForDataByStartYearByAllocation')

class StatisticsForDataByStartYearByAllocation(SelfPickling):

    @classmethod
    def create_from_data_and_statistics(cls: Type[T], data, statistics) -> T:
        stats_by_allocation = get_statistics_by_allocation(data, statistics)
        stats_df = _convert_to_dataframe_by_allocation(stats_by_allocation)

        data_type = next(iter(stats_by_allocation.values())).name
        allocation_symbols = list(next(iter(stats_by_allocation.keys()))._fields)
        Allocation_namedtuple = namedtuple('Allocation', allocation_symbols)
        to_allocation_symbols_and_value_func = generate_to_allocation_symbols_and_value_method(allocation_symbols,
                                                                                               data_type)

        return StatisticsForDataByStartYearByAllocation(stats_df, Allocation_namedtuple,
                                                        to_allocation_symbols_and_value_func)

    def __init__(self, stats_df, allocation_namedtuple, to_allocation_symbols_and_value_func):
        self._df = stats_df
        self._Allocation = allocation_namedtuple
        self._to_allocation_symbols_and_value = to_allocation_symbols_and_value_func


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

    def graph(self, x, y):
        fig, ax = plt.subplots()
        self._df.plot.scatter(x,y, ax=ax)
        mplcursors.cursor(ax, hover=True).connect(
            "add", lambda sel: sel.annotation.set_text(self._Allocation(*self._df.iloc[sel.target.index].name)))
        plt.show()

    def filter(self: Type[T], dataframe_filter_function) -> T:
        new_df = self._df[dataframe_filter_function(self._df)]
        return StatisticsForDataByStartYearByAllocation(new_df,
                                                        self._Allocation,
                                                        self._to_allocation_symbols_and_value)

    def filter_by_min_of(self: Type[T], statistic) -> T:
        new_df = self._df[self._df[statistic] == min(self._df[statistic])]
        return StatisticsForDataByStartYearByAllocation(new_df,
                                                        self._Allocation,
                                                        self._to_allocation_symbols_and_value)

    def filter_by_max_of(self: Type[T], statistic) -> T:
        new_df = self._df[self._df[statistic] == max(self._df[statistic])]
        return StatisticsForDataByStartYearByAllocation(new_df,
                                                        self._Allocation,
                                                        self._to_allocation_symbols_and_value)

    def filter_by_gte_percentile_of(self: Type[T], percentile, statistic) -> T:
        new_df = self._df[self._df[statistic] >= percentile_for(percentile)(self._df[statistic])]
        return StatisticsForDataByStartYearByAllocation(new_df,
                                                        self._Allocation,
                                                        self._to_allocation_symbols_and_value)

    def filter_by_lte_percentile_of(self: Type[T], percentile, statistic) -> T:
        new_df = self._df[self._df[statistic] <= percentile_for(percentile)(self._df[statistic])]
        return StatisticsForDataByStartYearByAllocation(new_df,
                                                        self._Allocation,
                                                        self._to_allocation_symbols_and_value)

def generate_to_allocation_symbols_and_value_method(allocation_symbols, data_type):
    def to_allocation_symbols_and_value(row):
        res = row[allocation_symbols]
        res[data_type] = row[row.name]
        return res
    return to_allocation_symbols_and_value

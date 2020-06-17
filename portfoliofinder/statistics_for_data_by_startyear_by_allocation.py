from __future__ import annotations

from collections import namedtuple
from typing import Dict

import matplotlib.pyplot as plt
import mplcursors
import pandas as pd

from ._convert_to_dataframe_by_allocation import _convert_to_dataframe_by_allocation
from .self_pickling import SelfPickling
from .stats import _get_statistics_by_allocation, percentile_for, StatListType


class StatisticsForDataByStartYearByAllocation(SelfPickling):
    """Statistical results for backtested portfolio data, by allocation mix."""

    @classmethod
    def create_from_data_and_statistics(cls,
                                        data_by_allocation: Dict[tuple, pd.Series],
                                        statistics: StatListType)\
            -> StatisticsForDataByStartYearByAllocation:
        """Create statistical results for backtested portfolio data, by allocation mix.

        :param data_by_allocation: backtested portfolio data by allocation mix
        :param statistics: array of statistic functions for pandas Series
        :return: statistical results for the data
        """
        stats_by_allocation = _get_statistics_by_allocation(data_by_allocation, statistics)
        stats_df = _convert_to_dataframe_by_allocation(stats_by_allocation)

        data_type = next(iter(stats_by_allocation.values())).name
        allocation_symbols = list(
            next(iter(stats_by_allocation.keys()))._fields)
        allocation_namedtuple = namedtuple('Allocation', allocation_symbols)
        to_allocation_symbols_and_value_func = \
            _generate_to_allocation_symbols_and_value_method(allocation_symbols,
                                                             data_type)

        return StatisticsForDataByStartYearByAllocation(stats_df, allocation_namedtuple,
                                                        to_allocation_symbols_and_value_func)

    def __init__(self, stats_df, allocation_namedtuple, to_allocation_symbols_and_value_func):
        self._df = stats_df
        self._allocation_namedtuple = allocation_namedtuple
        self._to_allocation_symbols_and_value = to_allocation_symbols_and_value_func

    def as_dataframe(self) -> pd.DataFrame:
        """Gets as pandas DataFrame."""
        return self._df.copy()

    def get_allocations_which_max_each_statistic(self) -> pd.DataFrame:
        """Gets allocations which maximize each statistic."""
        allocations_which_max_each_statistic = self._df[self._df.columns].idxmax()
        return self._append_value_for_each_statistic_allocation(
            allocations_which_max_each_statistic)

    def get_allocations_which_min_each_statistic(self) -> pd.DataFrame:
        """Gets allocation which minimize each statistic."""
        allocations_which_min_each_statistic = self._df[self._df.columns].idxmin()
        return self._append_value_for_each_statistic_allocation(
            allocations_which_min_each_statistic)

    def _append_value_for_each_statistic_allocation(self, allocations_for_each_statistic)\
            -> pd.DataFrame:
        all_statistics_for_each_allocation = self._df.loc[allocations_for_each_statistic]\
            .reset_index()\
            .set_index(allocations_for_each_statistic.index)
        allocation_and_value_for_each_statistic = all_statistics_for_each_allocation\
            .apply(self._to_allocation_symbols_and_value, axis=1)
        allocation_and_value_for_each_statistic.columns.name = ''
        return allocation_and_value_for_each_statistic

    def get_allocation_which_min_statistic(self, statistic) -> pd.Series:
        """Gets allocation which minimizes the specified statistic.

        :param statistic: statistic label (e.g., 'mean')
        :return: allocation which minimizes the statistic
        """
        allocation_which_min_statistic = self._df.idxmin().loc[statistic]
        res = self._df.loc[allocation_which_min_statistic]
        res.name = str(self._allocation_namedtuple(*res.name))
        return res

    def get_allocation_which_max_statistic(self, statistic) -> pd.Series:
        """Gets allocation which maximizes the specified statistic.

        :param statistic: statistic label (e.g., 'mean')
        :return: allocation which maximizes the statistic
        """
        allocation_which_max_statistic = self._df.idxmax().loc[statistic]
        res = self._df.loc[allocation_which_max_statistic]
        res.name = str(self._allocation_namedtuple(*res.name))
        return res

    def graph(self, x_axis, y_axis):
        """Creates a scattergraph to visualize the data.

        :param x_axis: statistic label for the x axis (e.g., 'mean')
        :param y_axis: statistic label for the y axis (e.g., 'std')
        """
        _, axis_object = plt.subplots()
        self._df.plot.scatter(x_axis, y_axis, axis_object=axis_object)
        mplcursors.cursor(axis_object, hover=True).connect(
            "add",
            lambda sel: sel.annotation.set_text(
                self._allocation_namedtuple(*self._df.iloc[sel.target.index].name))
        )
        plt.show()

    def filter(self, dataframe_filter_function) -> StatisticsForDataByStartYearByAllocation:
        """Filters these statistical results with the specified function.

        :param dataframe_filter_function: function to filter results with
        :return: a new set of statistical results
        """
        new_df = self._df[dataframe_filter_function(self._df)]
        return StatisticsForDataByStartYearByAllocation(new_df,
                                                        self._allocation_namedtuple,
                                                        self._to_allocation_symbols_and_value)

    def filter_by_min_of(self, statistic_label) -> StatisticsForDataByStartYearByAllocation:
        """Filters these statistical results to only include data which minimizes
        the specified statistic.

        :param statistic_label: label of the statistic
        :return: a new set of statistical results
        """
        new_df = self._df[self._df[statistic_label] == min(self._df[statistic_label])]
        return StatisticsForDataByStartYearByAllocation(new_df,
                                                        self._allocation_namedtuple,
                                                        self._to_allocation_symbols_and_value)

    def filter_by_max_of(self, statistic) -> StatisticsForDataByStartYearByAllocation:
        """Filters these statistical results to only include data which maximizes
        the specified statistic.

        :param statistic_label: label of the statistic
        :return: a new set of statistical results
        """
        new_df = self._df[self._df[statistic] == max(self._df[statistic])]
        return StatisticsForDataByStartYearByAllocation(new_df,
                                                        self._allocation_namedtuple,
                                                        self._to_allocation_symbols_and_value)

    def filter_by_gte_percentile_of(self, percentile: int, statistic) \
            -> StatisticsForDataByStartYearByAllocation:
        """Filters these statistical results to only include data which are
        greater than or equal to the specified percential for the specified
        statistic.

        :param percentile: percentile as int from 0 to 100
        :param statistic_label: label of the statistic
        :return: a new set of statistical results
        """
        new_df = self._df[self._df[statistic] >=
                          percentile_for(percentile)(self._df[statistic])]
        return StatisticsForDataByStartYearByAllocation(new_df,
                                                        self._allocation_namedtuple,
                                                        self._to_allocation_symbols_and_value)

    def filter_by_lte_percentile_of(self, percentile, statistic) \
            -> StatisticsForDataByStartYearByAllocation:
        """Filters these statistical results to only include data which are
        less than or equal to the specified percential for the specified
        statistic.

        :param percentile: percentile as int from 0 to 100
        :param statistic_label: label of the statistic
        :return: a new set of statistical results
        """
        new_df = self._df[self._df[statistic] <=
                          percentile_for(percentile)(self._df[statistic])]
        return StatisticsForDataByStartYearByAllocation(new_df,
                                                        self._allocation_namedtuple,
                                                        self._to_allocation_symbols_and_value)


def _generate_to_allocation_symbols_and_value_method(allocation_symbols, data_type):
    def to_allocation_symbols_and_value(row):
        res = row[allocation_symbols]
        res[data_type] = row[row.name]
        return res
    return to_allocation_symbols_and_value

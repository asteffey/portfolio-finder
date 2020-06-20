from __future__ import annotations

from collections import namedtuple
from functools import wraps
from typing import Dict

import matplotlib.pyplot as plt
import mplcursors
import pandas as pd
import progressbar

from ..stats.functions import percentile_for, StatList
from ..util.self_pickling import SelfPickling
from ..util.to_dataframe import to_dataframe


class BacktestedStatistics(SelfPickling):
    """Statistical results for backtested portfolio data."""

    def __init__(self, data_by_allocation: Dict[tuple, pd.Series], statistics: StatList):
        """Create statistical results for backtested portfolio data.

        :param data_by_allocation: backtested portfolio data
        :param statistics: array of statistic functions for pandas Series
        :return: statistical results for the data
        """
        stats_by_allocation = _get_statistics_by_allocation(data_by_allocation, statistics)
        self._df = to_dataframe(stats_by_allocation)

        data_type = next(iter(stats_by_allocation.values())).name
        allocation_symbols = list(
            next(iter(stats_by_allocation.keys()))._fields)
        self._allocation_namedtuple = namedtuple('Allocation', allocation_symbols)
        self._to_allocation_symbols_and_value = \
            _generate_to_allocation_symbols_and_value_method(allocation_symbols,
                                                             data_type)

    @classmethod
    def _from_stats(cls, stats_df, allocation_namedtuple, to_allocation_symbols_and_value_func)\
            -> BacktestedStatistics:
        new_stats = cls.__new__(cls)
        super().__init__(new_stats)
        # pylint: disable=protected-access
        new_stats._df = stats_df
        new_stats._allocation_namedtuple = allocation_namedtuple
        new_stats._to_allocation_symbols_and_value = to_allocation_symbols_and_value_func
        # pylint: enable=protected-access
        return new_stats

    def __repr__(self):
        return self._df.__repr__()

    def __str__(self):
        return self._df.__str__()

    def as_dataframe(self) -> pd.DataFrame:
        """Gets this as a pandas DataFrame.

        Note that changes to the returned DataFrame will modify this object.
        """
        return self._df

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
        self._df.plot.scatter(x_axis, y_axis)
        mplcursors.cursor(hover=True).connect(
            "add",
            lambda sel: sel.annotation.set_text(
                self._allocation_namedtuple(*self._df.iloc[sel.target.index].name))
        )
        plt.show()

    def filter(self, dataframe_filter_function) -> BacktestedStatistics:
        """Filters these statistical results with the specified function.

        :param dataframe_filter_function: function to filter results with
        :return: a new set of statistical results
        """
        new_df = self._df[dataframe_filter_function(self._df)]
        return BacktestedStatistics._from_stats(new_df,
                                                self._allocation_namedtuple,
                                                self._to_allocation_symbols_and_value)

    def filter_by_min_of(self, statistic_label) -> BacktestedStatistics:
        """Filters these statistical results to only include data which minimizes
        the specified statistic.

        :param statistic_label: label of the statistic
        :return: a new set of statistical results
        """
        new_df = self._df[self._df[statistic_label] == min(self._df[statistic_label])]
        return BacktestedStatistics._from_stats(new_df,
                                                self._allocation_namedtuple,
                                                self._to_allocation_symbols_and_value)

    def filter_by_max_of(self, statistic_label) -> BacktestedStatistics:
        """Filters these statistical results to only include data which maximizes
        the specified statistic.

        :param statistic_label: label of the statistic
        :return: a new set of statistical results
        """
        new_df = self._df[self._df[statistic_label] == max(self._df[statistic_label])]
        return BacktestedStatistics._from_stats(new_df,
                                                self._allocation_namedtuple,
                                                self._to_allocation_symbols_and_value)

    def filter_by_gte_percentile_of(self, percentile: int, statistic_label) \
            -> BacktestedStatistics:
        """Filters these statistical results to only include data which are
        greater than or equal to the specified percential for the specified
        statistic.

        :param percentile: percentile as int from 0 to 100
        :param statistic_label: label of the statistic
        :return: a new set of statistical results
        """
        new_df = self._df[self._df[statistic_label] >=
                          percentile_for(percentile)(self._df[statistic_label])]
        return BacktestedStatistics._from_stats(new_df,
                                                self._allocation_namedtuple,
                                                self._to_allocation_symbols_and_value)

    def filter_by_lte_percentile_of(self, percentile, statistic_label) \
            -> BacktestedStatistics:
        """Filters these statistical results to only include data which are
        less than or equal to the specified percential for the specified
        statistic.

        :param percentile: percentile as int from 0 to 100
        :param statistic_label: label of the statistic
        :return: a new set of statistical results
        """
        new_df = self._df[self._df[statistic_label] <=
                          percentile_for(percentile)(self._df[statistic_label])]
        return BacktestedStatistics._from_stats(new_df,
                                                self._allocation_namedtuple,
                                                self._to_allocation_symbols_and_value)

def _generate_to_allocation_symbols_and_value_method(allocation_symbols, data_type):
    def to_allocation_symbols_and_value(row):
        res = row[allocation_symbols]
        res[data_type] = row[row.name]
        return res
    return to_allocation_symbols_and_value


def _get_statistics_by_allocation(portfolio_values_by_allocations, statistics: StatList):
    statistics_by_allocation = {}
    for allocation in progressbar.progressbar(portfolio_values_by_allocations.keys()):
        portfolio_timeframe_by_startyear = _get_statistics(
            portfolio_values_by_allocations[allocation], statistics)
        statistics_by_allocation[allocation] = portfolio_timeframe_by_startyear
    return statistics_by_allocation


def _get_statistics(portfolio_values: pd.Series, statistics: StatList) -> pd.Series:
    statistics = list(map(lambda stat: _typecheck_series(
        stat) if callable(stat) else stat, statistics))
    statistics = portfolio_values.agg(statistics)
    statistics.index.name = "Statistic"
    return statistics


def _typecheck_series(func):
    @wraps(func)
    def wrapper(series):
        if isinstance(series, pd.Series):
            return func(series)
        raise TypeError
    return wrapper

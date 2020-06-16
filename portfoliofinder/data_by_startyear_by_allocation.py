import pandas as pd
import progressbar

from ._convert_to_dataframe_by_allocation import _convert_to_dataframe_by_allocation
from .stats import DEFAULT_STATS
from .statistics_for_data_by_startyear_by_allocation import StatisticsForDataByStartYearByAllocation
from .self_pickling import SelfPickling


class _DataByStartYearByAllocation(SelfPickling):
    def __init__(self, data_func, data_by_allocation: dict, *argv):
        self._data = _get_data_by_startyear_by_allocation(
            data_func, data_by_allocation, *argv)

    def get_series(self, allocation) -> pd.Series:
        """Gets the portfolio returns as a pandas Series for a given
        allocation.

        :param allocation: allocation to get returns for
        """
        return self._data[allocation]

    def as_dataframe(self) -> pd.DataFrame:
        """Gets as pandas DataFrame."""
        return _convert_to_dataframe_by_allocation(self._data)

    def get_statistics(self, statistics=DEFAULT_STATS) -> StatisticsForDataByStartYearByAllocation:
        """Gets statistical results for backtested portfolio data, by allocation mix.

        :param statistics: array of statistic functions for pandas Series
        :return: A pandas Series containing values for each statistic
        """

        return StatisticsForDataByStartYearByAllocation\
            .create_from_data_and_statistics(self._data, statistics)


def _get_data_by_startyear_by_allocation(data_func, data_by_allocations, *argv):
    data_by_startyear_by_allocation = {}
    for allocation in progressbar.progressbar(data_by_allocations.keys()):
        data_by_startyear = data_func(data_by_allocations[allocation], *argv)
        data_by_startyear_by_allocation[allocation] = data_by_startyear
    return data_by_startyear_by_allocation

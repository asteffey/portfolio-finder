from typing import Dict

import pandas as pd
import progressbar

from .backtested_statistics import BacktestedStatistics
from ..stats import DEFAULT_STATS, StatList
from ..util.self_pickling import SelfPickling
from ..util.to_dataframe import to_dataframe


class _BacktestedData(SelfPickling):
    """Base class for backtested data."""
    def __init__(self, data_func, data_by_allocation: dict, *argv):
        self._data = _get_data_by_startyear_by_allocation(
            data_func, data_by_allocation, *argv)

    def __repr__(self):
        return self.to_dataframe().__repr__()

    def __str__(self):
        return self.to_dataframe().__str__()

    def get_series(self, allocation) -> pd.Series:
        """Gets the portfolio returns as a pandas Series for a given
        allocation.

        :param allocation: allocation to get returns for
        """
        return self._data[allocation]

    def to_dataframe(self) -> pd.DataFrame:
        """Converts this to a pandas DataFrame."""
        return to_dataframe(self._data)

    def get_statistics(self, statistics: StatList = DEFAULT_STATS)\
            -> BacktestedStatistics:
        """Gets statistical results for backtested portfolio data, by allocation mix.

        :param statistics: array of statistic functions for pandas Series
        :return: A pandas Series containing values for each statistic
        """

        return BacktestedStatistics(self._data, statistics)


def _get_data_by_startyear_by_allocation(data_func, data_by_allocations, *argv)\
        -> Dict[tuple, pd.Series]:
    data_by_startyear_by_allocation = {}
    for allocation in progressbar.progressbar(data_by_allocations.keys()):
        data_by_startyear = data_func(data_by_allocations[allocation], *argv)
        data_by_startyear_by_allocation[allocation] = data_by_startyear
    return data_by_startyear_by_allocation

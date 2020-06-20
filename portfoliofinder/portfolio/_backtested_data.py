from typing import Dict

import pandas as pd

from .backtested_statistics import BacktestedStatistics
from ..stats import DEFAULT_STATS, StatList
from ..util.progressbar import progressbar
from ..util.self_pickling import SelfPickling
from ..util.to_dataframe import to_dataframe


class _BacktestedData(SelfPickling):
    """Base class for backtested data."""
    def __init__(self, data_func, data_by_allocation: dict, use_progressbar: bool, *argv):
        self._data = {}
        for allocation in progressbar(data_by_allocation.keys(), use_progressbar):
            data_by_startyear = data_func(data_by_allocation[allocation], *argv)
            self._data[allocation] = data_by_startyear

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

    def get_statistics(self, statistics: StatList = DEFAULT_STATS, use_progressbar: bool = False)\
            -> BacktestedStatistics:
        """Gets statistical results for backtested portfolio data, by allocation mix.

        :param statistics: array of statistic functions for pandas Series
        :param use_progressbar: whether are not to display a progressbar to provide the status
                                of large calculations
        :return: A pandas Series containing values for each statistic
        """

        return BacktestedStatistics(self._data, statistics, use_progressbar)


def _get_data_by_startyear_by_allocation(data_func, data_by_allocations, use_progressbar, *argv)\
        -> Dict[tuple, pd.Series]:
    data_by_startyear_by_allocation = {}
    for allocation in progressbar(data_by_allocations.keys(), use_progressbar):
        data_by_startyear = data_func(data_by_allocations[allocation], *argv)
        data_by_startyear_by_allocation[allocation] = data_by_startyear
    return data_by_startyear_by_allocation

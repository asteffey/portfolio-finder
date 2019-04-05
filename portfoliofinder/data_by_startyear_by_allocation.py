import pandas as pd
from functools import reduce

from .contributions import Contributions
from ._convert_to_dataframe_by_allocation import _convert_to_dataframe_by_allocation
from .stats import DEFAULT_STATS, get_statistics_by_allocation

class DataByStartYearByAllocation():

    def __init__(self, data_func, data_by_allocation: dict, *argv):
        self._data = _get_data_by_startyear_by_allocation(data_func, data_by_allocation, *argv)

    def to_series(self, allocation) -> pd.Series:
        return self._data[allocation]

    def to_dataframe(self) -> pd.DataFrame:
        return _convert_to_dataframe_by_allocation(self._data)

    def get_statistics(self, statistics = DEFAULT_STATS) -> pd.Series:
        statistics = get_statistics_by_allocation(self._data, statistics)
        return _convert_to_dataframe_by_allocation(statistics)


def _get_data_by_startyear_by_allocation(data_func, data_by_allocations, *argv):
    data_by_startyear_by_allocation = {}
    for allocation in data_by_allocations.keys():
        data_by_startyear = data_func(data_by_allocations[allocation], *argv)
        data_by_startyear_by_allocation[allocation] = data_by_startyear
    return data_by_startyear_by_allocation
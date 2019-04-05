import pandas as pd

from ._convert_to_dataframe_by_allocation import _convert_to_dataframe_by_allocation
from .stats import DEFAULT_STATS
from .statistics_for_data_by_startyear_by_allocation import StatisticsForDataByStartYearByAllocation


class DataByStartYearByAllocation():

    def __init__(self, data_func, data_by_allocation: dict, *argv):
        self._data = _get_data_by_startyear_by_allocation(data_func, data_by_allocation, *argv)

    def to_series(self, allocation) -> pd.Series:
        return self._data[allocation]

    def to_dataframe(self) -> pd.DataFrame:
        return _convert_to_dataframe_by_allocation(self._data)

    def get_statistics(self, statistics = DEFAULT_STATS) -> StatisticsForDataByStartYearByAllocation:
        return StatisticsForDataByStartYearByAllocation(self._data, statistics)


def _get_data_by_startyear_by_allocation(data_func, data_by_allocations, *argv):
    data_by_startyear_by_allocation = {}
    for allocation in data_by_allocations.keys():
        data_by_startyear = data_func(data_by_allocations[allocation], *argv)
        data_by_startyear_by_allocation[allocation] = data_by_startyear
    return data_by_startyear_by_allocation
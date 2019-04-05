import pandas as pd
from .stats import get_statistics_by_allocation


from ._convert_to_dataframe_by_allocation import _convert_to_dataframe_by_allocation

class StatisticsForDataByStartYearByAllocation():

    def __init__(self, data, statistics):
        self._statistics = get_statistics_by_allocation(data, statistics)

    def to_dataframe(self) -> pd.DataFrame:
        return _convert_to_dataframe_by_allocation(self._statistics)
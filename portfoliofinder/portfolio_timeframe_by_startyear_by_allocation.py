import pandas as pd
from functools import reduce

from .contributions import Contributions
from .portfolio_timeframe_by_startyear import _get_portfolio_timeframe_by_startyear
from ._convert_to_dataframe_by_allocation import _convert_to_dataframe_by_allocation
from .stats import DEFAULT_STATS, get_statistics_by_allocation

class PortfolioTimeframesByStartYearByAllocation():

    def __init__(self, portfolio_returns_by_allocation: dict, target_value, contributions: Contributions):
        self._portfolio_timeframe_by_startyear_by_allocation = _get_portfolio_timeframe_by_startyear_by_allocation(
            portfolio_returns_by_allocation, target_value, contributions)

    def to_series(self, allocation) -> pd.Series:
        return self._portfolio_timeframe_by_startyear_by_allocation[allocation]

    def to_dataframe(self) -> pd.DataFrame:
        return _convert_to_dataframe_by_allocation(self._portfolio_timeframe_by_startyear_by_allocation)

    def get_statistics(self, statistics = DEFAULT_STATS) -> pd.Series:
        return get_statistics_by_allocation(self._portfolio_timeframe_by_startyear_by_allocation, statistics)


def _get_portfolio_timeframe_by_startyear_by_allocation(portfolio_returns_by_allocations, target_value, contributions):
    portfolio_timeframe_by_startyear_by_allocation = {}
    for allocation in portfolio_returns_by_allocations.keys():
        portfolio_timeframe_by_startyear = _get_portfolio_timeframe_by_startyear(portfolio_returns_by_allocations[allocation], target_value, contributions)
        portfolio_timeframe_by_startyear_by_allocation[allocation] = portfolio_timeframe_by_startyear
    return portfolio_timeframe_by_startyear_by_allocation
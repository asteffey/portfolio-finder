import pandas as pd
from functools import reduce

from .contributions import Contributions
from .portfolio_value_by_startyear import _get_portfolio_value_by_startyear

class PortfolioValuesByStartYearByAllocation():

    def __init__(self, portfolio_returns_by_allocation: dict, timeframe, contributions: Contributions):
        self._portfolio_value_by_startyear_by_allocation = _get_portfolio_value_by_startyear_by_allocation(
            portfolio_returns_by_allocation, timeframe, contributions)

    def to_series(self, allocation) -> pd.Series:
        return self._portfolio_value_by_startyear_by_allocation[allocation]


def _get_portfolio_value_by_startyear_by_allocation(portfolio_returns_by_allocations, timeframe, contributions):
    portfolio_value_by_startyear_by_allocation = {}
    for allocation in portfolio_returns_by_allocations.keys():
        portfolio_value_by_startyear = _get_portfolio_value_by_startyear(portfolio_returns_by_allocations[allocation], timeframe, contributions)
        portfolio_value_by_startyear_by_allocation[allocation] = portfolio_value_by_startyear
    return portfolio_value_by_startyear_by_allocation
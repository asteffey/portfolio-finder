import pandas as pd
import progressbar

from ._convert_to_dataframe_by_allocation import _convert_to_dataframe_by_allocation
from .contributions import Contributions, DEFAULT_CONTRIBUTION
from .portfolio_allocations import PortfolioAllocations
from .portfolio_returns import _get_portfolio_returns
from .portfolio_timeframe_by_startyear_by_allocation \
    import PortfolioTimeframesByStartYearByAllocation
from .portfolio_value_by_startyear_by_allocation \
    import PortfolioValuesByStartYearByAllocation
from .self_pickling import SelfPickling


class PortfolioReturnsByAllocation(SelfPickling):
    """Portfolio returns by year for a set of allocation mixes."""

    def __init__(self, returns_by_symbol: pd.DataFrame,
                 allocations: PortfolioAllocations):
        returns_by_symbol = returns_by_symbol[allocations.as_dataframe().columns]

        self.portfolio_returns_by_allocation = {}
        for allocation in progressbar.progressbar(allocations.to_tuples()):
            portfolio_returns = _get_portfolio_returns(
                allocation, returns_by_symbol)
            self.portfolio_returns_by_allocation[allocation] = portfolio_returns

    def get_series(self, allocation) -> pd.Series:
        """Gets the portfolio returns as a pandas Series for a given
        allocation.

        :param allocation: allocation to get returns for
        """
        return self.portfolio_returns_by_allocation[allocation]

    def as_dataframe(self) -> pd.DataFrame:
        """Gets as pandas DataFrame."""
        return _convert_to_dataframe_by_allocation(
            self.portfolio_returns_by_allocation)

    def to_portfolio_value_by_startyear_by_allocation(
            self, timeframe, contributions: Contributions = DEFAULT_CONTRIBUTION):
        """Provides the portfolio value after a length of time given
        the contributions and by each start year and allocation mix.

        :param timeframe: portfolio timeframe in years
        :param contributions: contributions to portfolio
        :return: portfolio portfolio value after timeframe by start year and
                 allocation mix
        """
        return PortfolioValuesByStartYearByAllocation(
            self.portfolio_returns_by_allocation, timeframe, contributions)

    def to_portfolio_timeframe_by_startyear_by_allocation(
            self, target_value, contributions: Contributions = DEFAULT_CONTRIBUTION):
        """Provides the length of time to achieve the target value given
        the contributions and by each start year and allocation mix.

        :param target_value: portfolio value to target
        :param contributions: contributions to portfolio
        :return: portfolio timeframes to achieve target value by start year and
                 allocation mix
        """
        return PortfolioTimeframesByStartYearByAllocation(
            self.portfolio_returns_by_allocation, target_value, contributions)

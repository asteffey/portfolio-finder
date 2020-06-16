import pandas as pd

from .portfolio_value_by_startyear import PortfolioValuesByStartYear
from .portfolio_timeframe_by_startyear import PortfolioTimeframesByStartYear
from .contributions import Contributions, DEFAULT_CONTRIBUTION
from .self_pickling import SelfPickling


class PortfolioReturns(SelfPickling):
    """Portfolio returns, by year, for a specific allocation mix."""

    def __init__(self, returns_by_symbol: pd.DataFrame, allocation):
        """Create portfolio returns, by year, for a specific allocation mix.

        :param returns_by_symbol:
        :param allocation: namedtuple with fund symbols as names
        """
        allocation_symbols = _get_allocation_symbols(allocation)
        self._returns = _get_portfolio_returns(allocation, returns_by_symbol[allocation_symbols])

    def as_series(self) -> pd.Series:
        """Gets as pandas Series."""
        return self._returns

    def to_portfolio_value_by_startyear(self, timeframe,
                                        contributions: Contributions = DEFAULT_CONTRIBUTION):
        """Creates portfolio values by start year for a specific timeframe and
        contributions schedule, based on these portfolio returns.

        :param timeframe: fixed timeframe for portfolio
        :param contributions: contributions schedule
        :return: portfolio values by start year, for a specific allocation mix,
                 timeframe, and contributions schedule
        """
        return PortfolioValuesByStartYear(self._returns, timeframe, contributions)

    def to_portfolio_timeframe_by_startyear(self, target_value,
                                            contributions: Contributions = DEFAULT_CONTRIBUTION):
        """Creates set of timeframes for portfolio to achieve a target value, by start year,
        for a specific contributions schedule, based on these portfolio returns.

        :param target_value: target value the portfolio is looking to achieve
        :param contributions: contributions schedule
        :return: timeframes for portfolio to achieve a target value, by start year,
                 for a specific allocation mix and contributions schedule
        """
        return PortfolioTimeframesByStartYear(self._returns, target_value, contributions)


def _get_portfolio_returns(portfolio_allocation, returns_by_symbol: pd.DataFrame) -> pd.Series:
    portfolio_returns = []
    for row in returns_by_symbol.iterrows():
        return_by_symbol = row[1]
        return_for_year = sum(return_by_symbol * portfolio_allocation)
        portfolio_returns.append(return_for_year)
    years = returns_by_symbol.axes[0]
    return pd.Series(portfolio_returns, index=years, name="Portfolio Return")

def _get_allocation_symbols(allocation):
    return list(allocation._fields)

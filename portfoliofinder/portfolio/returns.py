import pandas as pd

from ..util.progressbar import progressbar
from ..util.self_pickling import SelfPickling
from ..util.to_dataframe import to_dataframe
from .backtested_timeframes import BacktestedTimeframes
from .backtested_values import BacktestedValues
from typing import Dict
from ..contributions import *


class Returns(SelfPickling):
    """Portfolio returns by year for a set of allocation mixes."""

    def __init__(self, returns_by_symbol: pd.DataFrame,
                 allocations: pd.DataFrame,
                 use_progressbar: bool = False):
        returns_by_symbol = returns_by_symbol[allocations.columns]

        self._portfolio_returns_by_allocation = {}
        allocations_tuples = list(allocations.itertuples(name="Allocation", index=False))
        for allocation in progressbar(allocations_tuples, use_progressbar):
            portfolio_returns = _get_portfolio_returns(
                allocation, returns_by_symbol)
            self._portfolio_returns_by_allocation[allocation] = portfolio_returns

    def __repr__(self):
        return self.to_dataframe().__repr__()

    def __str__(self):
        return self.to_dataframe().__str__()

    def to_dataframe(self) -> pd.DataFrame:
        """Converts this to a pandas DataFrame."""
        return to_dataframe(
            self._portfolio_returns_by_allocation)

    def get_series(self, allocation) -> pd.Series:
        """Gets the portfolio returns as a pandas Series for a given
        allocation.

        :param allocation: allocation to get returns for
        """
        return self._portfolio_returns_by_allocation[allocation]

    def with_contributions(self, contributions: Contributions = DEFAULT_CONTRIBUTION):
        """Add contributions to these portfolio returns.

        :param contributions: contribution schedule
        :return: portfolio returns with contributions
        """
        return ReturnsWithContributions(self._portfolio_returns_by_allocation,
                                        contributions)

    def with_initial_contribution(self, starting_value: float):
        """Add an initial contribution to these portfolio returns.

        :param starting_value: initial contribution at inception of portfolio
        """
        return self.with_contributions(InitialContribution(starting_value))

    def with_regular_contributions(self, starting_value: float, annual_contribution: float):
        """Add regular contributions to these portfolio returns.

        :param starting_value: initial contribution made at portfolio inception
        :param annual_contribution: subsequent annual contributions
        """
        return self.with_contributions(RegularContributions(starting_value, annual_contribution))

    def with_scheduled_contributions(self, scheduled_contributions: Dict[int, float]):
        """Add scheduled contributions to these portfolio returns.

        :param scheduled_contributions: contributions by year relative to inception of portfolio
        """
        return self.with_contributions(ScheduledContributions(scheduled_contributions))

class ReturnsWithContributions(Returns):
    """Portfolio returns by year for a set of allocation mixes,
    along with a contributions schedule.
    """

    def __init__(self, portfolio_returns_by_allocation, contributions: Contributions):
        self._portfolio_returns_by_allocation = portfolio_returns_by_allocation
        self._contributions = contributions

    def get_backtested_values(self, timeframe: int, use_progressbar: bool = False) -> BacktestedValues:
        """Calculates final portfolio values, by start year, after a fixed timeframe.

        :param timeframe: timeframe in years
        :param use_progressbar: whether are not to display a progressbar to provide the status
                                of large calculations
        :return: portfolio values, by start year, after a fixed timeframe
        """
        return BacktestedValues(
            self._portfolio_returns_by_allocation, timeframe, use_progressbar, self._contributions)

    def get_backtested_timeframes(self, target_value: float, use_progressbar: bool = False) -> BacktestedTimeframes:
        """Calculates portfolio timeframes, by start year, required to
        achieve a target value.

        :param target_value: portfolio value to target
        :param use_progressbar: whether are not to display a progressbar to provide the status
                                of large calculations
        :return: portfolio values, by start year, after a fixed timeframe
        """
        return BacktestedTimeframes(
            self._portfolio_returns_by_allocation, target_value, use_progressbar, self._contributions)


def _get_portfolio_returns(portfolio_allocation, returns_by_symbol: pd.DataFrame) -> pd.Series:
    portfolio_returns = []
    for row in returns_by_symbol.iterrows():
        return_by_symbol = row[1]
        return_for_year = sum(return_by_symbol * portfolio_allocation)
        portfolio_returns.append(return_for_year)
    years = returns_by_symbol.axes[0]
    return pd.Series(portfolio_returns, index=years, name="Portfolio Return")

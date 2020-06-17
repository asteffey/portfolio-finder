from __future__ import annotations

from typing import List

import pandas as pd

from .portfolio_allocations import PortfolioAllocations
from .portfolio_returns import PortfolioReturns
from .portfolio_returns_by_allocation import PortfolioReturnsByAllocation


class SymbolReturns:
    """Returns for each symbol by year."""
    def __init__(self, returns_by_symbol: pd.DataFrame):
        """Create returns for each symbol by year.

        :param returns_by_symbol: A pandas DataFrame with columns by symbol and rows by year
        """
        self.returns_by_symbol = returns_by_symbol

    @classmethod
    def from_csv(cls, csv_file: str) -> SymbolReturns:
        """Read returns from a CSV file.

        :param csv_file: path to CSV file
        :return: returns for each symbol by year
        """
        return cls(pd.read_csv(csv_file, index_col=0))

    def as_dataframe(self) -> pd.DataFrame:
        """Gets as pandas DataFrame."""
        return self.returns_by_symbol

    def filter_by_symbols(self, symbols: List[str]) -> SymbolReturns:
        """Creates new returns filtered by specified symbols.

        :param symbols: symbols to filter by
        :return: returns for each specified symbol by year
        """
        return SymbolReturns(self.returns_by_symbol[symbols])

    def adjust_for_inflation(self, inflation_rates: pd.Series) -> SymbolReturns:
        """Creates new returns adjusted for inflation.

        :param inflation_rates: pandas Series of inflation rates by year
        :return: returns for each specified symbol by year
        """
        def _adjust_for_inflation(returns_for_year):
            year = returns_for_year.name
            inflation_rate = inflation_rates[year]
            return (returns_for_year + 1) / (inflation_rate + 1) - 1
        return SymbolReturns(self.returns_by_symbol.apply(_adjust_for_inflation, axis=1))

    def to_portfolio_returns(self, allocation) -> PortfolioReturns:
        """Creates portfolio returns, by year, for a specific allocation mix,
        based on these fund returns.

        :param allocation: the allocation mix
        :return: portfolio returns, by year, for a specific allocation mix
        """
        return PortfolioReturns(self.returns_by_symbol, allocation)

    def to_portfolio_returns_by_allocation(self, allocations: PortfolioAllocations) \
            -> PortfolioReturnsByAllocation:
        """Creates portfolio returns by year for a set of allocation mixes,
        based on these fund returns.

        :param allocations: a range of portfolio allocations
        :return: portfolio returns by year for a set of allocation mixes
        """
        return PortfolioReturnsByAllocation(self.returns_by_symbol, allocations)

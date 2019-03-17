import pandas as pd
from .portfolio_returns import PortfolioReturns
from .portfolio_returns_group import PortfolioReturnsByAllocation

class ReturnsBySymbol():
    def __init__(self, returns_by_symbol: pd.DataFrame):
        self.returns_by_symbol = returns_by_symbol
    
    @classmethod
    def from_csv(cls, csv_file):
        return cls(pd.read_csv(csv_file, index_col=0))
    
    def to_dataframe(self):
        return self.returns_by_symbol

    def filter_by_symbols(self, symbols):
        return ReturnsBySymbol(self.returns_by_symbol[symbols])

    def adjust_for_inflation(self, inflation_rates):
        def _adjust_for_inflation(returns_for_year):
            year = returns_for_year.name
            inflation_rate = inflation_rates[year]
            return (returns_for_year + 1) / (inflation_rate + 1) - 1
        return ReturnsBySymbol(self.returns_by_symbol.apply(_adjust_for_inflation, axis=1))

    def to_portfolio_returns(self, allocation) -> PortfolioReturns:
        return PortfolioReturns(self.returns_by_symbol, allocation)

    def to_portfolio_returns_group(self, allocations) -> PortfolioReturnsByAllocation:
        return PortfolioReturnsByAllocation(self.returns_by_symbol, allocations)

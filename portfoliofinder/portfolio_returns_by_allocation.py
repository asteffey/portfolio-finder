import pandas as pd

from .portfolio_returns import _get_allocation_symbols, _get_portfolio_returns

class PortfolioReturnsByAllocation():

    def __init__(self, returns_by_symbol: pd.Series, allocations):
        allocation_symbols = _get_allocation_symbols(allocations[0])
        returns_by_symbol = returns_by_symbol[allocation_symbols]

        self.portfolio_returns_by_allocation = {}
        for allocation in allocations:
            portfolio_returns = _get_portfolio_returns(allocation, returns_by_symbol)
            self.portfolio_returns_by_allocation[allocation] = portfolio_returns

    def get_series(self, allocation) -> pd.Series:
        return self.portfolio_returns_by_allocation[allocation]

    def to_dataframe(self) -> pd.DataFrame:
        return _convert_to_dataframe_by_allocation(self.portfolio_returns_by_allocation)


def _convert_to_dataframe_by_allocation(series_dict_by_allocation):
    df = pd.concat(series_dict_by_allocation, axis=1).T
    
    an_allocation = list(series_dict_by_allocation.keys())[0]
    allocation_symbols = list(an_allocation._asdict().keys())
    df.index.names = allocation_symbols
    
    return df
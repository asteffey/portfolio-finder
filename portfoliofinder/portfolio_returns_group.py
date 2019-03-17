import pandas as pd

from .portfolio_returns import _get_allocation_symbols, _get_portfolio_returns

class PortfolioReturnsGroup():

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



def _get_portfolio_returns(portfolio_allocation, returns_by_symbol: pd.DataFrame) -> pd.Series:
    portfolio_returns = []
    for row in returns_by_symbol.iterrows():
        return_by_symbol = row[1]
        return_for_year = sum(return_by_symbol * portfolio_allocation)
        portfolio_returns.append(return_for_year)
    years = returns_by_symbol.axes[0]
    return pd.Series(portfolio_returns, index=years, name="Portfolio Return")

def _convert_to_dataframe_by_allocation(series_dict_by_allocation):
    df = pd.concat(series_dict_by_allocation, axis=1).T
    
    an_allocation = list(series_dict_by_allocation.keys())[0]
    allocation_symbols = list(an_allocation._asdict().keys())
    df.index.names = allocation_symbols
    
    return df
import pandas as pd

class PortfolioReturns():

    def __init__(self, returns_by_symbol: pd.Series, allocation):
        allocation_symbols = _get_allocation_symbols(allocation)
        self._returns = _get_portfolio_returns(allocation, returns_by_symbol[allocation_symbols])

    def to_series(self) -> pd.Series:
        return self._returns



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
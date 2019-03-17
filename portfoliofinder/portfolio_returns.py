import pandas as pd
from .returns_by_symbol import ReturnsBySymbol

class PortfolioReturns():

    def __init__(self, returns_by_symbol: ReturnsBySymbol, allocation):
        symbols = list(allocation._fields)
        returns = returns_by_symbol.to_dataframe()
        self.returns = _get_portfolio_returns(allocation, returns[symbols])

    def to_series(self) -> pd.Series:
        return self.returns

    
    


def _get_portfolio_returns(portfolio_allocation, returns_by_symbol: pd.DataFrame) -> pd.Series:
    portfolio_returns = []
    for row in returns_by_symbol.iterrows():
        return_by_symbol = row[1]
        return_for_year = sum(return_by_symbol * portfolio_allocation)
        portfolio_returns.append(return_for_year)
    years = returns_by_symbol.axes[0]
    return pd.Series(portfolio_returns, index=years, name="Portfolio Return")
import pandas as pd
from functools import reduce
from functools import wraps

from .contributions import Contributions
from .stats import DEFAULT_STATS

class PortfolioTimeframesByStartYear():

    def __init__(self, portfolio_returns: pd.Series, target_value, contributions: Contributions):
        self._portfolio_timeframe_by_startyear = _get_portfolio_timeframe_by_startyear(
            portfolio_returns, target_value, contributions)

    def to_series(self) -> pd.Series:
        return self._portfolio_timeframe_by_startyear

    def get_statistics(self, statistics = DEFAULT_STATS) -> pd.Series:
        return _get_statistics(self._portfolio_timeframe_by_startyear, statistics)



def _get_portfolio_timeframe_by_startyear(portfolio_returns, target_value, contributions: Contributions):
    all_years = portfolio_returns.index
    
    timeframes = []
    start_years = []
    for start_year in all_years:
        value = 0
        investment_year = 0
        while value < target_value and start_year + investment_year <= all_years[-1]:
            contribution = contributions.get_contribution_for_year(investment_year)
            current_return = portfolio_returns.loc[start_year + investment_year]
            value = (value + contribution) * (1 + current_return)

            investment_year += 1
        
        if value >= target_value:
            timeframes.append(investment_year)
            start_years.append(start_year)
        
    
    timeframe_by_startyear = pd.Series(data=timeframes,
                                       index=pd.Index(start_years, name='Year'),
                                       name="Portfolio Timeframe")
    return timeframe_by_startyear.dropna().astype(float)


def _get_statistics(portfolio_values : pd.Series, statistics) -> pd.Series:
    statistics = list(map(lambda stat: _typecheck_series(stat) if callable(stat) else stat, statistics))
    ret = portfolio_values.agg(statistics)
    ret.name = "Portfolio Timeframe"
    ret.index.name = "Statistic"
    return ret

def _typecheck_series(func):
    @wraps(func)
    def wrapper(series):
        if isinstance(series, pd.Series):
            return func(series)
        else:
            raise TypeError
    return wrapper
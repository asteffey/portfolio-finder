import pandas as pd
from functools import reduce
from functools import wraps

from .contributions import Contributions
from .stats import DEFAULT_STATS

class PortfolioValuesByStartYear():

    def __init__(self, portfolio_returns: pd.Series, timeframe, contributions: Contributions):
        self._portfolio_value_by_startyear = _get_portfolio_value_by_startyear(
            portfolio_returns, timeframe, contributions)

    def to_series(self) -> pd.Series:
        return self._portfolio_value_by_startyear

    def get_statistics(self, statistics = DEFAULT_STATS) -> pd.Series:
        return _get_statistics(self._portfolio_value_by_startyear, statistics)


def _get_portfolio_value_by_startyear(portfolio_returns, timeframe, contributions: Contributions):
    start_years = _get_start_years_for_timeframe(portfolio_returns.index, timeframe)
    
    values = []
    for start_year in start_years:
        value = _get_portfolio_value_for_startyear(start_year, portfolio_returns, timeframe, contributions)
        values.append(value)
    
    return pd.Series(data=values,
                     index=pd.Index(start_years, name='Year'),
                     name="Portfolio Value")

def _get_start_years_for_timeframe(years: pd.Index, timeframe):
    first_year = years[0]
    last_year = years[-1] - (timeframe - 1)
    return _inclusive_range(first_year, last_year)


def _inclusive_range(start, stop, step=1):
    return range(start, (stop + 1) if step >= 0 else (stop - 1), step)


def _get_portfolio_value_for_startyear(start_year, portfolio_returns: pd.Series, timeframe, contributions: Contributions):
    investment_years = range(start_year, start_year + timeframe)
    returns_over_timeframe = portfolio_returns.loc[investment_years]

    timeframe_iter = iter(range(timeframe))
    def reduce_to_portfolio_value(prev_value, current_return):
        investment_year = next(timeframe_iter)
        contribution = contributions.get_contribution_for_year(investment_year)
        value = prev_value + contribution
        return value * (1 + current_return)
    
    return reduce(reduce_to_portfolio_value, returns_over_timeframe, 0)


def _get_statistics(portfolio_values : pd.Series, statistics) -> pd.Series:
    statistics = list(map(lambda stat: _typecheck_series(stat) if callable(stat) else stat, statistics))
    ret = portfolio_values.agg(statistics)
    ret.name = "Portfolio Value"
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
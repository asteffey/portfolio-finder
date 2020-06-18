from functools import reduce

import pandas as pd

from ._backtested_data import _BacktestedData
from ..contributions import Contributions


class BacktestedValues(_BacktestedData):
    """Backtested portfolio values, by start year, after a fixed timeframe."""

    def __init__(self, portfolio_returns_by_allocation: dict,
                 timeframe: int, contributions: Contributions):
        _BacktestedData.__init__(self,
                                 _get_portfolio_value_by_startyear,
                                 portfolio_returns_by_allocation,
                                 timeframe,
                                 contributions)

def _get_portfolio_value_by_startyear(portfolio_returns, timeframe, contributions: Contributions):
    start_years = _get_start_years_for_timeframe(
        portfolio_returns.index, timeframe)

    values = []
    for start_year in start_years:
        value = _get_portfolio_value_for_startyear(
            start_year, portfolio_returns, timeframe, contributions)
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


def _get_portfolio_value_for_startyear(start_year, portfolio_returns: pd.Series,
                                       timeframe, contributions: Contributions):
    investment_years = range(start_year, start_year + timeframe)
    returns_over_timeframe = portfolio_returns.loc[investment_years]

    timeframe_iter = iter(range(timeframe))

    def reduce_to_portfolio_value(prev_value, current_return):
        investment_year = next(timeframe_iter)
        contribution = contributions.get_contribution_for_year(investment_year)
        value = prev_value + contribution
        return value * (1 + current_return)

    return reduce(reduce_to_portfolio_value, returns_over_timeframe, 0)

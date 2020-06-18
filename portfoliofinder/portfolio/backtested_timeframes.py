import pandas as pd

from ._backtested_data import _BacktestedData
from ..contributions import Contributions


class BacktestedTimeframes(_BacktestedData):
    """Backtested portfolio timeframes, by start year, required to
    achieve a target value.
    """

    def __init__(self, portfolio_returns_by_allocation: dict,
                 target_value: float, contributions: Contributions):
        _BacktestedData.__init__(self,
                                 _get_portfolio_timeframe_by_startyear,
                                 portfolio_returns_by_allocation,
                                 target_value,
                                 contributions)


def _get_portfolio_timeframe_by_startyear(portfolio_returns, target_value,
                                          contributions: Contributions)\
        -> pd.Series:
    all_years = portfolio_returns.index

    timeframes = []
    start_years = []
    for start_year in all_years:
        value = 0
        investment_year = 0
        while value < target_value and start_year + investment_year <= all_years[-1]:
            contribution = contributions.get_contribution_for_year(
                investment_year)
            current_return = portfolio_returns.loc[start_year +
                                                   investment_year]
            value = (value + contribution) * (1 + current_return)

            investment_year += 1

        if value >= target_value:
            timeframes.append(investment_year)
            start_years.append(start_year)

    timeframe_by_startyear = pd.Series(data=timeframes,
                                       index=pd.Index(
                                           start_years, name='Year'),
                                       name="Portfolio Timeframe")
    return timeframe_by_startyear.dropna().astype(float)

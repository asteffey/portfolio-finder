import pandas as pd
from .self_pickling import SelfPickling

from .contributions import Contributions
from .stats import DEFAULT_STATS, _get_statistics, StatListType


class PortfolioTimeframesByStartYear(SelfPickling):
    """
    Timeframes for portfolio to achieve a target value, by start year,
    for a specific allocation mix and contributions schedule.
    """

    def __init__(self, portfolio_returns: pd.Series, target_value, contributions: Contributions):
        self._portfolio_timeframe_by_startyear = _get_portfolio_timeframe_by_startyear(
            portfolio_returns, target_value, contributions)

    def as_series(self) -> pd.Series:
        """Gets as pandas Series."""
        return self._portfolio_timeframe_by_startyear

    def get_statistics(self, statistics: StatListType = DEFAULT_STATS) -> pd.Series:
        """Gets statistical results for the amount of time required for backtested
        portfolios to achieve a target value given a specific
        allocation mix and contribution schedule.

        :param statistics: array of statistic functions for pandas Series
        :return: A pandas Series containing values for each statistic
        """
        return _get_portfolio_timeframe_statistics(
            self._portfolio_timeframe_by_startyear, statistics)


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


def _get_portfolio_timeframe_statistics(portfolio_values: pd.Series, statistics) -> pd.Series:
    statistics = _get_statistics(portfolio_values, statistics)
    statistics.name = "Portfolio Timeframe"
    return statistics

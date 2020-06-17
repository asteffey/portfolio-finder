from functools import wraps
from typing import Callable, List, Union
from scipy.stats import gmean
import pandas as pd
import progressbar

StatFunction = Callable[[pd.Series], float]
StatListType = List[Union[str, StatFunction]]

def percentile_for(percentile: int) -> StatFunction:
    """Creates a function to calculate the specified percentile.

    :param percentile: Percentile as an integer from 0 to 100
    :return: function to calculate the specified percentile
    """
    if percentile < 0 or percentile > 100:
        raise TypeError('percentile must be between 0 and 100, inclusive')

    def percentile_(series: pd.Series):
        return series.quantile(percentile / 100)
    percentile_.__name__ = 'percentile_{:2.0f}'.format(percentile)
    return percentile_


def sharpe_ratio(series: pd.Series) -> float:
    """Calculates the Sharpe ratio for a series of returns.

    This function assumes that returns are already relative to
    a risk-free rate, and thus simply calculates `mean / std`.

    :param series: series of calculate ratio for
    :return: sharpe ratio
    """
    return series.mean() / series.std()


DEFAULT_STATS = ['min'] + [percentile_for(x) for x in range(10, 91, 10)] + [
    'max', 'mean', gmean, 'std', sharpe_ratio]


def _get_statistics(portfolio_values: pd.Series, statistics: StatListType) -> pd.Series:
    statistics = list(map(lambda stat: _typecheck_series(
        stat) if callable(stat) else stat, statistics))
    statistics = portfolio_values.agg(statistics)
    statistics.index.name = "Statistic"
    return statistics


def _typecheck_series(func):
    @wraps(func)
    def wrapper(series):
        if isinstance(series, pd.Series):
            return func(series)
        raise TypeError
    return wrapper


def _get_statistics_by_allocation(portfolio_values_by_allocations, statistics: StatListType):
    statistics_by_allocation = {}
    for allocation in progressbar.progressbar(portfolio_values_by_allocations.keys()):
        portfolio_timeframe_by_startyear = _get_statistics(
            portfolio_values_by_allocations[allocation], statistics)
        statistics_by_allocation[allocation] = portfolio_timeframe_by_startyear
    return statistics_by_allocation

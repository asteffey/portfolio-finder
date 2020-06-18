import pandas as pd
from scipy.stats import gmean

from .types import StatList, StatFunction


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


DEFAULT_STATS: StatList = ['min'] + [percentile_for(x) for x in range(10, 91, 10)] + [
    'max', 'mean', gmean, 'std', sharpe_ratio]
"""List of default statistic to use."""

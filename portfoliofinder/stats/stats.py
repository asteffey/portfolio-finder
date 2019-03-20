from pandas import Series as __Series
from scipy.stats import gmean
from functools import wraps
import pandas as pd

def percentile_for(percentile):
    def percentile_(series : __Series):
        return series.quantile(percentile / 100)
    percentile_.__name__ = 'percentile_{:2.0f}'.format(percentile)
    return percentile_


DEFAULT_STATS = ['min'] + [percentile_for(x) for x in range(10,91,10)] + ['max', 'mean', gmean]

def get_statistics(portfolio_values : pd.Series, statistics) -> pd.Series:
    statistics = list(map(lambda stat: _typecheck_series(stat) if callable(stat) else stat, statistics))
    statistics = portfolio_values.agg(statistics)
    statistics.index.name = "Statistic"
    statistics.name = "Portfolio" #TODO: fix me
    return statistics


def _typecheck_series(func):
    @wraps(func)
    def wrapper(series):
        if isinstance(series, pd.Series):
            return func(series)
        else:
            raise TypeError
    return wrapper

def get_statistics_by_allocation(portfolio_values_by_allocations, statistics):
    statistics_by_allocation = {}
    for allocation in portfolio_values_by_allocations.keys():
        portfolio_timeframe_by_startyear = get_statistics(portfolio_values_by_allocations[allocation], statistics)
        statistics_by_allocation[allocation] = portfolio_timeframe_by_startyear
    return _convert_to_dataframe_by_allocation(statistics_by_allocation)


def _convert_to_dataframe_by_allocation(series_dict_by_allocation):
    df = pd.concat(series_dict_by_allocation, axis=1).T
    
    an_allocation = list(series_dict_by_allocation.keys())[0]
    allocation_symbols = list(an_allocation._asdict().keys())
    df.index.names = allocation_symbols
    
    return df
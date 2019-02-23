from pandas import Series as __Series
from scipy.stats import gmean as __gmean

def percentile_for(percentile):
    def percentile_(series : __Series):
        if isinstance(series, __Series):
            return series.quantile(percentile / 100)
        else:
            raise TypeError    
    percentile_.__name__ = 'percentile_{:2.0f}'.format(percentile)
    return percentile_


def gmean(series):
    if isinstance(series, __Series):
        return __gmean(series)
    else:
        raise TypeError


DEFAULT_STATS = ['min'] + [percentile_for(x) for x in range(10,91,10)] + ['max', 'mean', gmean]
#DEFAULT_STATS = ['min', 'max', 'mean', gmean]
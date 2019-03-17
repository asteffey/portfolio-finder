from pandas import Series as __Series
from scipy.stats import gmean

def percentile_for(percentile):
    def percentile_(series : __Series):
        return series.quantile(percentile / 100)
    percentile_.__name__ = 'percentile_{:2.0f}'.format(percentile)
    return percentile_


DEFAULT_STATS = ['min'] + [percentile_for(x) for x in range(10,91,10)] + ['max', 'mean', gmean]

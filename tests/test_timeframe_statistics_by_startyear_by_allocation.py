from pandas.testing import assert_series_equal
import portfoliofinder as pf
from testdata_constants import *


def test_get_with_default_from_portfolio_timeframe_by_startyear_by_allocation():
    """tests get_statistics_by_allocation"""
    portfolio_returns_by_allocation = pf.Returns(
        EXPECTED_SPECIFIC_RETURNS, EXPECTED_PORTFOLIO_ALLOCATIONS)
    portfolio_timeframe_by_startyear_by_allocation = portfolio_returns_by_allocation\
        .with_initial_contribution(1)\
        .get_backtested_timeframes(MY_DEFAULT_TARGET)

    actual_statistics_by_allocation = portfolio_timeframe_by_startyear_by_allocation.get_statistics().as_dataframe()

    assert len(actual_statistics_by_allocation) == len(
        EXPECTED_PORTFOLIO_ALLOCATIONS)

    actual_portfolio_stats = actual_statistics_by_allocation.loc[MY_ALLOCATION]
    actual_portfolio_stats.name = "Portfolio Timeframe"
    assert_series_equal(actual_portfolio_stats,
                        EXPECTED_DEFAULT_STATISTICS_FOR_PORTFOLIO_TIMEFRAMES)


def test_get_with_custom_from_portfolio_timeframe_by_startyear_by_allocation():
    """tests get_statistics_by_allocation"""
    portfolio_returns_by_allocation = pf.Returns(
        EXPECTED_SPECIFIC_RETURNS, EXPECTED_PORTFOLIO_ALLOCATIONS)
    portfolio_timeframe_by_startyear_by_allocation = portfolio_returns_by_allocation \
        .with_initial_contribution(1) \
        .get_backtested_timeframes(MY_DEFAULT_TARGET)

    actual_statistics_by_allocation = portfolio_timeframe_by_startyear_by_allocation.get_statistics(
        MY_CUSTOM_STATISTICS).as_dataframe()

    assert len(actual_statistics_by_allocation) == len(
        EXPECTED_PORTFOLIO_ALLOCATIONS)

    actual_portfolio_stats = actual_statistics_by_allocation.loc[MY_ALLOCATION]
    actual_portfolio_stats.name = "Portfolio Timeframe"
    assert_series_equal(actual_portfolio_stats,
                        EXPECTED_DEFAULT_STATISTICS_FOR_PORTFOLIO_TIMEFRAMES_WITH_CUSTOM_STATS)


def test_get_max_for_each_statistic():
    portfolio_returns_by_allocation = pf.Returns(
        EXPECTED_SPECIFIC_RETURNS, EXPECTED_PORTFOLIO_ALLOCATIONS)
    portfolio_timeframe_by_startyear_by_allocation = portfolio_returns_by_allocation \
        .with_initial_contribution(1) \
        .get_backtested_timeframes(MY_DEFAULT_TARGET)

    statistics_by_allocation = portfolio_timeframe_by_startyear_by_allocation.get_statistics()

    res = statistics_by_allocation.get_allocations_which_max_each_statistic()
    assert len(res) == len(pf.stats.DEFAULT_STATS)
    assert res.loc['min']['Portfolio Timeframe'] == max(
        statistics_by_allocation.as_dataframe()['min'])
    assert res.loc['max']['Portfolio Timeframe'] == max(
        statistics_by_allocation.as_dataframe()['max'])
    assert res.loc['gmean']['Portfolio Timeframe'] == max(
        statistics_by_allocation.as_dataframe()['gmean'])
    assert res.loc['percentile_30']['Portfolio Timeframe'] == max(
        statistics_by_allocation.as_dataframe()['percentile_30'])


def test_get_min_for_each_statistic():
    portfolio_returns_by_allocation = pf.Returns(
        EXPECTED_SPECIFIC_RETURNS, EXPECTED_PORTFOLIO_ALLOCATIONS)
    portfolio_timeframe_by_startyear_by_allocation = portfolio_returns_by_allocation \
        .with_initial_contribution(1) \
        .get_backtested_timeframes(MY_DEFAULT_TARGET)

    statistics_by_allocation = portfolio_timeframe_by_startyear_by_allocation.get_statistics()

    res = statistics_by_allocation.get_allocations_which_min_each_statistic()
    assert len(res) == len(pf.stats.DEFAULT_STATS)
    assert res.loc['min']['Portfolio Timeframe'] == min(
        statistics_by_allocation.as_dataframe()['min'])
    assert res.loc['max']['Portfolio Timeframe'] == min(
        statistics_by_allocation.as_dataframe()['max'])
    assert res.loc['gmean']['Portfolio Timeframe'] == min(
        statistics_by_allocation.as_dataframe()['gmean'])
    assert res.loc['percentile_30']['Portfolio Timeframe'] == min(
        statistics_by_allocation.as_dataframe()['percentile_30'])

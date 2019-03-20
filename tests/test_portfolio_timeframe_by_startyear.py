"""
pytests for portfolio_timeframe_by_startyear module
"""

import pytest
from pandas.util.testing import assert_frame_equal
from pandas.util.testing import assert_series_equal

import portfoliofinder as pf

from testdata_reader import read_dataframe, read_series
from test_portfolio_returns import DEFAULT_PORTFOLIO_RETURNS, EXPECTED_PORTFOLIO_RETURNS, MY_ALLOCATION

MY_SCHEDULED_CONTRIBUTIONS = pf.contributions.ScheduledContributions(
    {n: (1000 if n in (0, 5) else 10) for n in range(0, 100)})

MY_DEFAULT_TARGET = 4
MY_TARGET_WITH_CONTRIBUTIONS = 10000

EXPECTED_PORTFOLIO_TIMEFRAME_BY_STARTYEAR = read_series('portfolio_timeframe_by_startyear', usecols=['Year', 'Portfolio Timeframe']).dropna()
EXPECTED_PORTFOLIO_TIMEFRAME_BY_STARTYEAR_WITH_CONTRIBUTIONS = read_series('portfolio_timeframe_by_startyear_with_contributions', usecols=['Year', 'Portfolio Timeframe']).dropna()

CUSTOM_STATISTICS = ['min',pf.stats.percentile_for(10),pf.stats.gmean]
EXPECTED_DEFAULT_STATISTICS_FOR_PORTFOLIO_TIMEFRAMES = read_series('default_statistics_for_timeframe', usecols=['Statistic', 'Portfolio Timeframe'])
EXPECTED_DEFAULT_STATISTICS_FOR_PORTFOLIO_TIMEFRAMES_WITH_CUSTOM_STATS = read_series('custom_statistics_for_timeframe', usecols=['Statistic', 'Portfolio Timeframe'])


def test_init_with_default_contributions():
    actual_portfolio_timeframe_by_startyear = pf.PortfolioTimeframesByStartYear(
        EXPECTED_PORTFOLIO_RETURNS, MY_DEFAULT_TARGET, pf.contributions.DEFAULT_CONTRIBUTION)
    
    assert_series_equal(actual_portfolio_timeframe_by_startyear.to_series(),
                        EXPECTED_PORTFOLIO_TIMEFRAME_BY_STARTYEAR)


def test_from_portfolio_returns_with_default_contributions():
    actual_portfolio_timeframe_by_startyear = DEFAULT_PORTFOLIO_RETURNS.to_portfolio_timeframe_by_startyear(
        MY_DEFAULT_TARGET)

    assert_series_equal(actual_portfolio_timeframe_by_startyear.to_series(),
                        EXPECTED_PORTFOLIO_TIMEFRAME_BY_STARTYEAR)


def test_from_portfolio_returns_with_custom_contributions():
    """
    tests get_portfolio_value_by_startyear with custom contributions
    """
    actual_portfolio_timeframe_by_startyear = DEFAULT_PORTFOLIO_RETURNS.to_portfolio_timeframe_by_startyear(
        MY_TARGET_WITH_CONTRIBUTIONS, MY_SCHEDULED_CONTRIBUTIONS)

    assert_series_equal(actual_portfolio_timeframe_by_startyear.to_series(),
                        EXPECTED_PORTFOLIO_TIMEFRAME_BY_STARTYEAR_WITH_CONTRIBUTIONS)

def test_get_statistics_with_default():
    """tests get_statistics with default statistics"""
    portfolio_timeframe_by_startyear = pf.PortfolioTimeframesByStartYear(
        EXPECTED_PORTFOLIO_RETURNS, MY_DEFAULT_TARGET, pf.contributions.DEFAULT_CONTRIBUTION)
    actual_statistics = portfolio_timeframe_by_startyear.get_statistics()

    assert_series_equal(actual_statistics, EXPECTED_DEFAULT_STATISTICS_FOR_PORTFOLIO_TIMEFRAMES)


def test_get_statistics_with_custom():
    """tests get_statistics with default statistics"""
    portfolio_timeframe_by_startyear = pf.PortfolioTimeframesByStartYear(
        EXPECTED_PORTFOLIO_RETURNS, MY_DEFAULT_TARGET, pf.contributions.DEFAULT_CONTRIBUTION)
    actual_statistics = portfolio_timeframe_by_startyear.get_statistics(CUSTOM_STATISTICS)

    assert_series_equal(actual_statistics, EXPECTED_DEFAULT_STATISTICS_FOR_PORTFOLIO_TIMEFRAMES_WITH_CUSTOM_STATS)
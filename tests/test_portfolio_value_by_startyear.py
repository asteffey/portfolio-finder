"""
pytests for portfolio_value_by_startyear module
"""

from pandas.util.testing import assert_series_equal

import portfoliofinder as pf

from testdata_constants import *


def test_init_with_default_contributions():
    actual_portfolio_value_by_startyear = pf.PortfolioValuesByStartYear(
        EXPECTED_PORTFOLIO_RETURNS, MY_TIMEFRAME, pf.contributions.DEFAULT_CONTRIBUTION)

    assert_series_equal(actual_portfolio_value_by_startyear.to_series(),
                        EXPECTED_PORTFOLIO_VALUE_BY_STARTYEAR)


def test_from_portfolio_returns_with_default_contributions():
    portfolio_returns = pf.PortfolioReturns(
        EXPECTED_SPECIFIC_RETURNS, MY_ALLOCATION)
    actual_portfolio_value_by_startyear = portfolio_returns.to_portfolio_value_by_startyear(
        MY_TIMEFRAME)

    assert_series_equal(actual_portfolio_value_by_startyear.to_series(),
                        EXPECTED_PORTFOLIO_VALUE_BY_STARTYEAR)


def test_from_portfolio_returns_with_custom_contributions():
    """
    tests get_portfolio_value_by_startyear with custom contributions
    """
    portfolio_returns = pf.PortfolioReturns(
        EXPECTED_SPECIFIC_RETURNS, MY_ALLOCATION)
    actual_portfolio_value_by_startyear = portfolio_returns.to_portfolio_value_by_startyear(
        MY_TIMEFRAME, MY_SCHEDULED_CONTRIBUTIONS)

    assert_series_equal(actual_portfolio_value_by_startyear.to_series(),
                        EXPECTED_PORTFOLIO_VALUE_BY_STARTYEAR_WITH_CONTRIBUTIONS)

def test_get_statistics_with_default():
    """tests get_statistics with default statistics"""
    portfolio_value_by_startyear = pf.PortfolioValuesByStartYear(
        EXPECTED_PORTFOLIO_RETURNS, MY_TIMEFRAME, pf.contributions.DEFAULT_CONTRIBUTION)
    actual_statistics = portfolio_value_by_startyear.get_statistics()

    assert_series_equal(actual_statistics, EXPECTED_DEFAULT_STATISTICS_FOR_PORTFOLIO_VALUES)


def test_get_statistics_with_custom():
    """tests get_statistics with custom statistics"""
    portfolio_value_by_startyear = pf.PortfolioValuesByStartYear(
        EXPECTED_PORTFOLIO_RETURNS, MY_TIMEFRAME, pf.contributions.DEFAULT_CONTRIBUTION)
    actual_statistics = portfolio_value_by_startyear.get_statistics(MY_CUSTOM_STATISTICS)

    assert_series_equal(actual_statistics, EXPECTED_DEFAULT_STATISTICS_FOR_PORTFOLIO_VALUES_WITH_CUSTOM_STATS)
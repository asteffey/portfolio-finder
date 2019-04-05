"""
pytests for portfolio_value_by_startyear_by_allocation module
"""

import pytest
from pandas.util.testing import assert_frame_equal
from pandas.util.testing import assert_series_equal

import portfoliofinder as pf

from testdata_reader import read_dataframe, read_series
from test_portfolio_returns import MY_ALLOCATION, EXPECTED_SPECIFIC_RETURNS, EXPECTED_PORTFOLIO_RETURNS
from test_portfolio_returns import DEFAULT_PORTFOLIO_RETURNS, EXPECTED_PORTFOLIO_RETURNS, MY_ALLOCATION
from test_portfolio_timeframe_by_startyear import CUSTOM_STATISTICS, MY_SCHEDULED_CONTRIBUTIONS
from test_portfolio_value_by_startyear import MY_TIMEFRAME
from test_portfolio_value_by_startyear import EXPECTED_PORTFOLIO_VALUE_BY_STARTYEAR, EXPECTED_PORTFOLIO_VALUE_BY_STARTYEAR_WITH_CONTRIBUTIONS
from test_portfolio_value_by_startyear import EXPECTED_DEFAULT_STATISTICS_FOR_PORTFOLIO_VALUES, EXPECTED_DEFAULT_STATISTICS_FOR_PORTFOLIO_VALUES_WITH_CUSTOM_STATS
from test_portfolio_returns_by_allocation import DEFAULT_PORTFOLIO_RETURNS_BY_ALLOCATION

def test_init_with_default_contributions():
    portfolio_value_by_startyear_by_allocation = pf.PortfolioValuesByStartYearByAllocation(
        {MY_ALLOCATION: EXPECTED_PORTFOLIO_RETURNS}, MY_TIMEFRAME, pf.contributions.DEFAULT_CONTRIBUTION)

    actual_portfolio_value_by_startyear = portfolio_value_by_startyear_by_allocation.to_series(MY_ALLOCATION)

    assert_series_equal(actual_portfolio_value_by_startyear,
                        EXPECTED_PORTFOLIO_VALUE_BY_STARTYEAR)


def test_from_portfolio_returns_by_allocation_with_default_contributions():
    portfolio_value_by_startyear_by_allocation = DEFAULT_PORTFOLIO_RETURNS_BY_ALLOCATION.to_portfolio_value_by_startyear_by_allocation(
        MY_TIMEFRAME)

    actual_portfolio_value_by_startyear = portfolio_value_by_startyear_by_allocation.to_series(MY_ALLOCATION)

    assert_series_equal(actual_portfolio_value_by_startyear,
                        EXPECTED_PORTFOLIO_VALUE_BY_STARTYEAR)


def test_to_dataframe():
    portfolio_value_by_startyear_by_allocation = DEFAULT_PORTFOLIO_RETURNS_BY_ALLOCATION.to_portfolio_value_by_startyear_by_allocation(
        MY_TIMEFRAME)

    actual_portfolio_value_by_startyear = portfolio_value_by_startyear_by_allocation.to_dataframe().loc[MY_ALLOCATION]

    expected = EXPECTED_PORTFOLIO_VALUE_BY_STARTYEAR.copy()
    expected.name = MY_ALLOCATION

    assert_series_equal(actual_portfolio_value_by_startyear,
                        expected)


def test_from_portfolio_returns_by_allocation_with_custom_contributions():
    """
    tests get_portfolio_value_by_startyear with custom contributions
    """
    portfolio_value_by_startyear_by_allocation = DEFAULT_PORTFOLIO_RETURNS_BY_ALLOCATION.to_portfolio_value_by_startyear_by_allocation(
        MY_TIMEFRAME, MY_SCHEDULED_CONTRIBUTIONS)

    actual_portfolio_value_by_startyear = portfolio_value_by_startyear_by_allocation.to_series(MY_ALLOCATION)

    assert_series_equal(actual_portfolio_value_by_startyear,
                        EXPECTED_PORTFOLIO_VALUE_BY_STARTYEAR_WITH_CONTRIBUTIONS)


def test_get_statistics_by_allocation_with_default():
    """tests get_statistics_by_allocation"""
    portfolio_value_by_startyear_by_allocation = DEFAULT_PORTFOLIO_RETURNS_BY_ALLOCATION.to_portfolio_value_by_startyear_by_allocation(
        MY_TIMEFRAME)

    actual_statistics_by_allocation = portfolio_value_by_startyear_by_allocation.get_statistics().to_dataframe()
    
    assert len(actual_statistics_by_allocation) == len(DEFAULT_PORTFOLIO_RETURNS_BY_ALLOCATION.to_dataframe())

    actual_portfolio_stats = actual_statistics_by_allocation.loc[MY_ALLOCATION]
    actual_portfolio_stats.name = "Portfolio Value"
    assert_series_equal(actual_portfolio_stats, EXPECTED_DEFAULT_STATISTICS_FOR_PORTFOLIO_VALUES)

def test_get_statistics_by_allocation_with_custom():
    """tests get_statistics_by_allocation"""
    portfolio_value_by_startyear_by_allocation = DEFAULT_PORTFOLIO_RETURNS_BY_ALLOCATION.to_portfolio_value_by_startyear_by_allocation(
        MY_TIMEFRAME)

    actual_statistics_by_allocation = portfolio_value_by_startyear_by_allocation.get_statistics(CUSTOM_STATISTICS).to_dataframe()
    
    assert len(actual_statistics_by_allocation) == len(DEFAULT_PORTFOLIO_RETURNS_BY_ALLOCATION.to_dataframe())

    actual_portfolio_stats = actual_statistics_by_allocation.loc[MY_ALLOCATION]
    actual_portfolio_stats.name = "Portfolio Value"
    assert_series_equal(actual_portfolio_stats, EXPECTED_DEFAULT_STATISTICS_FOR_PORTFOLIO_VALUES_WITH_CUSTOM_STATS)
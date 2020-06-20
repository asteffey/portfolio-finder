"""
pytests for portfolio_timeframe_by_startyear_by_allocation module
"""

from pandas.testing import assert_series_equal

import portfoliofinder as pf

from testdata_constants import *


def test_init():
    portfolio_timeframe_by_startyear_by_allocation = pf.BacktestedTimeframes(
        {MY_ALLOCATION: EXPECTED_PORTFOLIO_RETURNS}, MY_DEFAULT_TARGET, False, SINGLE_CONTRIBUTION)

    actual_portfolio_timeframe_by_startyear = portfolio_timeframe_by_startyear_by_allocation.get_series(
        MY_ALLOCATION)

    assert_series_equal(actual_portfolio_timeframe_by_startyear,
                        EXPECTED_PORTFOLIO_TIMEFRAME_BY_STARTYEAR)


def test_from_portfolio_returns_by_allocation():
    portfolio_returns_by_allocation = pf.Returns(
        EXPECTED_SPECIFIC_RETURNS, EXPECTED_PORTFOLIO_ALLOCATIONS)
    portfolio_timeframe_by_startyear_by_allocation = portfolio_returns_by_allocation\
        .with_initial_contribution(1)\
        .get_backtested_timeframes(MY_DEFAULT_TARGET)

    actual_portfolio_timeframe_by_startyear = portfolio_timeframe_by_startyear_by_allocation.get_series(
        MY_ALLOCATION)

    assert_series_equal(actual_portfolio_timeframe_by_startyear,
                        EXPECTED_PORTFOLIO_TIMEFRAME_BY_STARTYEAR)


def test_to_dataframe():
    portfolio_returns_by_allocation = pf.Returns(
        EXPECTED_SPECIFIC_RETURNS, EXPECTED_PORTFOLIO_ALLOCATIONS)
    portfolio_timeframe_by_startyear_by_allocation = portfolio_returns_by_allocation\
        .with_initial_contribution(1)\
        .get_backtested_timeframes(MY_DEFAULT_TARGET)

    actual_portfolio_timeframe_by_startyear = portfolio_timeframe_by_startyear_by_allocation.to_dataframe().loc[MY_ALLOCATION]

    expected = EXPECTED_PORTFOLIO_TIMEFRAME_BY_STARTYEAR.copy()
    expected.name = MY_ALLOCATION

    assert_series_equal(actual_portfolio_timeframe_by_startyear, expected)


def test_from_portfolio_returns_by_allocation_with_custom_contributions():
    """
    tests get_portfolio_timeframe_by_startyear with custom contributions
    """
    portfolio_returns_by_allocation = pf.Returns(
        EXPECTED_SPECIFIC_RETURNS, EXPECTED_PORTFOLIO_ALLOCATIONS)
    portfolio_timeframe_by_startyear_by_allocation = portfolio_returns_by_allocation\
        .with_contributions(MY_SCHEDULED_CONTRIBUTIONS)\
        .get_backtested_timeframes(MY_TARGET_WITH_CONTRIBUTIONS)

    actual_portfolio_timeframe_by_startyear = portfolio_timeframe_by_startyear_by_allocation\
        .get_series(MY_ALLOCATION)

    assert_series_equal(actual_portfolio_timeframe_by_startyear,
                        EXPECTED_PORTFOLIO_TIMEFRAME_BY_STARTYEAR_WITH_CONTRIBUTIONS)

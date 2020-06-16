"""
pytests for portfolio_timeframe_by_startyear_by_allocation module
"""

from pandas.testing import assert_series_equal

import portfoliofinder as pf

from testdata_constants import *


def test_init_with_default_contributions():
    portfolio_timeframe_by_startyear_by_allocation = pf.PortfolioTimeframesByStartYearByAllocation(
        {MY_ALLOCATION: EXPECTED_PORTFOLIO_RETURNS}, MY_DEFAULT_TARGET, pf.contributions.DEFAULT_CONTRIBUTION)

    actual_portfolio_timeframe_by_startyear = portfolio_timeframe_by_startyear_by_allocation.to_series(MY_ALLOCATION)

    assert_series_equal(actual_portfolio_timeframe_by_startyear,
                        EXPECTED_PORTFOLIO_TIMEFRAME_BY_STARTYEAR)


def test_from_portfolio_returns_by_allocation_with_default_contributions():
    portfolio_returns_by_allocation = pf.PortfolioReturnsByAllocation(
        EXPECTED_SPECIFIC_RETURNS, EXPECTED_PORTFOLIO_ALLOCATIONS)
    portfolio_timeframe_by_startyear_by_allocation = portfolio_returns_by_allocation.to_portfolio_timeframe_by_startyear_by_allocation(
        MY_DEFAULT_TARGET)

    actual_portfolio_timeframe_by_startyear = portfolio_timeframe_by_startyear_by_allocation.to_series(MY_ALLOCATION)

    assert_series_equal(actual_portfolio_timeframe_by_startyear,
                        EXPECTED_PORTFOLIO_TIMEFRAME_BY_STARTYEAR)


def test_to_dataframe():
    portfolio_returns_by_allocation = pf.PortfolioReturnsByAllocation(
        EXPECTED_SPECIFIC_RETURNS, EXPECTED_PORTFOLIO_ALLOCATIONS)
    portfolio_timeframe_by_startyear_by_allocation = portfolio_returns_by_allocation.to_portfolio_timeframe_by_startyear_by_allocation(
        MY_DEFAULT_TARGET)

    actual_portfolio_timeframe_by_startyear = portfolio_timeframe_by_startyear_by_allocation.to_dataframe().loc[MY_ALLOCATION]

    expected = EXPECTED_PORTFOLIO_TIMEFRAME_BY_STARTYEAR.copy()
    expected.name = MY_ALLOCATION

    assert_series_equal(actual_portfolio_timeframe_by_startyear,
                        expected)


def test_from_portfolio_returns_by_allocation_with_custom_contributions():
    """
    tests get_portfolio_timeframe_by_startyear with custom contributions
    """
    portfolio_returns_by_allocation = pf.PortfolioReturnsByAllocation(
        EXPECTED_SPECIFIC_RETURNS, EXPECTED_PORTFOLIO_ALLOCATIONS)
    portfolio_timeframe_by_startyear_by_allocation = portfolio_returns_by_allocation.to_portfolio_timeframe_by_startyear_by_allocation(
        MY_TARGET_WITH_CONTRIBUTIONS, MY_SCHEDULED_CONTRIBUTIONS)

    actual_portfolio_timeframe_by_startyear = portfolio_timeframe_by_startyear_by_allocation.to_series(MY_ALLOCATION)

    assert_series_equal(actual_portfolio_timeframe_by_startyear,
                        EXPECTED_PORTFOLIO_TIMEFRAME_BY_STARTYEAR_WITH_CONTRIBUTIONS)

"""
pytests for portfolio_value_by_startyear_by_allocation module
"""

import pytest
from pandas.util.testing import assert_frame_equal
from pandas.util.testing import assert_series_equal

import portfoliofinder as pf

from data_to_test import read_dataframe
from data_to_test import read_series
from data_to_test import MY_ALLOCATION, MY_TIMEFRAME, EXPECTED_SPECIFIC_RETURNS, EXPECTED_PORTFOLIO_RETURNS, MY_SCHEDULED_CONTRIBUTIONS
from data_to_test import EXPECTED_PORTFOLIO_VALUE_BY_STARTYEAR, EXPECTED_PORTFOLIO_VALUE_BY_STARTYEAR_WITH_CONTRIBUTIONS
from data_to_test import EXPECTED_PORTFOLIO_ALLOCATIONS

def test_init_with_default_contributions():
    portfolio_value_by_startyear_by_allocation = pf.PortfolioValuesByStartYearByAllocation(
        {MY_ALLOCATION: EXPECTED_PORTFOLIO_RETURNS}, MY_TIMEFRAME, pf.DEFAULT_CONTRIBUTION)

    actual_portfolio_value_by_startyear = portfolio_value_by_startyear_by_allocation.to_series(MY_ALLOCATION)

    assert_series_equal(actual_portfolio_value_by_startyear,
                        EXPECTED_PORTFOLIO_VALUE_BY_STARTYEAR)


def test_from_portfolio_returns_by_allocation_with_default_contributions():
    portfolio_returns_by_allocation = pf.PortfolioReturnsByAllocation(
        EXPECTED_SPECIFIC_RETURNS, EXPECTED_PORTFOLIO_ALLOCATIONS)
    portfolio_value_by_startyear_by_allocation = portfolio_returns_by_allocation.to_portfolio_value_by_startyear_by_allocation(
        MY_TIMEFRAME)

    actual_portfolio_value_by_startyear = portfolio_value_by_startyear_by_allocation.to_series(MY_ALLOCATION)

    assert_series_equal(actual_portfolio_value_by_startyear,
                        EXPECTED_PORTFOLIO_VALUE_BY_STARTYEAR)


def test_from_portfolio_returns_by_allocation_with_custom_contributions():
    """
    tests get_portfolio_value_by_startyear with custom contributions
    """
    portfolio_returns_by_allocation = pf.PortfolioReturnsByAllocation(
        EXPECTED_SPECIFIC_RETURNS, EXPECTED_PORTFOLIO_ALLOCATIONS)
    portfolio_value_by_startyear_by_allocation = portfolio_returns_by_allocation.to_portfolio_value_by_startyear_by_allocation(
        MY_TIMEFRAME, MY_SCHEDULED_CONTRIBUTIONS)

    actual_portfolio_value_by_startyear = portfolio_value_by_startyear_by_allocation.to_series(MY_ALLOCATION)

    assert_series_equal(actual_portfolio_value_by_startyear,
                        EXPECTED_PORTFOLIO_VALUE_BY_STARTYEAR_WITH_CONTRIBUTIONS)


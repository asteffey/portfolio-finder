"""
pytests for portfolio_timeframe_by_startyear module
"""

import pytest
from pandas.util.testing import assert_frame_equal
from pandas.util.testing import assert_series_equal

import portfoliofinder as pf

from data_to_test import read_dataframe
from data_to_test import read_series
from data_to_test import MY_ALLOCATION, MY_DEFAULT_TARGET, MY_TARGET_WITH_CONTRIBUTIONS
from data_to_test import EXPECTED_SPECIFIC_RETURNS, EXPECTED_PORTFOLIO_RETURNS, MY_SCHEDULED_CONTRIBUTIONS
from data_to_test import EXPECTED_PORTFOLIO_TIMEFRAME_BY_STARTYEAR, EXPECTED_PORTFOLIO_TIMEFRAME_BY_STARTYEAR_WITH_CONTRIBUTIONS


def test_init_with_default_contributions():
    actual_portfolio_timeframe_by_startyear = pf.PortfolioTimeframesByStartYear(
        EXPECTED_PORTFOLIO_RETURNS, MY_DEFAULT_TARGET, pf.DEFAULT_CONTRIBUTION)
    
    assert_series_equal(actual_portfolio_timeframe_by_startyear.to_series(),
                        EXPECTED_PORTFOLIO_TIMEFRAME_BY_STARTYEAR)


def test_from_portfolio_returns_with_default_contributions():
    portfolio_returns = pf.PortfolioReturns(
        EXPECTED_SPECIFIC_RETURNS, MY_ALLOCATION)
    actual_portfolio_timeframe_by_startyear = portfolio_returns.to_portfolio_timeframe_by_startyear(
        MY_DEFAULT_TARGET)

    assert_series_equal(actual_portfolio_timeframe_by_startyear.to_series(),
                        EXPECTED_PORTFOLIO_TIMEFRAME_BY_STARTYEAR)


def test_from_portfolio_returns_with_custom_contributions():
    """
    tests get_portfolio_value_by_startyear with custom contributions
    """
    portfolio_returns = pf.PortfolioReturns(
        EXPECTED_SPECIFIC_RETURNS, MY_ALLOCATION)
    actual_portfolio_value_by_startyear = portfolio_returns.to_portfolio_timeframe_by_startyear(
        MY_TARGET_WITH_CONTRIBUTIONS, MY_SCHEDULED_CONTRIBUTIONS)

    assert_series_equal(actual_portfolio_value_by_startyear.to_series(),
                        EXPECTED_PORTFOLIO_TIMEFRAME_BY_STARTYEAR_WITH_CONTRIBUTIONS)

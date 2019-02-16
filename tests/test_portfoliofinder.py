"""
pytests for portfoliofinder module
"""

from pandas.util.testing import assert_frame_equal
from pandas.util.testing import assert_series_equal
import pytest

import portfoliofinder as pf
import data_to_test as dtt



def test_fetch_all_returns_from_csv():
    """tests fetch_all_returns_from_csv"""
    actual_returns = pf.fetch_all_returns_from_csv("tests/test_data.csv")

    expected = dtt.get_expected_all_returns()
    assert_frame_equal(actual_returns, expected)


def test_get_specific_returns():
    """tests get_specific_returns"""
    all_returns = dtt.get_expected_all_returns()
    actual_specific_returns = pf.get_specific_returns(
        all_returns, dtt.SPECIFIC_FUNDS)

    expected = dtt.get_expected_specific_returns()
    assert_frame_equal(actual_specific_returns, expected)


def test_create_portfolio_allocations():
    """tests create_portfolio_allocations"""
    actual_allocations = pf.create_portfolio_allocations(
        dtt.SPECIFIC_FUNDS, 0.25)

    expected = dtt.get_expected_portfolio_allocations()
    assert sorted(actual_allocations) == sorted(expected)


def test_get_portfolio_returns_by_allocation():
    """tests get_portfolio_returns_by_allocation"""
    portfolio_allocations = dtt.get_expected_portfolio_allocations()
    returns = dtt.get_expected_specific_returns()
    actual_portfolio_returns_by_allocation = pf.get_portfolio_returns_by_allocation(
        portfolio_allocations, returns)

    actual_portfolio_returns = actual_portfolio_returns_by_allocation[dtt.MY_ALLOCATION]

    expected = dtt.get_expected_portfolio_returns()
    assert_series_equal(actual_portfolio_returns, expected)


def test_get_inflation_adjusted_returns_for_dataframe():
    """tests get_inflation_adjusted_returns"""
    specific_returns = dtt.get_expected_specific_returns()
    inflation_rates = dtt.get_expected_inflation_rates()
    actual_inflation_adjusted_returns = pf.get_inflation_adjusted_returns(
        specific_returns, inflation_rates)

    expected = dtt.get_expected_inflation_adjusted_specific_returns()
    assert_frame_equal(actual_inflation_adjusted_returns, expected)


def test_get_inflation_adjusted_returns_for_series():
    """tests get_inflation_adjusted_returns"""
    portfolio_returns = dtt.get_expected_portfolio_returns()
    inflation_rates = dtt.get_expected_inflation_rates()
    actual_inflation_adjusted_returns = pf.get_inflation_adjusted_returns(
        portfolio_returns, inflation_rates)

    expected = dtt.get_expected_inflation_adjusted_portfolio_returns()
    assert_series_equal(actual_inflation_adjusted_returns, expected)

def test_get_inflation_adjusted_returns_raises_typeerror():
    inflation_rates = dtt.get_expected_inflation_rates()
    with pytest.raises(TypeError):
        pf.get_inflation_adjusted_returns(0, inflation_rates)

def test_get_portfolio_value_by_startyear():
    """tests get_portfolio_value_by_startyear"""
    portfolio_returns = dtt.get_expected_portfolio_returns()
    timeframe = dtt.MY_TIMEFRAME
    actual_portfolio_value_by_startyear = pf.get_portfolio_value_by_startyear(
        portfolio_returns, timeframe)

    expected = dtt.get_expected_portfolio_value_by_startyear()
    assert_series_equal(actual_portfolio_value_by_startyear, expected)


def test_get_portfolio_value_by_startyear_with_contributions():
    """
    tests get_portfolio_value_by_startyear with an optional contributions
    argument passed
    """
    portfolio_returns = dtt.get_expected_portfolio_returns()
    timeframe = dtt.MY_TIMEFRAME
    contributions = dtt.MY_SCHEDULED_CONTRIBUTIONS
    actual_portfolio_value_by_startyear = pf.get_portfolio_value_by_startyear(
        portfolio_returns, timeframe, contributions)

    expected = dtt.get_expected_portfolio_value_by_startyear_with_contributions()
    assert_series_equal(actual_portfolio_value_by_startyear, expected)


def test_get_portfolio_timeframe_by_startyear():
    """tests get_portfolio_timeframe_by_startyear"""
    portfolio_returns = dtt.get_expected_portfolio_returns()
    target_value = dtt.MY_DEFAULT_TARGET
    actual_portfolio_timeframe_by_startyear = pf.get_portfolio_timeframe_by_startyear(
        portfolio_returns, target_value)

    expected = dtt.get_expected_portfolio_timeframe_by_startyear()
    assert_series_equal(actual_portfolio_timeframe_by_startyear, expected)


def test_get_portfolio_timeframe_by_startyear_with_contributions():
    """
    tests get_portfolio_timeframe_by_startyear with an optional contributions
    argument passed
    """
    portfolio_returns = dtt.get_expected_portfolio_returns()
    target_value = dtt.MY_TARGET_WITH_CONTRIBUTIONS
    contributions = dtt.MY_SCHEDULED_CONTRIBUTIONS
    actual_portfolio_timeframe_by_startyear = pf.get_portfolio_timeframe_by_startyear(
        portfolio_returns, target_value, contributions)

    expected = dtt.get_expected_portfolio_timeframe_by_startyear_with_contributions()
    assert_series_equal(actual_portfolio_timeframe_by_startyear, expected)


#TODO test get_statistics_for_portfolio(portfolio_timeframe_by_startyear, statistic_list)

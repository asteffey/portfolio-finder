"""
pytests for portfoliofinder module
"""

import pytest
from pandas.util.testing import assert_frame_equal
from pandas.util.testing import assert_series_equal
import pandas as pd

import portfoliofinder as pf
import data_to_test as dtt
from scipy.stats import gmean

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

def test_get_portfolio_returns_for_allocation():
    """tests get_portfolio_returns_for_allocation"""
    returns = dtt.get_expected_specific_returns()
    actual_portfolio_returns = pf.get_portfolio_returns_for_allocation(
        dtt.MY_ALLOCATION, returns)

    expected = dtt.get_expected_portfolio_returns()
    assert_series_equal(actual_portfolio_returns, expected)

def test_get_portfolio_returns_by_allocation():
    """tests get_portfolio_returns_by_allocation"""
    portfolio_allocations = dtt.get_expected_portfolio_allocations()
    returns = dtt.get_expected_specific_returns()
    actual_portfolio_returns_by_allocation = pf.get_portfolio_returns_by_allocation(
        portfolio_allocations, returns)

    assert len(actual_portfolio_returns_by_allocation) == len(portfolio_allocations)

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
    """tests get_expected_inflation_rates raises TypeError when passed incorrect type"""
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


def test_get_portfolio_value_by_startyear_by_allocation():
    """tests get_portfolio_value_by_startyear_by_allocation"""
    portfolio_allocations = dtt.get_expected_portfolio_allocations()
    returns = dtt.get_expected_specific_returns()
    portfolio_returns_by_allocation = pf.get_portfolio_returns_by_allocation(portfolio_allocations, returns)

    actual_portfolio_value_by_startyear_by_allocation = pf.get_portfolio_value_by_startyear_by_allocation(portfolio_returns_by_allocation, dtt.MY_TIMEFRAME)
    assert len(actual_portfolio_value_by_startyear_by_allocation) == len(portfolio_allocations)

    actual_portfolio_value_by_startyear = actual_portfolio_value_by_startyear_by_allocation[dtt.MY_ALLOCATION]
    
    expected = dtt.get_expected_portfolio_value_by_startyear()
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


def test_get_portfolio_timeframe_by_startyear_by_allocation():
    """tests get_portfolio_value_by_startyear_by_allocation"""
    portfolio_allocations = dtt.get_expected_portfolio_allocations()
    returns = dtt.get_expected_specific_returns()
    portfolio_returns_by_allocation = pf.get_portfolio_returns_by_allocation(portfolio_allocations, returns)

    actual_portfolio_timeframe_by_startyear_by_allocation = pf.get_portfolio_timeframe_by_startyear_by_allocation(portfolio_returns_by_allocation, dtt.MY_DEFAULT_TARGET)
    assert len(actual_portfolio_timeframe_by_startyear_by_allocation) == len(portfolio_allocations)

    actual_portfolio_timeframe_by_startyear = actual_portfolio_timeframe_by_startyear_by_allocation[dtt.MY_ALLOCATION]
    
    expected = dtt.get_expected_portfolio_timeframe_by_startyear()
    assert_series_equal(actual_portfolio_timeframe_by_startyear, expected)


def test_get_default_statistics_for_portfolio_values():
    """tests get_statistics_for_portfolio_values with default statistics"""
    portfolio_values = dtt.get_expected_portfolio_value_by_startyear()
    actual_portfolio_stats = pf.get_statistics(portfolio_values)

    expected = dtt.get_expected_default_statistics_for_portfolio_values()
    assert_series_equal(actual_portfolio_stats, expected)


def test_get_statistics_for_portfolio_values_with_custom_statistics():
    """tests get_statistics_for_portfolio_values with custom statistics"""
    portfolio_values = dtt.get_expected_portfolio_value_by_startyear()
    actual_portfolio_stats = pf.get_statistics(portfolio_values, dtt.CUSTOM_STATISTICS)

    expected = dtt.get_expected_custom_statistics_for_portfolio_values()
    assert_series_equal(actual_portfolio_stats, expected)

#TODO test getting just getting gmean to ensure only 1 row returned
def test_get_statistic_for_gmean_returns_one_result():
    values = dtt.pd.Series([1,2,3,4])
    stats = pf.get_statistics(values, [gmean])
    assert stats.size == 1


def test_get_default_statistics_for_portfolio_timeframes():
    """tests get_statistics with portfolio_timeframes and default statistics"""
    portfolio_timeframes = dtt.get_expected_portfolio_timeframe_by_startyear()
    actual_portfolio_stats = pf.get_statistics(portfolio_timeframes)

    expected = dtt.get_expected_default_statistics_for_portfolio_timeframes()
    assert_series_equal(actual_portfolio_stats, expected)


def test_get_statistics_for_portfolio_timeframes_with_custom_statistics():
    """tests get_statistics with portfolio_timeframes and custom statistics"""
    portfolio_timeframes = dtt.get_expected_portfolio_timeframe_by_startyear()
    actual_portfolio_stats = pf.get_statistics(portfolio_timeframes, dtt.CUSTOM_STATISTICS)

    expected = dtt.get_expected_custom_statistics_for_portfolio_timeframes()
    assert_series_equal(actual_portfolio_stats, expected)


def test_get_statistics_by_allocation():
    """tests get_statistics_by_allocation"""
    portfolio_allocations = dtt.get_expected_portfolio_allocations()
    returns = dtt.get_expected_specific_returns()
    portfolio_returns_by_allocation = pf.get_portfolio_returns_by_allocation(portfolio_allocations, returns)
    portfolio_timeframe_by_startyear_by_allocation = pf.get_portfolio_timeframe_by_startyear_by_allocation(portfolio_returns_by_allocation, dtt.MY_DEFAULT_TARGET)
    
    actual_statistics_by_allocation = pf.get_statistics_by_allocation(portfolio_timeframe_by_startyear_by_allocation)
    
    assert len(actual_statistics_by_allocation) == len(portfolio_allocations)

    actual_portfolio_stats = actual_statistics_by_allocation[dtt.MY_ALLOCATION]
    
    expected = dtt.get_expected_default_statistics_for_portfolio_timeframes()
    assert_series_equal(actual_portfolio_stats, expected)

def test_convert_to_dataframe_by_allocation():
    allocation1 = dtt.PortfolioAllocation(0, 1, 0)
    allocation2 = dtt.PortfolioAllocation(1, 0, 0)
    series_dict_by_allocation = {allocation1: pd.Series([1]), allocation2: pd.Series(['a'])}
    
    actual_dataframe_by_allocation = pf.convert_to_dataframe_by_allocation(series_dict_by_allocation)

    assert actual_dataframe_by_allocation.loc[allocation1].loc[0] == 1
    assert actual_dataframe_by_allocation.loc[allocation2].loc[0] == 'a'



#pd.concat([row1_series,row2_series], axis=1).T

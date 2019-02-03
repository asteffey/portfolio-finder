import pytest

import portfoliofinder as pf
import data_to_test as dtt
from pandas.util.testing import assert_frame_equal

def test_fetch_all_returns_from_csv():
    returns = pf.fetch_all_returns_from_csv("tests/test_data.csv")
    expected_returns = dtt.get_expected_all_returns()
    assert_frame_equal(returns, expected_returns)

def test_get_specific_returns():
    all_returns = dtt.get_expected_all_returns()
    specific_returns = pf.get_specific_returns(all_returns, dtt.SPECIFIC_FUNDS)
    expected_specific_returns = dtt.get_expected_specific_returns()
    assert_frame_equal(specific_returns, expected_specific_returns)

def test_create_portfolio_allocations():
    expected_allocations = dtt.get_expected_portfolio_allocation()
    allocations = pf.create_portfolio_allocations(dtt.SPECIFIC_FUNDS, 0.25)
    assert sorted(allocations) == sorted(expected_allocations)

def test_get_portfolio_returns ():
    expected_portfolio_returns = dtt.get_expected_portfolio_returns()
    portfolio_allocation = dtt.get_expected_portfolio_allocation()
    portfolio_returns = pf.get_portfolio_returns (portfolio_allocation, dtt.SPECIFIC_FUNDS)
    assert_frame_equal(portfolio_returns, expected_portfolio_returns)

    
#TODO test get_inflation_adjusted_returns (returns, inflation_rates)
def test_get_inflation_adjusted_returns():
    expected_inflation_adjusted_returns = dtt.get_expected_inflation_adjusted_returns()
    specific_returns = dtt.get_expected_specific_returns()
    inflation_rates = pf.get_specific_returns(dtt.get_expected_all_returns(), ['USA_INF'])
    inflation_adjusted_returns = pf.get_inflation_adjusted_returns(specific_returns, )
    assert_frame_equal(inflation_adjusted_returns, expected_inflation_adjusted_returns)
    
#TODO test get_portfolio_value_by_startyear
    
#TODO test get_portfolio_timeframe_by_startyear

#TODO test get_statistics_for_portfolio(portfolio_timeframe_by_startyear, statistic_list)

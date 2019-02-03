import pytest

import portfoliofinder as pf
import data_to_test as dtt

def test_fetch_all_returns_from_csv():
    returns = pf.fetch_all_returns_from_csv("tests/test_data.csv")
    assert all(returns.axes[1].array == dtt.ALL_FUNDS)
    are_valid_returns(returns)

def test_get_specific_returns():
    all_returns = pf.fetch_all_returns_from_csv("tests/test_data.csv")
    returns = pf.get_specific_returns(all_returns, dtt.SPECIFIC_FUNDS)
    assert all(returns.axes[1].array == dtt.SPECIFIC_FUNDS)
    are_valid_returns(returns)

def are_valid_returns(returns):
    assert all(returns.axes[0].array == list(range(1970,2018)))
    assert returns['USA_TSM'][1970] == pytest.approx(0.009)
    assert returns['USA_TSM'][1973] == pytest.approx(-0.177)
    assert returns['GLD'].sum() == pytest.approx(5.13)

def test_create_portfolio_allocations():
    expected_allocations = dtt.get_expected_portfolio_allocation()
    expected_allocations.sort()

    allocations = pf.create_portfolio_allocations(dtt.SPECIFIC_FUNDS, 0.25)
    allocations.sort()

    assert allocations == expected_allocations

def test_get_portfolio_returns ():
    portfolio_allocation = pf.create_portfolio_allocations(dtt.SPECIFIC_FUNDS, 0.25)
    pf.get_portfolio_returns (portfolio_allocation, dtt.SPECIFIC_FUNDS)

    
#TODO test get_inflation_adjusted_returns (returns, inflation_rates)
    
#TODO test get_portfolio_value_by_startyear
    
#TODO test get_portfolio_timeframe_by_startyear

#TODO test get_statistics_for_portfolio(portfolio_timeframe_by_startyear, statistic_list)

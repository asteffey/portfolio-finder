import pytest

import portfoliofinder as pf

def test_fetch_all_returns_from_csv():
    returns = pf.fetch_all_returns_from_csv("tests/test_data.csv")
    assert all(returns.axes[0].array == list(range(1970,2018)))
    assert all(returns.axes[1].array == ['USA_TSM', 'GLD', 'EM', 'USA_INF', 'RISK_FREE'])
    assert returns['USA_TSM'][1970] == pytest.approx(0.009)
    assert returns['USA_TSM'][1973] == pytest.approx(-0.177)
    assert returns['GLD'].sum() == pytest.approx(5.13)

def test_get_specific_returns(returns, symbols):
    all_returns = pf.fetch_all_returns_from_csv("tests/test_data.csv")
    returns = pf.get_specific_returns(all_returns, ['USA_TSM', 'GLD', 'EM'])
    assert all(returns.axes[0].array == list(range(1970,2018)))
    assert all(returns.axes[1].array == ['USA_TSM', 'GLD', 'EM'])
    assert returns['USA_TSM'][1970] == pytest.approx(0.009)
    assert returns['USA_TSM'][1973] == pytest.approx(-0.177)
    assert returns['GLD'].sum() == pytest.approx(5.13)

#TODO get_portfolio_returns (portfolio_allocation, fund_returns)
    
#TODO get_inflation_adjusted_returns (returns, inflation_rates)
    
#TODO get_portfolio_value_by_startyear
    
#TODO get_portfolio_timeframe_by_startyear

#TODO get_statistics_for_portfolio(portfolio_timeframe_by_startyear, statistic_list)

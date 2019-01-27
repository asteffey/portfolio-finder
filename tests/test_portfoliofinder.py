import pytest

import portfoliofinder as pf
from collections import namedtuple

ALL_FUNDS = ['USA_TSM', 'GLD', 'EM', 'USA_INF', 'RISK_FREE']
SPECIFIC_FUNDS = ['USA_TSM', 'GLD', 'EM']

def test_fetch_all_returns_from_csv():
    returns = pf.fetch_all_returns_from_csv("tests/test_data.csv")
    assert all(returns.axes[0].array == list(range(1970,2018)))
    assert all(returns.axes[1].array == ALL_FUNDS)
    assert returns['USA_TSM'][1970] == pytest.approx(0.009)
    assert returns['USA_TSM'][1973] == pytest.approx(-0.177)
    assert returns['GLD'].sum() == pytest.approx(5.13)

def test_get_specific_returns():
    all_returns = pf.fetch_all_returns_from_csv("tests/test_data.csv")
    returns = pf.get_specific_returns(all_returns, SPECIFIC_FUNDS)
    assert all(returns.axes[0].array == list(range(1970,2018)))
    assert all(returns.axes[1].array == SPECIFIC_FUNDS)
    assert returns['USA_TSM'][1970] == pytest.approx(0.009)
    assert returns['USA_TSM'][1973] == pytest.approx(-0.177)
    assert returns['GLD'].sum() == pytest.approx(5.13)

def test_create_portfolio_allocations():
    PortfolioAllocation = namedtuple('PortfolioAllocation', SPECIFIC_FUNDS)
    expected_allocations = [PortfolioAllocation(0, 1, 0),
                            PortfolioAllocation(0, 0.75, 0.25),
                            PortfolioAllocation(0, 0.5, 0.5),
                            PortfolioAllocation(0, 0.25, 0.75),
                            PortfolioAllocation(0, 0, 1),
                            PortfolioAllocation(0.25, 0.75, 0),
                            PortfolioAllocation(0.25, 0.5, 0.25),
                            PortfolioAllocation(0.25, 0.25, 0.5),
                            PortfolioAllocation(0.25, 0, 0.75),
                            PortfolioAllocation(0.5, 0.5, 0),
                            PortfolioAllocation(0.5, 0.25, 0.25),
                            PortfolioAllocation(0.5, 0, 0.5),
                            PortfolioAllocation(0.75, 0.25, 0),
                            PortfolioAllocation(0.75, 0, 0.25),
                            PortfolioAllocation(1, 0, 0)]
    expected_allocations.sort()

    allocations = pf.create_portfolio_allocations(SPECIFIC_FUNDS, 0.25)
    allocations.sort()

    assert all(allocations == expected_allocations)

#TODO test get_portfolio_returns (portfolio_allocation, fund_returns)
    
#TODO test get_inflation_adjusted_returns (returns, inflation_rates)
    
#TODO test get_portfolio_value_by_startyear
    
#TODO test get_portfolio_timeframe_by_startyear

#TODO test get_statistics_for_portfolio(portfolio_timeframe_by_startyear, statistic_list)

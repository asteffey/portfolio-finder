"""
pytests for portfolio_returns module
"""

from pandas.testing import assert_series_equal

from testdata_constants import *


def test_init():
    actual_portfolio_returns = portfoliofinder.PortfolioReturns(
        EXPECTED_SPECIFIC_RETURNS, MY_ALLOCATION)
    assert_series_equal(actual_portfolio_returns.as_series(),
                        EXPECTED_PORTFOLIO_RETURNS)


def test_from_returns_by_symbol():
    returns_by_symbol = portfoliofinder.SymbolReturns(
        EXPECTED_SPECIFIC_RETURNS)
    actual_portfolio_returns = returns_by_symbol.to_portfolio_returns(
        MY_ALLOCATION)

    assert_series_equal(actual_portfolio_returns.as_series(),
                        EXPECTED_PORTFOLIO_RETURNS)

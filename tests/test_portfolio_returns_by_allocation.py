"""
pytests for portfolio_returns module
"""

from pandas.testing import assert_series_equal

import portfoliofinder as pf

from testdata_constants import *


def test_get_portfolio_returns():
    portfolio_returns_by_allocation = pf.PortfolioReturnsByAllocation(
        EXPECTED_SPECIFIC_RETURNS, pf.PortfolioAllocations(EXPECTED_PORTFOLIO_ALLOCATIONS))
    actual_portfolio_returns = portfolio_returns_by_allocation.get_series(
        MY_ALLOCATION)

    print(portfolio_returns_by_allocation.as_dataframe())

    assert_series_equal(actual_portfolio_returns, EXPECTED_PORTFOLIO_RETURNS)


def test_as_dataframe():
    portfolio_returns_by_allocation = pf.PortfolioReturnsByAllocation(
        EXPECTED_SPECIFIC_RETURNS, pf.PortfolioAllocations(EXPECTED_PORTFOLIO_ALLOCATIONS))
    actual_portfolio_returns = portfolio_returns_by_allocation.as_dataframe(
    ).loc[MY_ALLOCATION]

    expected = EXPECTED_PORTFOLIO_RETURNS.copy()
    expected.name = MY_ALLOCATION
    assert_series_equal(actual_portfolio_returns, expected)


def test_from_returns_by_symbol():
    specific_returns = pf.SymbolReturns(EXPECTED_SPECIFIC_RETURNS)
    actual_portfolio_returns_by_allocation = specific_returns.to_portfolio_returns_by_allocation(
        pf.PortfolioAllocations(EXPECTED_PORTFOLIO_ALLOCATIONS))

    actual_portfolio_returns = actual_portfolio_returns_by_allocation.get_series(
        MY_ALLOCATION)

    assert_series_equal(actual_portfolio_returns, EXPECTED_PORTFOLIO_RETURNS)

"""
pytests for portfolio_returns module
"""

import pytest
from pandas.util.testing import assert_frame_equal
from pandas.util.testing import assert_series_equal

import portfoliofinder as pf

from testdata_constants import *

def test_get_portfolio_returns():
    actual_portfolio_returns = DEFAULT_PORTFOLIO_RETURNS_BY_ALLOCATION.get_series(MY_ALLOCATION)

    assert_series_equal(actual_portfolio_returns, EXPECTED_PORTFOLIO_RETURNS)

def test_to_dataframe():
    actual_portfolio_returns = DEFAULT_PORTFOLIO_RETURNS_BY_ALLOCATION.to_dataframe().loc[MY_ALLOCATION]
    
    expected = EXPECTED_PORTFOLIO_RETURNS.copy()
    expected.name = MY_ALLOCATION
    assert_series_equal(actual_portfolio_returns, expected)


def test_from_returns_by_symbol():
    specific_returns = pf.ReturnsBySymbol(EXPECTED_SPECIFIC_RETURNS)
    actual_portfolio_returns_by_allocation = specific_returns.to_portfolio_returns_by_allocation(EXPECTED_PORTFOLIO_ALLOCATIONS)

    actual_portfolio_returns = actual_portfolio_returns_by_allocation.get_series(MY_ALLOCATION)

    assert_series_equal(actual_portfolio_returns, EXPECTED_PORTFOLIO_RETURNS)
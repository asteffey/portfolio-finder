"""
pytests for portfolio_returns module
"""

import pytest
from pandas.util.testing import assert_frame_equal
from pandas.util.testing import assert_series_equal
from collections import namedtuple

import portfoliofinder as pf

from testdata_reader import read_dataframe, read_dataframe_raw, read_series
from test_returns_by_symbol import SPECIFIC_FUNDS, DEFAULT_SPECIFIC_RETURNS_BY_SYMBOL

PortfolioAllocation = namedtuple('PortfolioAllocation', SPECIFIC_FUNDS)
MY_ALLOCATION = PortfolioAllocation(0, 0.75, 0.25)

EXPECTED_SPECIFIC_RETURNS = read_dataframe('specific_returns')
EXPECTED_PORTFOLIO_RETURNS = read_series('portfolio_returns')

DEFAULT_PORTFOLIO_RETURNS = pf.PortfolioReturns(EXPECTED_SPECIFIC_RETURNS, MY_ALLOCATION)

def test_init():
    assert_series_equal(DEFAULT_PORTFOLIO_RETURNS.to_series(), EXPECTED_PORTFOLIO_RETURNS)

def test_from_returns_by_symbol():
    actual_portfolio_returns = DEFAULT_SPECIFIC_RETURNS_BY_SYMBOL.to_portfolio_returns(MY_ALLOCATION)

    assert_series_equal(actual_portfolio_returns.to_series(), EXPECTED_PORTFOLIO_RETURNS)
"""
pytests for portfolio_returns module
"""

import pytest
from pandas.util.testing import assert_frame_equal
from pandas.util.testing import assert_series_equal

import portfoliofinder as pf

from data_to_test import read_dataframe
from data_to_test import read_series
from data_to_test import SPECIFIC_FUNDS, MY_ALLOCATION, EXPECTED_SPECIFIC_RETURNS, EXPECTED_PORTFOLIO_RETURNS


def test_init():
    actual_portfolio_returns = pf.PortfolioReturns(EXPECTED_SPECIFIC_RETURNS, MY_ALLOCATION)

    assert_series_equal(actual_portfolio_returns.to_series(), EXPECTED_PORTFOLIO_RETURNS)

def test_from_returns_by_symbol():
    specific_returns = pf.ReturnsBySymbol(EXPECTED_SPECIFIC_RETURNS)
    actual_portfolio_returns = specific_returns.to_portfolio_returns(MY_ALLOCATION)

    assert_series_equal(actual_portfolio_returns.to_series(), EXPECTED_PORTFOLIO_RETURNS)
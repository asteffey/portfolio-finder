"""
pytests for portfolio_returns module
"""

import pytest
from pandas.util.testing import assert_frame_equal
from pandas.util.testing import assert_series_equal

import portfoliofinder as pf

from data_to_test import read_dataframe
from data_to_test import read_series
from data_to_test import SPECIFIC_FUNDS, MY_ALLOCATION

EXPECTED_SPECIFIC_RETURNS = read_dataframe('specific_returns')
EXPECTED_PORTFOLIO_RETURNS = read_series('portfolio_returns')


def test_init():
    specific_returns = pf.ReturnsBySymbol(EXPECTED_SPECIFIC_RETURNS)
    actual_portfolio_returns = pf.PortfolioReturns(specific_returns, MY_ALLOCATION)

    assert_series_equal(actual_portfolio_returns.to_series(), EXPECTED_PORTFOLIO_RETURNS)

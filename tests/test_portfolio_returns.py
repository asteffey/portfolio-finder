"""
pytests for portfolio_returns module
"""

import pytest
from pandas.util.testing import assert_frame_equal
from pandas.util.testing import assert_series_equal
from collections import namedtuple

import portfoliofinder as pf

from testdata_constants import *

def test_init():
    assert_series_equal(DEFAULT_PORTFOLIO_RETURNS.to_series(), EXPECTED_PORTFOLIO_RETURNS)

def test_from_returns_by_symbol():
    actual_portfolio_returns = DEFAULT_SPECIFIC_RETURNS_BY_SYMBOL.to_portfolio_returns(MY_ALLOCATION)

    assert_series_equal(actual_portfolio_returns.to_series(), EXPECTED_PORTFOLIO_RETURNS)
from collections import namedtuple

import portfoliofinder as pf
from test_returns_by_symbol import SPECIFIC_FUNDS
from test_portfolio_returns_by_allocation import EXPECTED_PORTFOLIO_ALLOCATIONS

def test_create_portfolio_allocations():
    """tests create_portfolio_allocations"""
    actual_allocations = pf.create_portfolio_allocations(
        0.25, SPECIFIC_FUNDS)

    assert sorted(actual_allocations) == sorted(EXPECTED_PORTFOLIO_ALLOCATIONS)
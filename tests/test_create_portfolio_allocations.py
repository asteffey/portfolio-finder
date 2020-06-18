"""
pytests for PortfolioAllocations
"""

import portfoliofinder as pf
from testdata_constants import SPECIFIC_FUNDS
from test_portfolio_returns_by_allocation import EXPECTED_PORTFOLIO_ALLOCATIONS
from pandas.testing import assert_frame_equal


def test_create_portfolio_allocations():
    """tests PortfolioAllocations"""
    actual_allocations = pf.Allocations(0.25, SPECIFIC_FUNDS)

    assert_frame_equal(EXPECTED_PORTFOLIO_ALLOCATIONS, actual_allocations.as_dataframe())

from collections import namedtuple

import portfoliofinder as pf
from data_to_test import read_dataframe_raw
from data_to_test import SPECIFIC_FUNDS, PortfolioAllocation

EXPECTED_PORTFOLIO_ALLOCATIONS_DF = read_dataframe_raw('portfolio_allocation')
EXPECTED_PORTFOLIO_ALLOCATIONS = [PortfolioAllocation(*row[1:]) for row in EXPECTED_PORTFOLIO_ALLOCATIONS_DF.itertuples()]


def test_create_portfolio_allocations():
    """tests create_portfolio_allocations"""
    actual_allocations = pf.create_portfolio_allocations(
        0.25, SPECIFIC_FUNDS)

    assert sorted(actual_allocations) == sorted(EXPECTED_PORTFOLIO_ALLOCATIONS)
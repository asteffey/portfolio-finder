from pandas.testing import assert_series_equal
import portfoliofinder as pf
from testdata_constants import *


def test_get_with_default_from_portfolio_value_by_startyear_by_allocation():
    """tests get_statistics_by_allocation"""
    portfolio_returns_by_allocation = portfoliofinder.PortfolioReturnsByAllocation(EXPECTED_SPECIFIC_RETURNS,
                                                                                   pf.PortfolioAllocations(EXPECTED_PORTFOLIO_ALLOCATIONS))
    portfolio_value_by_startyear_by_allocation = portfolio_returns_by_allocation.to_portfolio_value_by_startyear_by_allocation(
        MY_TIMEFRAME)

    actual_statistics_by_allocation = portfolio_value_by_startyear_by_allocation.get_statistics().as_dataframe()

    assert len(actual_statistics_by_allocation) == len(
        portfolio_returns_by_allocation.as_dataframe())

    actual_portfolio_stats = actual_statistics_by_allocation.loc[MY_ALLOCATION]
    actual_portfolio_stats.name = "Portfolio Value"
    assert_series_equal(actual_portfolio_stats,
                        EXPECTED_DEFAULT_STATISTICS_FOR_PORTFOLIO_VALUES)


def test_get_with_custom_from_portfolio_value_by_startyear_by_allocation():
    """tests get_statistics_by_allocation"""
    portfolio_returns_by_allocation = portfoliofinder.PortfolioReturnsByAllocation(EXPECTED_SPECIFIC_RETURNS,
                                                                                   pf.PortfolioAllocations(EXPECTED_PORTFOLIO_ALLOCATIONS))
    portfolio_value_by_startyear_by_allocation = portfolio_returns_by_allocation.to_portfolio_value_by_startyear_by_allocation(
        MY_TIMEFRAME)

    actual_statistics_by_allocation = portfolio_value_by_startyear_by_allocation.get_statistics(
        MY_CUSTOM_STATISTICS).as_dataframe()

    assert len(actual_statistics_by_allocation) == len(
        portfolio_returns_by_allocation.as_dataframe())

    actual_portfolio_stats = actual_statistics_by_allocation.loc[MY_ALLOCATION]
    actual_portfolio_stats.name = "Portfolio Value"
    assert_series_equal(actual_portfolio_stats,
                        EXPECTED_DEFAULT_STATISTICS_FOR_PORTFOLIO_VALUES_WITH_CUSTOM_STATS)

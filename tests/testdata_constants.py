"""Test Constants."""

from collections import namedtuple

import portfoliofinder
from portfoliofinder.contributions import InitialContribution
import testdata_reader as tdr

SPECIFIC_FUNDS = ['USA_TSM', 'GLD', 'EM']
MY_TIMEFRAME = 10
PortfolioAllocation = namedtuple('PortfolioAllocation', SPECIFIC_FUNDS)
MY_ALLOCATION = PortfolioAllocation(0, 0.75, 0.25)
SINGLE_CONTRIBUTION = InitialContribution(1)

MY_SCHEDULED_CONTRIBUTIONS = portfoliofinder.ScheduledContributions(
    {n: (1000 if n in (0, 5) else 10) for n in range(0, 100)})

MY_DEFAULT_TARGET = 4
MY_TARGET_WITH_CONTRIBUTIONS = 10000

MY_CUSTOM_STATISTICS = ['min', portfoliofinder.stats.percentile_for(
    10), portfoliofinder.stats.gmean]

EXPECTED_ALL_RETURNS = tdr.read_dataframe('all_returns', index_col=0)
EXPECTED_SPECIFIC_RETURNS = tdr.read_dataframe('specific_returns', index_col=0)
EXPECTED_INFLATION_ADJUSTED_SPECIFIC_RETURNS = tdr.read_dataframe('inflation_adjusted_specific_returns', index_col=0)

EXPECTED_PORTFOLIO_RETURNS = tdr.read_series('portfolio_returns')

EXPECTED_PORTFOLIO_ALLOCATIONS = tdr.read_dataframe('portfolio_allocation')

EXPECTED_PORTFOLIO_TIMEFRAME_BY_STARTYEAR = tdr.read_series(
    'portfolio_timeframe_by_startyear', usecols=['Year', 'Portfolio Timeframe']).dropna()
EXPECTED_PORTFOLIO_TIMEFRAME_BY_STARTYEAR_WITH_CONTRIBUTIONS = tdr.read_series(
    'portfolio_timeframe_by_startyear_with_contributions',
    usecols=['Year', 'Portfolio Timeframe']).dropna()

EXPECTED_PORTFOLIO_VALUE_BY_STARTYEAR = tdr.read_series(
    'portfolio_value_by_startyear', usecols=['Year', 'Portfolio Value'])
EXPECTED_PORTFOLIO_VALUE_BY_STARTYEAR_WITH_CONTRIBUTIONS = tdr.read_series(
    'portfolio_value_by_startyear_with_contributions', usecols=['Year', 'Portfolio Value'])

EXPECTED_DEFAULT_STATISTICS_FOR_PORTFOLIO_TIMEFRAMES = tdr.read_series(
    'default_statistics_for_timeframe', usecols=['Statistic', 'Portfolio Timeframe'])
EXPECTED_DEFAULT_STATISTICS_FOR_PORTFOLIO_TIMEFRAMES_WITH_CUSTOM_STATS = tdr.read_series(
    'custom_statistics_for_timeframe', usecols=['Statistic', 'Portfolio Timeframe'])

EXPECTED_DEFAULT_STATISTICS_FOR_PORTFOLIO_VALUES = tdr.read_series(
    'default_statistics_for_value', usecols=['Statistic', 'Portfolio Value'])
EXPECTED_DEFAULT_STATISTICS_FOR_PORTFOLIO_VALUES_WITH_CUSTOM_STATS = tdr.read_series(
    'custom_statistics_for_value', usecols=['Statistic', 'Portfolio Value'])

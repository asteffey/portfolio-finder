import portfoliofinder

from collections import namedtuple
import testdata_reader as tdr

SPECIFIC_FUNDS = ['USA_TSM', 'GLD', 'EM']
MY_TIMEFRAME = 10
PortfolioAllocation = namedtuple('PortfolioAllocation', SPECIFIC_FUNDS)
MY_ALLOCATION = PortfolioAllocation(0, 0.75, 0.25)

MY_SCHEDULED_CONTRIBUTIONS = portfoliofinder.contributions.ScheduledContributions(
    {n: (1000 if n in (0, 5) else 10) for n in range(0, 100)})

MY_DEFAULT_TARGET = 4
MY_TARGET_WITH_CONTRIBUTIONS = 10000

CUSTOM_STATISTICS = ['min',portfoliofinder.stats.percentile_for(10),portfoliofinder.stats.gmean]

EXPECTED_ALL_RETURNS = tdr.read_dataframe('all_returns')
EXPECTED_SPECIFIC_RETURNS = tdr.read_dataframe('specific_returns')
EXPECTED_INFLATION_RATES = tdr.read_series('inflation_rates')
EXPECTED_INFLATION_ADJUSTED_SPECIFIC_RETURNS = tdr.read_dataframe('inflation_adjusted_specific_returns')

EXPECTED_PORTFOLIO_RETURNS = tdr.read_series('portfolio_returns')

DEFAULT_SPECIFIC_RETURNS_BY_SYMBOL = portfoliofinder.ReturnsBySymbol(EXPECTED_SPECIFIC_RETURNS)
DEFAULT_PORTFOLIO_RETURNS = portfoliofinder.PortfolioReturns(EXPECTED_SPECIFIC_RETURNS, MY_ALLOCATION)

EXPECTED_PORTFOLIO_ALLOCATIONS = [PortfolioAllocation(*row[1:]) for row in tdr.read_dataframe_raw('portfolio_allocation').itertuples()]
DEFAULT_PORTFOLIO_RETURNS_BY_ALLOCATION = portfoliofinder.PortfolioReturnsByAllocation(EXPECTED_SPECIFIC_RETURNS, EXPECTED_PORTFOLIO_ALLOCATIONS)

EXPECTED_PORTFOLIO_TIMEFRAME_BY_STARTYEAR = tdr.read_series('portfolio_timeframe_by_startyear', usecols=['Year', 'Portfolio Timeframe']).dropna()
EXPECTED_PORTFOLIO_TIMEFRAME_BY_STARTYEAR_WITH_CONTRIBUTIONS = tdr.read_series('portfolio_timeframe_by_startyear_with_contributions', usecols=['Year', 'Portfolio Timeframe']).dropna()

EXPECTED_PORTFOLIO_VALUE_BY_STARTYEAR = tdr.read_series('portfolio_value_by_startyear', usecols=['Year', 'Portfolio Value'])
EXPECTED_PORTFOLIO_VALUE_BY_STARTYEAR_WITH_CONTRIBUTIONS = tdr.read_series('portfolio_value_by_startyear_with_contributions', usecols=['Year', 'Portfolio Value'])

EXPECTED_DEFAULT_STATISTICS_FOR_PORTFOLIO_TIMEFRAMES = tdr.read_series('default_statistics_for_timeframe', usecols=['Statistic', 'Portfolio Timeframe'])
EXPECTED_DEFAULT_STATISTICS_FOR_PORTFOLIO_TIMEFRAMES_WITH_CUSTOM_STATS = tdr.read_series('custom_statistics_for_timeframe', usecols=['Statistic', 'Portfolio Timeframe'])

EXPECTED_DEFAULT_STATISTICS_FOR_PORTFOLIO_VALUES = tdr.read_series('default_statistics_for_value', usecols=['Statistic', 'Portfolio Value'])
EXPECTED_DEFAULT_STATISTICS_FOR_PORTFOLIO_VALUES_WITH_CUSTOM_STATS = tdr.read_series('custom_statistics_for_value', usecols=['Statistic', 'Portfolio Value'])
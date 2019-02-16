"""
Contains test inputs and expected values used throughout pytests
"""

"""
thought: this module violates SRP
every time I add a test, I have to update both test_portfoliofinder and this

TODO: create a seperate data reader class
TODO: reorganize test_portfoliofinder and this class into seperate tests for each function
"""

from collections import namedtuple
import pandas as pd
from portfoliofinder.contributions import ScheduledContributions

ALL_FUNDS = ['USA_TSM', 'GLD', 'EM', 'USA_INF', 'RISK_FREE']

SPECIFIC_FUNDS = ['USA_TSM', 'GLD', 'EM']

PortfolioAllocation = namedtuple('PortfolioAllocation', SPECIFIC_FUNDS)

MY_ALLOCATION = PortfolioAllocation(0, 0.75, 0.25)

MY_TIMEFRAME = 10

MY_DEFAULT_TARGET = 4

MY_SCHEDULED_CONTRIBUTIONS = ScheduledContributions(
    {n: (1000 if n in (0, 5) else 10) for n in range(0, 100)})

MY_TARGET_WITH_CONTRIBUTIONS = 10000

_TEST_DATA_PATH = "tests/test_results.xlsx"


def get_expected_all_returns():
    """returns expected_all_returns read from excel file"""

    return pd.read_excel(_TEST_DATA_PATH,
                         "all_returns",
                         index_col=0)


def get_expected_specific_returns():
    """returns expected_specific_returns read from excel file"""
    return pd.read_excel(_TEST_DATA_PATH,
                         "specific_returns",
                         index_col=0)


def get_expected_inflation_rates():
    """returns expected_inflation_rates read from excel file"""
    return pd.read_excel(_TEST_DATA_PATH,
                         "inflation_rates",
                         index_col=0)


def get_expected_inflation_adjusted_returns():
    """returns expected_inflation_adjusted_returns read from excel file"""
    return pd.read_excel(_TEST_DATA_PATH,
                         "inflation_adjusted_returns",
                         index_col=0)


def get_expected_portfolio_allocations():
    """returns expected_portfolio_allocation read from excel file"""
    dataframe = pd.read_excel(_TEST_DATA_PATH,
                              "portfolio_allocation",
                              header=None)
    return [PortfolioAllocation(*row[1:]) for row in dataframe.itertuples()]


def get_expected_portfolio_returns():
    """returns expected_portfolio_returns read from excel file"""
    return pd.read_excel(_TEST_DATA_PATH,
                         "portfolio_returns",
                         index_col=0,
                         squeeze=True)


def get_expected_portfolio_value_by_startyear():
    """returns expected_portfolio_value_by_startyear read from excel file"""
    return pd.read_excel(_TEST_DATA_PATH,
                         "portfolio_value_by_startyear",
                         index_col='Year',
                         usecols=['Year', 'Value'])


def get_expected_portfolio_value_by_startyear_with_contributions():
    """returns expected_portfolio_value_by_startyear_with_contributions read from excel file"""
    return pd.read_excel(_TEST_DATA_PATH,
                         "portfolio_value_by_startyear_with_contributions",
                         index_col='Year',
                         usecols=['Year', 'Value'])


def get_expected_portfolio_timeframe_by_startyear():
    """returns expected_portfolio_timeframe_by_startyear read from excel file"""
    dataframe = pd.read_excel(_TEST_DATA_PATH,
                              "portfolio_timeframe_by_startyear",
                              index_col='Year',
                              usecols=['Year', 'Timeframe'])
    return dataframe.dropna()


def get_expected_portfolio_timeframe_by_startyear_with_contributions():
    """returns expected_portfolio_timeframe_by_startyear_with_contributions read from excel file"""
    dataframe = pd.read_excel(_TEST_DATA_PATH,
                              "portfolio_timeframe_by_startyear_with_contributions",
                              index_col='Year',
                              usecols=['Year', 'Timeframe'])
    return dataframe.dropna()

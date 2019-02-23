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
import numpy as np
from portfoliofinder.contributions import ScheduledContributions
from typing import List

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


def get_expected_all_returns() -> pd.DataFrame:
    """returns expected_all_returns read from excel file"""

    return pd.read_excel(_TEST_DATA_PATH,
                         "all_returns",
                         index_col=0)


def get_expected_specific_returns() -> pd.DataFrame:
    """returns expected_specific_returns read from excel file"""
    return pd.read_excel(_TEST_DATA_PATH,
                         "specific_returns",
                         index_col=0)


def get_expected_inflation_rates() -> pd.Series:
    """returns expected_inflation_rates read from excel file"""
    return pd.read_excel(_TEST_DATA_PATH,
                         "inflation_rates",
                         index_col=0,
                         squeeze=True)


def get_expected_inflation_adjusted_specific_returns() -> pd.DataFrame:
    """returns expected_inflation_adjusted_specific_returns read from excel file"""
    return pd.read_excel(_TEST_DATA_PATH,
                         "inflation_adjusted_specific_returns",
                         index_col=0)


def get_expected_inflation_adjusted_portfolio_returns() -> pd.Series:
    """returns inflation_adjusted_portfolio_returns read from excel file"""
    return pd.read_excel(_TEST_DATA_PATH,
                         "inflation_adjusted_portfolio_returns",
                         index_col=0,
                         squeeze=True)


def get_expected_portfolio_allocations() -> List[PortfolioAllocation]:
    """returns expected_portfolio_allocation read from excel file"""
    dataframe = pd.read_excel(_TEST_DATA_PATH,
                              "portfolio_allocation",
                              header=None)
    return [PortfolioAllocation(*row[1:]) for row in dataframe.itertuples()]


def get_expected_portfolio_returns() -> pd.Series:
    """returns expected_portfolio_returns read from excel file"""
    return pd.read_excel(_TEST_DATA_PATH,
                         "portfolio_returns",
                         index_col=0,
                         squeeze=True)


def get_expected_portfolio_value_by_startyear() -> pd.Series:
    """returns expected_portfolio_value_by_startyear read from excel file"""
    return pd.read_excel(_TEST_DATA_PATH,
                         "portfolio_value_by_startyear",
                         index_col='Year',
                         usecols=['Year', 'Portfolio Value'],
                         squeeze=True)

#pd.read_excel(dtt._TEST_DATA_PATH, "portfolio_value_by_startyear", index_col='Year', usecols='Value', squeeze=True)

def get_expected_portfolio_value_by_startyear_with_contributions() -> pd.Series:
    """returns expected_portfolio_value_by_startyear_with_contributions read from excel file"""
    return pd.read_excel(_TEST_DATA_PATH,
                         "portfolio_value_by_startyear_with_contributions",
                         index_col='Year',
                         usecols=['Year', 'Portfolio Value'],
                         squeeze=True)


def get_expected_portfolio_timeframe_by_startyear() -> pd.Series:
    """returns expected_portfolio_timeframe_by_startyear read from excel file"""
    dataframe = pd.read_excel(_TEST_DATA_PATH,
                              "portfolio_timeframe_by_startyear",
                              index_col='Year',
                              usecols=['Year', 'Portfolio Timeframe'],
                              squeeze=True)
    return dataframe.dropna().astype(int)


def get_expected_portfolio_timeframe_by_startyear_with_contributions() -> pd.Series:
    """returns expected_portfolio_timeframe_by_startyear_with_contributions read from excel file"""
    dataframe = pd.read_excel(_TEST_DATA_PATH,
                              "portfolio_timeframe_by_startyear_with_contributions",
                              index_col='Year',
                              usecols=['Year', 'Portfolio Timeframe'],
                              squeeze=True)
    return dataframe.dropna().astype(int)

def get_expected_default_statistics_for_portfolio_values() -> pd.Series:
    return pd.read_excel(_TEST_DATA_PATH,
                         "default_statistics_for_value",
                         index_col='Statistic',
                         usecols=['Statistic', 'Portfolio'],
                         squeeze=True)

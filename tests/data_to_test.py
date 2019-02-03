from collections import namedtuple
import pandas as pd

ALL_FUNDS = ['USA_TSM', 'GLD', 'EM', 'USA_INF', 'RISK_FREE']
SPECIFIC_FUNDS = ['USA_TSM', 'GLD', 'EM']

PortfolioAllocation = namedtuple('PortfolioAllocation', SPECIFIC_FUNDS)

MY_ALLOCATION = PortfolioAllocation(0, 0.75, 0.25)


def get_expected_all_returns():
    return pd.read_excel("tests/test_results.xlsx","all_returns", index_col=0)

def get_expected_specific_returns():
    return pd.read_excel("tests/test_results.xlsx","specific_returns", index_col=0)

def get_expected_inflation_adjusted_returns():
    return pd.read_excel("tests/test_results.xlsx","inflation_adjusted_returns", index_col=0)

def get_expected_portfolio_allocation():
    df = pd.read_excel("tests/test_results.xlsx","portfolio_allocation", header=None)
    return [PortfolioAllocation(*row[1:]) for row in df.itertuples()]

def get_expected_portfolio_returns():
    return pd.read_excel("tests/test_results.xlsx","portfolio_returns", index_col=0)

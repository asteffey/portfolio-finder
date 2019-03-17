"""
pytests for returns_by_symbol module
"""

import pytest
from pandas.util.testing import assert_frame_equal
from pandas.util.testing import assert_series_equal
import pandas as pd

import portfoliofinder as pf

from data_to_test import read_dataframe
from data_to_test import read_series

SPECIFIC_FUNDS = ['USA_TSM', 'GLD', 'EM']

EXPECTED_ALL_RETURNS = read_dataframe('all_returns')
EXPECTED_SPECIFIC_RETURNS = read_dataframe('specific_returns')
EXPECTED_INFLATION_RATES = read_series('inflation_rates')
EXPECTED_INFLATION_ADJUSTED_SPECIFIC_RETURNS = read_dataframe('inflation_adjusted_specific_returns')

def test_init():
    df = pd.DataFrame({'a':[1],'b':[2]})
    returns_by_symbol = pf.ReturnsBySymbol(df)

    actual_df = returns_by_symbol.to_dataframe()

    assert_frame_equal(df, actual_df)

def test_from_csv():
    """tests fetch_all_returns_from_csv"""
    actual_returns = pf.ReturnsBySymbol.from_csv("tests/test_data.csv")

    assert_frame_equal(actual_returns.to_dataframe(), EXPECTED_ALL_RETURNS)


def test_get_specific_returns():
    """tests get_specific_returns"""
    all_returns = pf.ReturnsBySymbol(EXPECTED_ALL_RETURNS)

    actual_specific_returns = all_returns.filter_by_symbols(SPECIFIC_FUNDS)

    assert_frame_equal(actual_specific_returns.to_dataframe(), EXPECTED_SPECIFIC_RETURNS)

def test_adjust_for_inflation():
    """tests get_inflation_adjusted_returns"""
    specific_returns = pf.ReturnsBySymbol(EXPECTED_SPECIFIC_RETURNS)
    actual_inflation_adjusted_returns = specific_returns.adjust_for_inflation(EXPECTED_INFLATION_RATES)   

    assert_frame_equal(actual_inflation_adjusted_returns.to_dataframe(), EXPECTED_INFLATION_ADJUSTED_SPECIFIC_RETURNS)

"""
pytests for portfoliofinder module
"""

import pytest
from pandas.util.testing import assert_frame_equal
from pandas.util.testing import assert_series_equal
import pandas as pd

import portfoliofinder as pf
import data_to_test as dtt


def test_init():
    df = pd.DataFrame({'a':[1],'b':[2]})
    returns_by_symbol = pf.ReturnsBySymbol(df)

    actual_df = returns_by_symbol.to_dataframe()

    assert_frame_equal(df, actual_df)

def test_from_csv():
    """tests fetch_all_returns_from_csv"""
    actual_returns = pf.ReturnsBySymbol.from_csv("tests/test_data.csv")

    expected = dtt.get_expected_all_returns()
    assert_frame_equal(actual_returns.to_dataframe(), expected)


def test_get_specific_returns():
    """tests get_specific_returns"""
    all_returns = pf.ReturnsBySymbol(dtt.get_expected_all_returns())

    actual_specific_returns = all_returns.filter_by_symbols(dtt.SPECIFIC_FUNDS)

    expected = dtt.get_expected_specific_returns()
    assert_frame_equal(actual_specific_returns.to_dataframe(), expected)

def test_adjust_for_inflation():
    """tests get_inflation_adjusted_returns"""
    specific_returns = pf.ReturnsBySymbol(dtt.get_expected_specific_returns())
    inflation_rates = dtt.get_expected_inflation_rates()
    actual_inflation_adjusted_returns = specific_returns.adjust_for_inflation(inflation_rates)

    expected = dtt.get_expected_inflation_adjusted_specific_returns()
    assert_frame_equal(actual_inflation_adjusted_returns.to_dataframe(), expected)

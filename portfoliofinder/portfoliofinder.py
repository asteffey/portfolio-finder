import pandas as pd

from .combinatorics import named_range_of_allocations
"""
Workflow:
    - Inputs
        -- funds_csv_file OR online_source
        -- fund_symbols
        -- [if adjusting for inflation] inflation_rate_symbol OR average_inflation_rate
        -- [if using Sharpe ratio] risk_free_rate_symbol OR average_risk_free_rate
        -- allocation_step
        -- [optional] allocation_filters
        -- statistic_list
        -- timeframe OR target_value
        -- [optional] contributions_csv_file
"""


def fetch_all_returns_from_csv(csv_file):
    return pd.read_csv(csv_file, index_col=0)


def get_specific_returns(returns, symbols):
    return returns[symbols]


def create_portfolio_allocations(symbols, step):
    return list(named_range_of_allocations(step, symbols))


def get_inflation_adjusted_returns (returns, inflation_rates):
    if isinstance(returns, pd.DataFrame):
        return _get_inflation_adjusted_returns_for_dataframe(returns, inflation_rates)
    elif isinstance(returns, pd.Series):
        return _get_inflation_adjusted_returns_for_series(returns, inflation_rates)
    else:
        raise TypeError("returns must be pandas.DataFrame or pandas.Series")

def _get_inflation_adjusted_returns_for_series (returns: pd.Series, inflation_rates):
    adjusted_returns = (returns + 1) / (inflation_rates + 1) - 1
    adjusted_returns.name = returns.name
    return adjusted_returns

def _get_inflation_adjusted_returns_for_dataframe (returns: pd.DataFrame, inflation_rates):
    def adjust_for_inflation(returns):
        inflation_rate = inflation_rates[returns.name]
        return (returns + 1) / (inflation_rate + 1) - 1
    return returns.apply(adjust_for_inflation, axis=1)


def get_portfolio_returns_by_allocation(portfolio_allocations, returns):
    symbols = list(portfolio_allocations[0]._fields)
    returns_by_symbol = get_specific_returns(returns, symbols)
    
    portfolio_returns_by_allocation = {}
    for allocation in portfolio_allocations:
        portfolio_returns = _get_portfolio_returns(allocation, returns_by_symbol)
        portfolio_returns_by_allocation[allocation] = portfolio_returns
    return portfolio_returns_by_allocation

def _get_portfolio_returns(portfolio_allocation, returns_by_symbol: pd.DataFrame):
    portfolio_returns = []
    for row in returns_by_symbol.iterrows():
        return_by_symbol = row[1]
        return_for_year = sum(return_by_symbol * portfolio_allocation)
        portfolio_returns.append(return_for_year)
    years = returns_by_symbol.axes[0]
    return pd.Series(portfolio_returns, index=years, name="Portfolio Return")


#TODO get_portfolio_value_by_startyear (portfolio_returns, timeframe, contributions)

#TODO get_portfolio_timeframe_by_startyear

#TODO get_statistics_for_portfolio(portfolio_timeframe_by_startyear, statistic_list)

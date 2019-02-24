import pandas as pd
from functools import reduce

from .combinatorics import named_range_of_allocations
from .contributions import Contributions, DEFAULT_CONTRIBUTION
from .stats import DEFAULT_STATS

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
def get_portfolio_value_by_startyear(portfolio_returns, timeframe, contributions: Contributions = DEFAULT_CONTRIBUTION):
    start_years = get_start_years_for_timeframe(portfolio_returns.index, timeframe)
    
    values = []
    for start_year in start_years:
        value = get_portfolio_value_for_startyear(start_year, portfolio_returns, timeframe, contributions)
        values.append(value)
    
    return pd.Series(data=values,
                     index=pd.Index(start_years, name='Year'),
                     name="Portfolio Value")


def get_start_years_for_timeframe(years: pd.Index, timeframe):
    first_year = years[0]
    last_year = years[-1] - (timeframe - 1)
    return _inclusive_range(first_year, last_year)


def _inclusive_range(start, stop, step=1):
    return range(start, (stop + 1) if step >= 0 else (stop - 1), step)


def get_portfolio_value_for_startyear(start_year, portfolio_returns: pd.Series, timeframe, contributions: Contributions):
    investment_years = range(start_year, start_year + timeframe)
    returns_over_timeframe = portfolio_returns.loc[investment_years]

    timeframe_iter = iter(range(timeframe))
    def reduce_to_portfolio_value(prev_value, current_return):
        investment_year = next(timeframe_iter)
        contribution = contributions.get_contribution_for_year(investment_year)
        value = prev_value + contribution
        return value * (1 + current_return)
    
    return reduce(reduce_to_portfolio_value, returns_over_timeframe, 0)

def get_portfolio_timeframe_by_startyear(portfolio_returns, target_value, contributions: Contributions = DEFAULT_CONTRIBUTION):
    all_years = portfolio_returns.index
    
    timeframes = []
    start_years = []
    for start_year in all_years:
        value = 0
        investment_year = 0
        while value < target_value and start_year + investment_year <= all_years[-1]:
            contribution = contributions.get_contribution_for_year(investment_year)
            current_return = portfolio_returns.loc[start_year + investment_year]
            value = (value + contribution) * (1 + current_return)

            investment_year += 1
        
        if value >= target_value:
            timeframes.append(investment_year)
            start_years.append(start_year)
        
    
    timeframe_by_startyear = pd.Series(data=timeframes,
                                       index=pd.Index(start_years, name='Year'),
                                       name="Portfolio Timeframe")
    return timeframe_by_startyear.dropna()

#TODO get_statistics_for_portfolio(portfolio_timeframe_by_startyear, statistic_list)
def get_statistics_for_portfolio_values(portfolio_values : pd.Series, statistics = DEFAULT_STATS) -> pd.Series:
    ret = portfolio_values.agg(statistics)
    ret.name = "Portfolio"
    ret.index.name = "Statistic"
    return ret

#foo.agg([percentile(.1),percentile(.5)])
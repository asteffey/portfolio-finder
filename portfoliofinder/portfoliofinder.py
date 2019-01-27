import pandas as pd
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

def fetch_all_returns_from_csv (csv_file):
    return pd.read_csv(csv_file, index_col=0)

def get_specific_returns(returns, symbols):
    return returns[symbols]
    
#TODO get_portfolio_returns (portfolio_allocation, fund_returns)
    
#TODO get_inflation_adjusted_returns (returns, inflation_rates)
    
#TODO get_portfolio_value_by_startyear
    
#TODO get_portfolio_timeframe_by_startyear

#TODO get_statistics_for_portfolio(portfolio_timeframe_by_startyear, statistic_list)

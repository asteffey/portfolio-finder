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

#TODO fetch_all_returns_from_csv(csv_file)


#TODO get_returns (returns, symbols)
    
#TODO get_portfolio_returns (portfolio_allocation, fund_returns)
    
#TODO get_inflation_adjusted_returns (returns, inflation_rates)
    
#TODO get_portfolio_value_by_startyear
    
#TODO get_portfolio_timeframe_by_startyear

#TODO get_statistics_for_portfolio(portfolio_timeframe_by_startyear, statistic_list)

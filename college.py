import portfoliofinder as pf
import pandas as pd

pd.set_option('display.width', 300)
pd.set_option('display.max_columns', 20)

returns = pf.ReturnsBySymbol.from_csv("data.csv")
allocations = pf.create_portfolio_allocations(0.01, ['USA_TSM', 'WLDx_TSM', 'USA_INT', 'USA_REIT'])
allocations = list(filter(lambda x: x.USA_TSM>=0.25 and x.WLDx_TSM<=0.4 and x.USA_INT>=0.1 and x.USA_INT<=0.3 and x.USA_REIT<=0.15, allocations))

prba = returns.to_portfolio_returns_by_allocation(allocations)

contributions = pf.contributions.ScheduledContributions({0: 23000, 5: 23000})
pvbsba = prba.to_portfolio_value_by_startyear_by_allocation(17, contributions)

pvbsba_stats = pvbsba.get_statistics()

print(pvbsba_stats.get_allocation_which_max_statistic('mean'))

ptbsba = prba.to_portfolio_timeframe_by_startyear_by_allocation(200000, contributions)

ptbsba_stats = ptbsba.get_statistics()

print(ptbsba_stats.get_allocation_which_min_statistic('max'))

# TODO: graph results of statistics
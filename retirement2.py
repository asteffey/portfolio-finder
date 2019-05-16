import portfoliofinder as pf
import pandas as pd

pd.set_option('display.width', 300)
pd.set_option('display.max_columns', 20)

returns = pf.ReturnsBySymbol.from_csv("data.csv")
allocations = pf.create_portfolio_allocations(0.05, ['USA_TSM', 'WLDx_TSM', 'USA_INT', 'USA_REIT', 'EM', 'USA_SCB'])
allocations = list(filter(lambda x: x.USA_TSM>=0.3 and x.WLDx_TSM<=0.2 and x.USA_INT>=0.1 and x.USA_INT<=0.3 and x.USA_REIT<=0.2 and x.EM<=0.2 and x.USA_SCB<=0.3, allocations))

prba = returns.to_portfolio_returns_by_allocation(allocations)

contributions = pf.contributions.RegularContributions(387288, 25000)
ptbsba = prba.to_portfolio_timeframe_by_startyear_by_allocation(2500000, contributions)

ptbsba_stats = ptbsba.get_statistics()
ts = ptbsba_stats.filter_by_min_of('min').filter_by_min_of('max')

prba.save('retire2')
ptbsba.save('retire2')
ptbsba_stats.save('retire2_time')
ts.save('retire2_time_good')

print(ptbsba_stats.get_allocation_which_min_statistic('mean'))
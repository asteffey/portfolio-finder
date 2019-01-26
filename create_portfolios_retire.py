import pandas as pd
import numpy as np 
import math
import progressbar
import pickle

from combinatorics import range_of_allocations

def get_random_weights(number):
    weights = np.random.random(number)
    #TODO: fix temp mod to ensure REIT is never over 15%
    # weights[3] *= 0.15
    # weights[0:3] = weights[0:3] / np.sum(weights[0:3]) * (1-weights[3])
    # return weights
    return weights / np.sum(weights)

def get_weighted_yearly_returns(historic_data, inflation_data, weights):
    aggregate_yearly_returns = []
    for yr in historic_data.iterrows():
        inflation = inflation_data.get(yr[0])
        aggregate_yearly_returns.append(
            (sum(yr[1] * weights) - inflation) / (1 + inflation))
    return pd.Series(aggregate_yearly_returns, index=historic_data.axes[0])

def get_returns_over_timeframe(yearly_returns: pd.Series, timeframe):
    start_years_range = range(1970, 2017-timeframe+2)
    returns = []
    for start_year in start_years_range:
        value = 1
        for delta_year in range(timeframe):
            value *= (1 + yearly_returns.get(start_year + delta_year))
        returns.append(value - 1)
    return pd.Series(returns, index=start_years_range)


def get_random_portfolios(historic_data: pd.DataFrame, inflation_data, timeframe, portfolio_weights):
    portfolios_yearly_returns = []
    portfolios_returns_over_timeframe = []

    for weights in progressbar.progressbar(portfolio_weights):
        
        yearly_returns = get_weighted_yearly_returns(
            historic_data, inflation_data, weights)
        returns_over_timeframe = get_returns_over_timeframe(
            yearly_returns, timeframe)

        portfolios_yearly_returns.append(yearly_returns)
        portfolios_returns_over_timeframe.append(returns_over_timeframe)

    portfolios_symbol_weights = {}
    for index, symbol in enumerate(historic_data.columns):
        portfolios_symbol_weights[symbol] = [weight[index]
                                             for weight in portfolio_weights]

    return {"yearly_returns": portfolios_yearly_returns, "returns_over_timeframe": portfolios_returns_over_timeframe, "symbol_weights": portfolios_symbol_weights}

#######################################################################################################
#######################################################################################################
#######################################################################################################


#get data from csv
historic_financials = pd.read_csv("historic_financials.csv", index_col=0, squeeze=True)
risk_free_rate = historic_financials['RISK_FREE']
inflation_data = historic_financials['USA_INF']

historic_data = pd.read_csv("historic_data_retire.csv", index_col=0)

#0          1           2       3           4           5   6   7
#USA_TSM    WLDx_TSM	USA_INT	USA_BILL	USA_REIT	GLD	EM	SCB

custom_weights = range_of_allocations(20,8)
custom_weights = filter(lambda x : x[0]>=0.15 and x[0]<=0.4 and x[1]<=0.2 and x[2]<=0.2 and x[3]<=0.2 and x[4]<=0.15 and x[5]<=0.2 and x[6]<=0.3 and x[7]<=0.2, custom_weights)

random_portfolios = get_random_portfolios(historic_data, inflation_data, 20, list(custom_weights))

pickle.dump(random_portfolios, open('range_of_portfolios_20_retire20.bin',mode='wb'))

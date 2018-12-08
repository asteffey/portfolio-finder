import pandas as pd
import numpy as np 
import math
import progressbar
import pickle

def get_random_weights(number):
    weights = np.random.random(number)
    #TODO: fix temp mod to ensure REIT is never over 15%
    weights[4] *= 0.15
    weights[0:4] = weights[0:4] / np.sum(weights[0:4]) * (1-weights[4])
    return weights
    # return weights / np.sum(weights)

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


def get_random_portfolios(num_portfolios, historic_data: pd.DataFrame, risk_free_rate, timeframe, portfolio_weights = None):
    num_funds = len(historic_data.columns)

    portfolios_yearly_returns = []
    portfolios_returns_over_timeframe = []

    portfolio_weights = [get_random_weights(
        num_funds) for n in range(num_portfolios)] if portfolio_weights is None else portfolio_weights

    #ensure portfolios with 100% of each asset is accounted for
    # for i in range(num_funds):
    #     weights = [0]*num_funds
    #     weights[i] = 1
    #     portfolio_weights.append(np.array(weights))

    for weights in progressbar.progressbar(portfolio_weights):
        
        yearly_returns = get_weighted_yearly_returns(
            historic_data, risk_free_rate, weights)
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
historic_financials = pd.read_csv("historic_financials.csv", index_col=0, squeeze=True) / 100
risk_free_rate = historic_financials['RISK_FREE']

historic_data = pd.read_csv("historic_data.csv", index_col=0) / 100
#historic_data = historic_data.drop(labels='USA_BILL',axis=1)
#historic_data = historic_data.drop(labels='USA_REIT',axis=1)


custom_weights = [np.array([0.67, .15, .05, 0, .13]),
                  np.array([0.46, .23, .15, .01, .15]),
                  np.array([0.61, .12, .08, 0, .19]),
                  np.array([.45, .23, .08, 0, .24])]
                  #np.array([.15, .23, .01, 0, .61])

# custom_weights = [np.array([0.46, .23, .15, .01, .15]),
#                   np.array([1, 0, 0, 0, 0])]

# custom_weights = None

NUM_PORTFOLIOS = 50000
random_portfolios = get_random_portfolios(NUM_PORTFOLIOS, historic_data, risk_free_rate, 17, custom_weights)

pickle.dump(random_portfolios, open('random_portfolios_custom.bin',mode='wb'))

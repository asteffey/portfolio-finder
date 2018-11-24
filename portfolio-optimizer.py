import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

ANNUALISED_RISK_FREE_RATE = 0.0178

def get_ulcer_index (yearly_returns: pd.Series):
    sum_sq = 0
    max_value = 1
    current_value = 1
    for percent_return in yearly_returns.iteritems():
        current_value *= (1 + percent_return[1])
        if current_value > max_value:
            max_value = current_value
            print(0)
        else:
            sum_sq += (100 * ((current_value / max_value) - 1)) ** 2
            print((100 * ((current_value / max_value) - 1)) ** 2)
    return math.sqrt(sum_sq / len(yearly_returns))

def get_aggregate_yearly_returns (historic_data, inflation_data, weights):
    aggregate_yearly_returns = []
    for yr in historic_data.iterrows():
        inflation = inflation_data.get(yr[0])
        aggregate_yearly_returns.append((sum(yr[1] * weights) - inflation) / (1+ inflation))
    return pd.Series(aggregate_yearly_returns, index=historic_data.axes[0])


def get_total_return (yearly_returns: pd.Series):
    current_value = 1
    for percent_return in yearly_returns.iteritems():
        current_value *= (1 + percent_return[1])
    return current_value

def get_returns_over_timeframe (yearly_returns: pd.Series, timeframe):
    start_years_range = range(1970,2017-timeframe+2)
    returns = []
    for start_year in start_years_range:
        value = 1
        for delta_year in range(timeframe):
            value *= (1 + yearly_returns.get(start_year + delta_year))
        returns.append(value)
    return pd.Series(returns, index=start_years_range)



def get_random_portfolios_results (yearly_returns, timeframe):
    #TODO: look at a set of random portfolios at once
    return None



inflation_data = pd.read_csv("usa_inf.csv", index_col=0, squeeze=True) / 100

#get data from csv
historic_data = pd.read_csv("historic_data.csv", index_col=0) / 100
#historic_data = historic_data.drop(labels='USA_REIT',axis=1)


weights=[.25,.25,.25,.25]
yearly_returns = get_aggregate_yearly_returns(historic_data, inflation_data, weights)

ui = get_ulcer_index(yearly_returns)

breakpoint()

#TODO: get UPI

#TODO: output text data

#TODO: graph data


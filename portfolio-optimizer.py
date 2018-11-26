import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import progressbar

ANNUALISED_RISK_FREE_RATE = 0.0178

#TODO: figure out why ulcer index differs from portfoliocharts.com


def get_ulcer_index(yearly_returns: pd.Series):
    sum_sq = 0
    max_value = 1
    current_value = 1
    for percent_return in yearly_returns.iteritems():
        current_value *= (1 + percent_return[1])
        if current_value > max_value:
            max_value = current_value
            # print(0)
        else:
            sum_sq += (100 * ((current_value / max_value) - 1)) ** 2
            # print((100 * ((current_value / max_value) - 1)) ** 2)
    return math.sqrt(sum_sq / len(yearly_returns))


def get_annualized_return(total_return, timeframe):
    return (total_return + 1) ** (1 / timeframe) - 1


def get_aggregate_yearly_returns(historic_data, inflation_data, weights):
    aggregate_yearly_returns = []
    for yr in historic_data.iterrows():
        inflation = inflation_data.get(yr[0])
        aggregate_yearly_returns.append(
            (sum(yr[1] * weights) - inflation) / (1 + inflation))
    return pd.Series(aggregate_yearly_returns, index=historic_data.axes[0])


def get_total_return(yearly_returns: pd.Series):
    current_value = 1
    for percent_return in yearly_returns.iteritems():
        current_value *= (1 + percent_return[1])
    return current_value - 1


def get_returns_over_timeframe(yearly_returns: pd.Series, timeframe):
    start_years_range = range(1970, 2017-timeframe+2)
    returns = []
    for start_year in start_years_range:
        value = 1
        for delta_year in range(timeframe):
            value *= (1 + yearly_returns.get(start_year + delta_year))
        returns.append(value - 1)
    return pd.Series(returns, index=start_years_range)


def get_random_weights(number):
    weights = np.random.random(number)
    return weights / np.sum(weights)


def get_random_portfolios_results(num_portfolios, historic_data: pd.DataFrame, inflation_data: pd.Series, timeframe):
    #TODO: look at a set of random portfolios at once

    portfolio_returns = []
    portfolio_risks = []
    portfolio_ratios = []
    portfolio_weights = []

    for n in progressbar.progressbar(range(num_portfolios)):
        weights = get_random_weights(len(historic_data.columns))
        yearly_returns = get_aggregate_yearly_returns(
            historic_data, inflation_data, weights)
        returns_over_timeframe = get_returns_over_timeframe(
            yearly_returns, timeframe)

        expected_return = np.mean(returns_over_timeframe)
        risk_index = np.std(returns_over_timeframe)#get_ulcer_index(yearly_returns)
        upi_ratio = expected_return / risk_index

        portfolio_returns.append(expected_return)
        portfolio_risks.append(risk_index)
        portfolio_ratios.append(upi_ratio)
        portfolio_weights.append(weights)

    portfolio_results = {'Return': portfolio_returns,
                         'Risk': portfolio_risks, 'Ratio': portfolio_ratios}

    for index, symbol in enumerate(historic_data.columns):
        portfolio_results[symbol+' Weight'] = [weight[index]
                                               for weight in portfolio_weights]

    return pd.DataFrame(portfolio_results)

def get_portfolio_where (portfolio_results, column, function, *args):
    return portfolio_results.loc[portfolio_results[column] == function(portfolio_results[column], *args)]

inflation_data = pd.read_csv("usa_inf.csv", index_col=0, squeeze=True) / 100

#get data from csv
historic_data = pd.read_csv("historic_data.csv", index_col=0) / 100
#historic_data = historic_data.drop(labels='USA_REIT',axis=1)

portfolio_results = get_random_portfolios_results(
    1000, historic_data, inflation_data, 15)


max_return_portfolio = get_portfolio_where(portfolio_results, 'Return', np.max)
max_ratio_portfolio = get_portfolio_where(portfolio_results, 'Ratio', np.max)
min_risk_portfolio = get_portfolio_where(portfolio_results, 'Risk', np.min)

#TODO: output text data
#current placeholder:
print("\nMax Return\n", max_return_portfolio)
print("\nMax Ratio\n", max_ratio_portfolio)
print("\nMin Risk\n", min_risk_portfolio)

#TODO: graph data
#current placeholder:
plt.style.use('seaborn-dark')
portfolio_results.plot.scatter(x='Risk', y='Return', c='Ratio',
                cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
plt.scatter(x=max_ratio_portfolio['Risk'],
            y=max_ratio_portfolio['Return'], c='blue', marker='+', s=200)

plt.xlabel('Risk')
plt.ylabel('Mean Return')
plt.title('Efficient Frontier')
plt.show(block=False)

breakpoint()

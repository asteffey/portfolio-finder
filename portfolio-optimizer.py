import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import math
import progressbar
from scipy.stats import gmean
import cProfile

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




def get_weighted_yearly_returns(historic_data, inflation_data, weights):
    aggregate_yearly_returns = []
    for yr in historic_data.iterrows():
        inflation = inflation_data.get(yr[0])
        aggregate_yearly_returns.append(
            (sum(yr[1] * weights) - inflation) / (1 + inflation))
    return pd.Series(aggregate_yearly_returns, index=historic_data.axes[0])


def get_cumulative_change(yearly_returns: pd.Series, start_year = None):
    current_value = 1
    cumulative_return = []
    returns_list = yearly_returns.loc[start_year:] if start_year else yearly_returns
    #returns_list = yearly_returns.iteritems()
    for percent_return in returns_list.iteritems():
        current_value *= (1 + percent_return[1])
        cumulative_return.append(current_value)
    return pd.Series(cumulative_return, index=returns_list.axes[0])


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


def get_random_portfolios(num_portfolios, historic_data: pd.DataFrame, inflation_data: pd.Series, risk_free_rate, timeframe, portfolio_weights = None):
    num_funds = len(historic_data.columns)

    portfolios_yearly_returns = []
    portfolios_returns_over_timeframe = []
    portfolios_risk = []

    portfolio_weights = [get_random_weights(
        num_funds) for n in range(num_portfolios)] if portfolio_weights is None else portfolio_weights

    #ensure portfolios with 100% of each asset is accounted for
    # for i in range(num_funds):
    #     weights = [0]*num_funds
    #     weights[i] = 1
    #     portfolio_weights.append(np.array(weights))

    # risk_free_returns_over_timeframe = get_returns_over_timeframe(
    #     risk_free_rate, timeframe)

    for weights in progressbar.progressbar(portfolio_weights):
        
        yearly_returns = get_weighted_yearly_returns(
            historic_data, risk_free_rate, weights)
        returns_over_timeframe = get_returns_over_timeframe(
            yearly_returns, timeframe)
        returns_over_risk_free_over_timeframe = returns_over_timeframe# - risk_free_returns_over_timeframe
        # risk_index = np.std(returns_over_risk_free_over_timeframe) 
        risk_index = get_ulcer_index(yearly_returns)

        if risk_index == 0:
            continue

        portfolios_yearly_returns.append(yearly_returns)
        portfolios_returns_over_timeframe.append(returns_over_risk_free_over_timeframe)
        portfolios_risk.append(risk_index)

    portfolios_symbol_weights = {}
    for index, symbol in enumerate(historic_data.columns):
        portfolios_symbol_weights[symbol] = [weight[index]
                                             for weight in portfolio_weights]

    return {"yearly_returns": portfolios_yearly_returns, "returns_over_timeframe": portfolios_returns_over_timeframe, "Risk": portfolios_risk, "symbol_weights": portfolios_symbol_weights}

#@do_cprofile
def get_portfolios_results(portfolios, return_function: np.mean, *return_function_args):
    portfolio_selected_returns = []
    portfolio_ratios = []

    for index, returns_over_timeframe in enumerate(portfolios["returns_over_timeframe"]):
        selected_return = return_function(returns_over_timeframe, *return_function_args)
        selected_risk_ratio = selected_return / portfolios["Risk"][index]

        portfolio_selected_returns.append(selected_return) #expected_return
        portfolio_ratios.append(selected_risk_ratio)

    portfolio_results = {'Return': portfolio_selected_returns,
                         'Risk': portfolios["Risk"], 'Ratio': portfolio_ratios}

    return pd.DataFrame({**portfolio_results, **portfolios["symbol_weights"]})


def get_portfolio_where(portfolio_results, column, function, *args):
    return portfolio_results.loc[portfolio_results[column] == function(portfolio_results[column], *args)]

def get_efficient_frontier_portfolios(portfolio_results, num_points):
    min_return = portfolio_results['Return'].min()
    max_return = portfolio_results['Return'].max()
    step = (max_return - min_return) / num_points
    
    efficient_frontier_portfolios = []
    
    cur_return = min_return
    while (cur_return < max_return):
        portfolio_range = portfolio_results.loc[(cur_return <= portfolio_results['Return']) & (portfolio_results['Return'] < (cur_return + step))]
        efficient_frontier_portfolios.append(get_portfolio_where(portfolio_range, 'Risk', np.min))
        cur_return += step

    return pd.concat(efficient_frontier_portfolios)

def output_portfolios(portfolios):
    for label, portfolio in portfolios.items():
        print()
        print(label)
        print(portfolio)
    return None


def plot_results(portfolio_results, points):
    plt.style.use('seaborn-dark')
    portfolio_results.plot.scatter(x='Risk', y='Return', c='Ratio',
                                   cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
    for point in points:
        plt.scatter(x=point[0]['Risk'], y=point[0]['Return'],
                    c=point[1], marker='+', s=200, label=point[2])
        # plt.annotate(point[2], xy=(point[0]['Risk'], point[0]['Return']), xytext=(
        #     point[0]['Risk']-0.17, point[0]['Return']+0.17))

    plt.xlabel('Risk')
    plt.ylabel('Mean Return')
    plt.title('Efficient Frontier')
    plt.show(block=True)


#######################################################################################################

#get data from csv
historic_financials = pd.read_csv("historic_financials.csv", index_col=0, squeeze=True) / 100
inflation_data = historic_financials['USA_INF']
risk_free_rate = historic_financials['RISK_FREE']

historic_data = pd.read_csv("historic_data.csv", index_col=0) / 100
#historic_data = historic_data.drop(labels='USA_BILL',axis=1)
historic_data = historic_data.drop(labels='USA_REIT',axis=1)
NUM_PORTFOLIOS = 5000

# portfolio_results = get_random_portfolios_results(
#     NUM_PORTFOLIOS, historic_data, inflation_data, risk_free_rate, 17)

# key_portfolios = {}
# key_portfolios['Max Return'] = get_portfolio_where(
#     portfolio_results, 'Return', np.max)
# key_portfolios['Min Risk'] = get_portfolio_where(
#     portfolio_results, 'Risk', np.min)
# key_portfolios['Min Return'] = get_portfolio_where(
#     portfolio_results, 'Return', np.min)

# key_portfolios['Max Ratio'] = get_portfolio_where(
#     portfolio_results, 'Ratio', np.max)

# output_portfolios(key_portfolios)
# efficient_frontier_portfolios = get_efficient_frontier_portfolios(portfolio_results, 50)
# print(efficient_frontier_portfolios)

# plot_results(portfolio_results, [(key_portfolios['Max Ratio'], 'blue', 'Max Ratio')])

results = []
full_results = []

#custom_weights = [np.array([.42, .10, .48, 0]), np.array([.33, .20, .46, 0.01])]
custom_weights = None

random_portfolios = get_random_portfolios(NUM_PORTFOLIOS, historic_data, inflation_data, risk_free_rate, 17, custom_weights)

#percentiles = [0,10,20,30,40,50,60,70,80,90,100]
percentiles = [5, 15, 50, 85, 95]


plt_figure_num=0
for return_function in (list(map(lambda p: (np.percentile, p), percentiles)) + [(np.mean, None), (gmean, None)]):
    

    portfolio_results = get_portfolios_results(random_portfolios, *return_function)

    max_ratio = get_portfolio_where(portfolio_results, 'Ratio', np.max)
    series_id = return_function[1] if return_function[1] is not None else return_function[0].__name__
    max_ratio.loc[:,'percentile'] = series_id
    max_ratio.set_index('percentile')

    print("{}:".format(series_id))
    print(get_efficient_frontier_portfolios(portfolio_results, 20))

    # plt.close()
    # plt.figure(plt_figure_num)
    # plt_figure_num += 1
    # plt.figure().canvas.set_window_title("{} Percentile".format(series_id) if type(series_id) == int else series_id) #this is a leak abstraction
    # plot_results(portfolio_results, [(max_ratio, 'blue', 'Max Ratio')])

    full_results.append(portfolio_results)
    results.append(max_ratio)
results = pd.concat(results)
print(results)
breakpoint()

# plt.close()
# plt.style.use('seaborn-dark')
# for asset in historic_data.columns:
#     print(asset)
#     get_cumulative_change(historic_data[asset]).plot(legend=True, label=asset)

# plt.show()

# breakpoint()
    
    


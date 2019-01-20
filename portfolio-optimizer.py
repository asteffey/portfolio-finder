import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import math
import progressbar
from scipy.stats import gmean
import pickle

def get_annualized_return(total_return, timeframe):
    return (total_return + 1) ** (1 / timeframe) - 1

def get_cumulative_change(yearly_returns: pd.Series, start_year = None):
    current_value = 1
    cumulative_return = []
    returns_list = yearly_returns.loc[start_year:] if start_year else yearly_returns
    #returns_list = yearly_returns.iteritems()
    for percent_return in returns_list.iteritems():
        current_value *= (1 + percent_return[1])
        cumulative_return.append(current_value)
    return pd.Series(cumulative_return, index=returns_list.axes[0])

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

def get_total_return(yearly_returns: pd.Series):
    current_value = 1
    for percent_return in yearly_returns.iteritems():
        current_value *= (1 + percent_return[1])
    return current_value - 1


def get_portfolios_results(portfolios, return_function: np.mean, *return_function_args):
    portfolio_selected_returns = []
    portfolios_risk = []
    portfolio_ratios = []
    portfolio_low_returns = []
    portfolio_high_returns = []
    portfolio_mean_returns = []
    portfolio_gmean_returns = []

    for index, returns_over_timeframe in enumerate(portfolios["returns_over_timeframe"]):
        selected_return = return_function(returns_over_timeframe, *return_function_args)

        # risk_index = np.std(returns_over_timeframe) 
        #risk_index = get_ulcer_index(portfolios["yearly_returns"][index])
        risk_index = 1 / np.min(returns_over_timeframe) #TODO: check for dividebyzero

        if risk_index == 0:
            risk_index = 0.01

        selected_risk_ratio = selected_return / risk_index

        portfolio_low_returns.append(np.min(returns_over_timeframe))
        portfolio_high_returns.append(np.max(returns_over_timeframe))
        portfolio_mean_returns.append(np.mean(returns_over_timeframe))
        portfolio_gmean_returns.append(gmean(returns_over_timeframe))
        
        portfolio_selected_returns.append(selected_return) #expected_return
        portfolios_risk.append(risk_index)
        portfolio_ratios.append(selected_risk_ratio)

    portfolio_results = {'Return': portfolio_selected_returns,
                         'Low': portfolio_low_returns,
                         'GMean': portfolio_gmean_returns,
                         'Mean': portfolio_mean_returns,
                         'High': portfolio_high_returns,
                         'Risk': portfolios_risk, 'Ratio': portfolio_ratios}

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
#######################################################################################################
#######################################################################################################

max_ratio_results = []
max_return_results = []
full_results = []

#TODO: load portfolio_data here


#percentiles = [0,10,20,30,40,50,60,70,80,90,100]
percentiles = list(range(0,101,5))

random_portfolios = pickle.load(open('range_of_portfolios_20_retire20.bin',mode='rb'))

plt_figure_num=0
for return_function in progressbar.progressbar(list(map(lambda p: (np.percentile, p), percentiles)) + [(np.mean, None), (gmean, None)]):
    portfolio_results = get_portfolios_results(random_portfolios, *return_function)
    series_id = return_function[1] if return_function[1] is not None else return_function[0].__name__

    max_ratio = get_portfolio_where(portfolio_results, 'Ratio', np.max)
    max_ratio.loc[:,'percentile'] = series_id
    max_ratio.set_index('percentile')

    max_return = get_portfolio_where(portfolio_results, 'Return', np.max)
    max_return.loc[:,'percentile'] = series_id
    max_return.set_index('percentile')

    # print("{}:".format(series_id))
    # print(get_efficient_frontier_portfolios(portfolio_results, 20))

    # plt.close()
    # plt.figure(plt_figure_num)
    # plt_figure_num += 1
    # plt.figure().canvas.set_window_title("{} Percentile".format(series_id) if type(series_id) == int else series_id) #this is a leak abstraction
    # plot_results(portfolio_results, [(max_ratio, 'blue', 'Max Ratio')])

    full_results.append(portfolio_results)
    max_ratio_results.append(max_ratio)
    max_return_results.append(max_return)

max_ratio_results = pd.concat(max_ratio_results)
max_return_results = pd.concat(max_return_results)
print("\nmax_ratio:")
print(max_ratio_results)
print("\nmax_return:")
print(max_return_results)

# breakpoint()

# plt.close()
# plt.style.use('seaborn-dark')
# for asset in historic_data.columns:
#     print(asset)
#     get_cumulative_change(historic_data[asset]).plot(legend=True, label=asset)

# plt.show()

# breakpoint()
    
    


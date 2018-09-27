The following scripts are used to analyze financial data.

#####
# scripts for statistical analysis
#####

**autocorrelation.py plots the variance over time compared to a given chart in order to see trend patterns.

**correlation_matrix.py plots the correlation heat map of any number of symbols.

**covariance.py generates the individual variance and std deviation, and the covariance of any set of stocks.

**portfolio_variance.py generate the variance of a portfolio over a given period.

**sharpe_ratio.py generate the sharpe ratio for a given portfolio over a given period.

**sp_sharpe.py generates the sharpe ratio for the S&P500 over a given period.

#####
# scripts for backtesting and data manipulation
#####

**backtest.py this script backtests and generates returns on an asset using the variance trend following approach to generate trade signals. The results of the trend following approach are compared with a long term buy and hold strategy.

**date_format.py format and sort a .csv file by date

**pull_data.py pull historic price data from yahoo finance and save as .csv file.

**weights.py generate weights of given symbols in a portfolio.

#####
# scripts for pricing
#####

**butterfly_plot.py plots the price payoff of a butterfly spread.

**long_call_butterfly_plot.py plots the price payoff of a long call butterfly spread.

**short_put_butterfly_plot.py plots the price payoff of a short put butterfly spread.

**short_put_butterfly_price.py generates accurate pricing for the short put butterfly spread.

**spread_pricing.py more pricing info on butterfly spread.
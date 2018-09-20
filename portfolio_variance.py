'''
Portfolio Variance

Variance (sigma squared) is a measure of the dispersion of a set of datapoints around
their mean value. Variance measures the variability from an average (volatility).
Variance uses squares because it weights outliers more heavily than data near the mean.


Given2:
-a list of securities and weights in portfolio.
-daily closing price data from min previous 501 trading days.
price data must be in the following format:
Date first column, ascending from oldest date
Close second column

Return2: portfolio return variance
Calculated as: port_var=W'_p *S*W_p
where
W'_p: transpose of vector of weights of securities in portfolio
S: sample covariance matrix of returns
W_p: vector of weights of securities in portfolio


The portfolio return variance is a measure of consistency of returns.
The lower the correlation between securities in the portfolio, the lower the portfolio variance.

Standard deviation is the square root of variance.
By taking the standard deviation of a portfolios annual rate of return, you can better measure the
consistency with which returns are generated.

'''
import pandas as pd
import numpy as np
import datetime
from math import sqrt
# from datetime import timedelta

from yahoofinancials import YahooFinancials as yf

#open csv file, return matrix of data of previous period trading days
def import_data(file_name,start_date,period):
	#open the file using pandas
	data = pd.read_csv(file_name,header=0)
	#if prices are strings, convert to floats
	data['Close']=data['Close'].apply(pd.to_numeric, errors='coerce')
	
	#rearrange to make most recent dates first
	data=data.sort_values(by=['Date'],ascending=False)
	# print(data[['Date','Close']].head())
	
	#pull out the previous 501 days of data starting with start_date
	start_date=datetime.datetime.strptime(start_date,'%Y-%m-%d')
	# print(start_date.date())
	end_date=start_date-datetime.timedelta(days=period)
	# print(end_date.date())
	# data = data[(data['Date'] > datetime.datetime.strftime(end_date,'%Y-%m-%d')) & (data['Date'] < datetime.datetime.strftime(start_date,'%Y-%m-%d'))]
	start_date_index=data.loc[data['Date']==datetime.datetime.strftime(start_date,'%Y-%m-%d')].index[0]
	# print(start_date_index)
	end_date_index=start_date_index-period
	# print(end_date_index)
	# data = data[['Date','Close']].loc[end_date_index:start_date_index]
	data = data[['Date','Close']].loc[start_date_index:end_date_index]
	return pd.np.array(data)
	
	
def portfolio_variance(weights,covar_matrix):
	return np.dot(weights.T,np.dot(covar,weights))
	#or
	# return weights.T*np.matrix(covar)*weights
	
	

def update_quote(symbols):
	pull_data = yf(symbols)
	all_data = pull_data.get_stock_price_data(reformat=True)
	current_price = [all_data[sym]['regularMarketPrice'] for sym in symbols]
	return current_price
	
def weights():
	##################
	# input current holdings levels
	##################
	gold=3
	#Gold: XAUUSD=X
	silver=157
	#Silver: XAGUSD=X
	AAPL=105
	SYF=699
	SWKS=200

	holdings=[gold,silver,AAPL,SYF,SWKS]
	
	#for implementation use the following
	# prices=update_quote(['XAUUSD=X','XAGUSD=X','AAPL','SYF','SWKS'])
	#for test use the values below
	prices=[1209.10,14.17,223.85,32.44,82.63]
	
	position_val=[a*b for a,b in zip(holdings,prices)]
	total_val=sum(position_val)
	weights_in_list=[a/total_val for a in position_val]
	weights=[[a/total_val] for a in position_val]
	# print(weights)
	# return weights
	return weights_in_list,np.array(weights)

	
def main():

	####################
	# The overall portfolio variance
	####################
	
	# Need to write separate script to update all csv files with most recent data
	
	# read csv price data from previous 501 days
	holdings=['GOLD','SILVER','AAPL','SYF','SWKS']
	read_file=[sym+'.csv' for sym in holdings]
	recent_start_date='2018-09-05'
	# data_set=import_data(read_file[0],recent_start_date)
	# print(data_set)
	
	#period is the time period over which to calculate the covariance of each holding
	period=501
	
	# data_sets is a list of lists where each list is the daily closing price over
	# the specified period
	data_sets=[import_data(file,recent_start_date,period) for file in read_file]
	# print(len(data_sets)) #5 data sets
	# print(len(data_sets[0])) #501 items in each data set
	# print(data_sets[0][:5])
	# print(type(data_sets[0][5][1]))
	
	
	# calculate daily returns based on closing prices
	# returns_data_sets is a list of lists where each list is the
	# daily returns of the symbol over the last given period
	returns_data_sets=[]
	for set in data_sets:
		returns=[]
		for i in range(1,len(set)):
			# print(str(set[i][0])+' '+str(set[i][1]))
			returns.append(set[i-1][1]-set[i][1])
		returns_data_sets.append(returns)


	# generate the covariance matrix of the sample returns
	# this shows how closely the daily returns of the last given period correlate to each other
	cov_matrix=np.cov(returns_data_sets)
	cov_matrix=np.around(cov_matrix,4)
	# np.set_printoptions(suppress=True)
	# print(cov_matrix)
	
	
	# get the weights of each holding
	weights_list,cov_weights=weights()
	
	# multiply the weights and covariance matrix to generate the portfolio variance
	port_var=np.dot(cov_weights.T,np.dot(cov_matrix,cov_weights))
	print('Portfolio variance is '+str(round(port_var[0][0],4)))
	print('Portfolio std dev is '+str(round(sqrt(port_var[0][0]),4)))






main()
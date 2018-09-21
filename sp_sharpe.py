'''
Sharpe Ratio for S&P500
The most widely used method for calculating risk-adjusted return
The higher the sharpe ratio the better.
ex1: Buffett sharpe ratio for 1976-2011 is 0.76
19% excess return over risk free rate, 24.9% volatility
ex2: the market ratio for 1976-2011 is 0.39
6.16% excess return, 15.8% volatility


Can be inaccurate when applied to portfolios that do not have normal distribution of expected returns
can be inaccurate with portfolios with a high degree of kurtosis (fat tails)

Also can be inaccurate on portfolios with non-linear risks such as warrants or options
(see sortino ratio which removes the effects of upward price movements on std dev
to measure only return against downward price volatility.)

Given:
S&P500 data set

Return:
The sharpe ratio of the market over the given period
sharpe ratio=(mean portfolio return-risk free rate)/portfolio standard deviation

'''

#for data manipulation
import pandas as pd
import numpy as np
import datetime
from collections import defaultdict
from math import sqrt

#open csv file, return matrix of data, date in col1, data col2
def import_data(file_name,start_date,end_date):
	#open the file using pandas
	# print(file_name)
	data = pd.read_csv(file_name,header=0)
	# print(data[['Date','Close']].head())
	#if prices are strings, convert to floats
	data['Close']=data['Close'].apply(pd.to_numeric, errors='coerce')
	# print(data[['Date','Close']].head())
	#rearrange to make most recent dates first
	data=data.sort_values(by=['Date'],ascending=False)
	# print(data[['Date','Close']].head())
	
	#pull out the data over given range
	start_date=datetime.datetime.strptime(start_date,'%Y-%m-%d')
	# print(start_date.date())
	end_date=datetime.datetime.strptime(end_date,'%Y-%m-%d')
	# print(end_date.date())
	# data = data[(data['Date'] > datetime.datetime.strftime(end_date,'%Y-%m-%d')) & (data['Date'] < datetime.datetime.strftime(start_date,'%Y-%m-%d'))]
	start_date_index=data.loc[data['Date']==datetime.datetime.strftime(start_date,'%Y-%m-%d')].index[0]
	# print(start_date_index)
	end_date_index=data.loc[data['Date']==datetime.datetime.strftime(end_date,'%Y-%m-%d')].index[0]
	# print(end_date_index)
	# print(type(int(end_date_index)))
	# data = data[['Date','Close']].loc[end_date_index:start_date_index]
	data = data[['Date','Close']].loc[int(end_date_index):int(start_date_index)]
	# print(data.head())
	return pd.np.array(data)
	
	
#open csv file, return price delta over given time period
def gen_not_return(file_name,start_date,end_date):
	#open the file using pandas, use the first row as the header
	# need to fix this function to accomodate for times when the start_date or end_date is not in the csv file
	# will need to find nearest date
	read = pd.read_csv(file_name,header=0)

	for i in range(len(read)):
		if datetime.datetime.strptime(read['Date'][i],'%Y-%m-%d') == start_date:
			beg_price=float(read['Close'][i])
		if datetime.datetime.strptime(read['Date'][i],'%Y-%m-%d') == end_date:
			end_price=float(read['Close'][i])
	return end_price-beg_price,beg_price

	
	
	
def gen_return(data,start_date,end_date):
	# give the stock return in % over a given period based on the holdings dictionary
	
	# get the closing price at the start date
	st_dt_close=data[-1][1]
	end_dt_close=data[0][1]
	
	# get return over the period
	period_return=end_dt_close-st_dt_close

	# give the return in %
	tot_return=period_return/st_dt_close

	return tot_return
	
	
	
	
def port_std_dev(file_name,start_date,period):
	# generate the standard deviation of the portfolio
	
	# open the file using pandas
	# print(file_name)
	data = pd.read_csv(file_name,header=0)
	# print(data[['Date','Close']].head())
	#if prices are strings, convert to floats
	data['Close']=data['Close'].apply(pd.to_numeric, errors='coerce')
	# print(data[['Date','Close']].head())
	#rearrange to make most recent dates first
	data=data.sort_values(by=['Date'],ascending=False)
	# print(data[['Date','Close']].head())
	
	#pull out the data over given range
	start_date=datetime.datetime.strptime(start_date,'%Y-%m-%d')
	# print(start_date.date())

	# print(end_date.date())
	# data = data[(data['Date'] > datetime.datetime.strftime(end_date,'%Y-%m-%d')) & (data['Date'] < datetime.datetime.strftime(start_date,'%Y-%m-%d'))]
	start_date_index=data.loc[data['Date']==datetime.datetime.strftime(start_date,'%Y-%m-%d')].index[0]
	# print(start_date_index)
	end_date_index=start_date_index-period
	# print(end_date_index)
	# print(type(int(end_date_index)))
	# data = data[['Date','Close']].loc[end_date_index:start_date_index]
	data = data[['Date','Close']].loc[int(start_date_index):int(end_date_index)]
	data = data.reset_index(drop=True)
	# print(type(data['Close'].loc[1]))
	# print(data.head())

	# daily percentage return of the symbol over the last given period
	returns=[]
	for i in range(period):
		returns.append((data['Close'].loc[i]-data['Close'].loc[i+1])/data['Close'].loc[i+1])
		
	# print(max(returns))
	
	# get the std dev of the daily returns over the given period
	std_dev=np.std(returns)
	# print('Portfolio std dev is '+str(std_dev))
	return std_dev

	
	
def main():
	risk_free_r=0.03

	#set a date range to test in '%Y-%m-%d' format
	start_date='2018-08-01'
	end_date='2018-08-31'
	
	file='SP500.csv'
	# get the data set of the closing prices over the given period
	data_set=import_data(file,start_date,end_date)
	
	# generate portfolio return in % over given period
	# For the S&P500, the weight will just be 1
	port_return=gen_return(data_set,start_date,end_date)
	# print('portfolio return is '+str(round(port_return,2)))
	
	#generate portfolio std dev over given period
	period=501
	std_dev=port_std_dev(file,start_date,period)
	# print('portfolio std dev is '+str(round(std_dev,2)))
	
	#sharpe ratio
	sharpe=(port_return-risk_free_r)/std_dev
	print('portfolio sharpe ratio is '+str(round(sharpe,4)))
	



main()
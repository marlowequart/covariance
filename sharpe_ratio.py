'''
sharp ratio


Given:
historical stock holdings/trade data

Return:


'''

#for data manipulation
import pandas as pd
import numpy as np
import datetime
from collections import defaultdict
from math import sqrt

#open csv file, return matrix of data of previous period trading days
def closing_data(file_name,start_date,period):
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
	
	
def holdings():
	# create a dictionary of holdings, with the following entries:
	# Symbol is key
	# 0:purchase date (list of all purchases made)
	# 1:number of shares purchased (to match with list of dates)
	# 2:price at time of purchase
	# 3:sale date (list of all sales)
	# 4:number of shares sold (to match with list of sales)
	# 5:price at time of sale
	# return the dictionary
	
	# open history.csv file
	# open the file using pandas, use the first row as the header
	read = pd.read_csv('history.csv',header=0)
	#if prices are strings, convert to floats
	# read['Close']=read['Close'].apply(pd.to_numeric, errors='coerce')
	
	# if sale date is NAN, replace with todays date
	today=datetime.datetime.today().strftime('%Y-%m-%d')
	read['date_s'].fillna(today, inplace=True)
	# if sale num shares is NAN, replace with 0
	read['num_s'].fillna(0, inplace=True)
	# if sale price is NAN, replace with 0
	read['price_s'].fillna(0, inplace=True)

	date_p=read.groupby('symbol')['date_p'].apply(lambda x: x.tolist())
	date_p_dict=date_p.to_dict()
	num_p=read.groupby('symbol')['num_p'].apply(lambda x: x.tolist())
	num_p_dict=num_p.to_dict()
	price_p=read.groupby('symbol')['price_p'].apply(lambda x: x.tolist())
	price_p_dict=price_p.to_dict()	
	date_s=read.groupby('symbol')['date_s'].apply(lambda x: x.tolist())
	date_s_dict=date_s.to_dict()
	num_s=read.groupby('symbol')['num_s'].apply(lambda x: x.tolist())
	num_s_dict=num_s.to_dict()
	price_s=read.groupby('symbol')['price_s'].apply(lambda x: x.tolist())
	price_s_dict=price_s.to_dict()	

	return {key:[date_p_dict[key],num_p_dict[key],price_p_dict[key],date_s_dict[key],num_s_dict[key],price_s_dict[key]] for key in date_p_dict}

#open csv file, return price delta over given time period
def gen_return(file_name,start_date,end_date):
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

	
	
	
def return_calc(dictionary,start_date,end_date):
	# give the portfolio return in % over a given period based on the holdings dictionary
	
	st_dt_num=datetime.datetime.strptime(start_date,'%Y-%m-%d')
	end_dt_num=datetime.datetime.strptime(end_date,'%Y-%m-%d')
	
	# create a dictionary with each symbol and number of shares held over given period	
	hold_beg={}
	hold_tot={}
	for sym in dictionary:
		shares_ownd_begin=[]
		shares_ownd_end=[]
		shares_ownd_tot=[]
		for i in range(len(dictionary[sym][0])):
			# get purchase date for holding
			p_date=datetime.datetime.strptime(dictionary[sym][0][i],'%Y-%m-%d')
			#get sale date for holding
			# print(dictionary[sym][3][i])
			s_date=datetime.datetime.strptime(dictionary[sym][3][i],'%Y-%m-%d')
			# generate the shares held at beginning of period
			if (p_date <= st_dt_num):
				shares_ownd_begin.append(dictionary[sym][1][i])
			hold_beg.update({sym:sum(shares_ownd_begin)})
			# if the holding was held for the entire date range, add the number of shares held to the dict
			if (p_date <= st_dt_num) & (s_date >= end_dt_num):
				shares_ownd_tot.append(dictionary[sym][1][i])
			hold_tot.update({sym:sum(shares_ownd_tot)})
		# print(hold[sym])
	
	# get the return of each symbol in dictionary over the holding period
	files={sym:str(sym)+'.csv' for sym in dictionary}
	returns={}
	#port_val_beg is a list of the value of each holding at the beginning of the period
	port_val_beg=[]
	sum_returns=[]
	for sym in files:
		# print(files[sym])
		return1,beg_price=gen_return(files[sym],st_dt_num,end_dt_num)
		return2=return1*hold_tot[sym]
		returns.update({sym:return2})
		port_val_beg.append(beg_price*hold_beg[sym])
		sum_returns.append(return2)
	
	#port_val is the total portfolio value at the beginning of the period
	port_val=sum(port_val_beg)
	
	#generate the weight in % of each symbol at the beginning of the period
	weights_in_list=[sym_val/port_val for sym_val in port_val_beg]
	#generate the weights in a numpy array
	weights=[[sym_val/port_val] for sym_val in port_val_beg]
	cov_weights=np.array(weights)
	
	all_return=sum(sum_returns)
	tot_return=round(100*all_return/port_val,2)
	# print(port_val)
	# print(tot_return)
	# print(weights)
	return tot_return,cov_weights
	
	
	
	
def port_std_dev(dictionary,start_date,cov_weights):
	# generate the standard deviation of the portfolio using the sqrt of variance
	
	
	
	#period is the time period over which to calculate the covariance of each holding
	period=501
	
	# create list of csv files to pull data from
	files=[str(sym)+'.csv' for sym in dictionary]
	
	# data_sets is a list of lists where each list is the daily closing price over
	# the specified period
	data_sets=[closing_data(file,start_date,period) for file in files]	
	
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
	cov_matrix=np.cov(returns_data_sets)
	
	# multiply the weights and covariance matrix to generate the portfolio variance
	port_var=np.dot(cov_weights.T,np.dot(cov_matrix,cov_weights))
	
	# std dev is the sqrt of variance
	std_dev=round(sqrt(port_var[0][0]),4)
	# print('Portfolio std dev is '+str(std_dev))
	return std_dev

	
	
def main():
	risk_free_r=0.03
	# get the dictionary of holdings
	hold_dict=holdings()
	
	#set a date range to test in '%Y-%m-%d' format
	start_date='2018-08-01'
	end_date='2018-08-31'
	
	#generate portfolio return over given period as well as a list of weights of holdings
	# and 
	port_return,weights=return_calc(hold_dict,start_date,end_date)
	
	#generate portfolio std dev over given period
	std_dev=port_std_dev(hold_dict,start_date,weights)
	
	#sharpe ratio
	sharpe=(port_return-risk_free_r)/std_dev
	print('portfolio sharpe ratio is '+str(round(sharpe,4)))
	



main()
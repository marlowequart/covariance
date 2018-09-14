'''
Autocorrelation
The variance ratio looks at how the volatility changes over time. If the recent
volatility is higher than longer term, this is likely indicative of a mean reverting period
However if the longer term volatility is higher than recent, this could indicate a trend.
In this way, the variance ratio can be used to determine trends.
Another way to say this is a tool to separate the signal(trend) from the noise.

Given:
1 data set
Data set must be sorted by date from oldest at the top to newest date

Return:
variance_ratio_plot: a graph of the autocorrelation for a given date

want to see how this changes over time and how we might be able to detect a crossover
from sideways to trend.


'''

#for data manipulation
import pandas as pd
import numpy as np
import datetime

#for plot function
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
from scipy import stats

#open csv file, return matrix of data, date in col1, data col2
def import_data(file_name):
	#open the file using pandas, use the first row as the header
	data = pd.read_csv(file_name,header=0)
	return pd.np.array(data[['Date','Close']])
	
def volatility_list(int_retns,timespan):
	# this function returns a list of the volatilities calculated backwards
	# for the given time span for each point of the ndarray.
	# ndarray is an nd_array
	# timespan is an int

	vol_list=[]
	for i in range(len(int_retns)):
		if i<timespan:
			vol_list.append(0)
		else:
			vol_list.append(np.std(int_retns[(i-timespan):i]))
	return vol_list
	
def volatility_sing(int_retns,timespan,idx):
	# this function returns the volatility calculated backwards
	# for the given time span for a single point of the ndarray.
	# int_retns is an nd_array of the daily returns
	# timespan is an int
	# idx is the index to calculate

	return np.std(int_retns[(idx-timespan):idx])
	
	
	
def init_plot(ndarray):
	# Create a correlation matrix, the input is a pandas dataframe with the columns being
	# the data that you want to make the correlation matrix from.
	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	xdata=[datetime.datetime.strptime(ndarray[i][0],'%Y-%m-%d') for i in range(len(ndarray))]
	ydata=[ndarray[i][1] for i in range(len(ndarray))]
	ax1.plot(xdata,ydata)
	ax1.set_xlabel('Date')
	ax1.set_ylabel('Price')
	plt.title('Time Series')
	ax1.grid(True)
	plt.show()
	
def variance_ratio_plot(timespan,volatilities):
	# Create a correlation matrix, the input is a pandas dataframe with the columns being
	# the data that you want to make the correlation matrix from.
	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	ax1.plot(timespan,volatilities)
	ax1.xaxis.set_major_locator(MultipleLocator(50))
	
	# Also plot linear regression line
	gradient, intercept = stats.linregress(timespan,volatilities)
	print(gradient,intercept)
	# lr_x=np.linspace(timespan)
	# lr_y=gradient*lr_x+intercept
	# ax1.plot(timespan,lr_y,'-r')
	
	ax1.set_xlabel('Frequency of Observation')
	ax1.set_ylabel('Volatility')
	plt.title('Variance Ratio')
	ax1.grid(True)
	plt.show()
	
	
def main():
	read_file='GOLD.csv'
	#import_data returns an nd_array
	clean_data=import_data(read_file)
	# print(clean_data[5][0])
	# init_plot(clean_data)
	interday_returns=[((clean_data[i][1]/clean_data[i-1][1])-1) for i in range(1,len(clean_data))]
	interday_returns.insert(0,0)

	# print the variance ratio graph for a given date
	index=8000
	print('date under consideration: '+str(clean_data[index][0]))
	time_lengths=[5,10,20,25,50,100,150,200,250]
	volatilities=[volatility_sing(interday_returns,time,index) for time in time_lengths]
	variance_ratio_plot(time_lengths,volatilities)
	
	


main()
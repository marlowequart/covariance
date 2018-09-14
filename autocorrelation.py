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
Positive slope indicates a trend. The trend could either be downards or upwards.

'''

#for data manipulation
import pandas as pd
import numpy as np
import datetime

#for plot function
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
from scipy import stats
import scipy as sp
import scipy.interpolate

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
	

	# Optional, plot linear regression line
	slope, intercept, r_value, p_value, std_err  = stats.linregress(timespan,volatilities)
	lr_y=[slope*timespan[i]+intercept for i in range(len(timespan))]
	ax1.plot(timespan,lr_y,'-r')
	
	
	ax1.set_xlabel('Frequency of Observation')
	ax1.set_ylabel('Volatility')
	plt.title('Variance Ratio')
	ax1.grid(True)
	plt.show()
	
def var_slope_plot(pri_dataset,idxs,var_slopes,resolution):
	# plot the variance ratio slopes
	
	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	#plot the original data
	xdata=[datetime.datetime.strptime(pri_dataset[i][0],'%Y-%m-%d') for i in range(len(pri_dataset))]
	ydata=[pri_dataset[i][1] for i in range(len(pri_dataset))]
	ax1.plot(xdata,ydata)
	
	#add second axis with variance slopes
	ax2 = ax1.twinx()
	#want to add datapoints to variance slope line for more resolution
	new_dx=len(pri_dataset)/resolution
	new_x=np.linspace(min(idxs),max(idxs),new_dx)
	var_xdata=[datetime.datetime.strptime(pri_dataset[i][0],'%Y-%m-%d') for i in new_x]
	var_ydata=sp.interpolate.interp1d(idxs,var_slopes,kind='cubic')(new_x)
	zeros=[0 for i in range(len(new_x))]
	# print(var_xdata)
	ax2.plot(var_xdata,var_ydata,'-r')
	ax2.plot(var_xdata,zeros,color='c',linestyle='--')
	#set y axis with zero in the middle and +/- the max of the max/min values
	ymax=max(var_slopes)
	ymin=min(var_slopes)
	max_dy=abs(max(ymax,ymin))
	y_range=np.arange(-max_dy,max_dy,max_dy/3.0)
	ax2.set_yticks(y_range)
	
	#draw a vertical line at any zero crossing on the var_xdata
	#get the index for zero crossing
	z_c=np.where(np.diff(np.sign(var_ydata)))[0]
	zc_idx=[new_x[i] for i in z_c]
	z_cross=[datetime.datetime.strptime(pri_dataset[i][0],'%Y-%m-%d') for i in zc_idx]
	#draw lines
	for date in z_cross:
		plt.axvline(x=date, color='k', linestyle='--')
	#shade anything positive light grey
	
	
	ax1.set_xlabel('Date')
	ax1.set_ylabel('Price')
	ax2.set_ylabel('Variance Slope')
	plt.title('Variance Slope and time series')
	ax1.grid(True)
	plt.show()
	
def var_slope(timespan,vols):
	# get the slope of the variance plot
	slope, intercept, r_value, p_value, std_err  = stats.linregress(timespan,vols)
	return slope
	
# Slice sets cuts out the dates before the max/min start date and
# after the min/max end date
def slice_sets(ndarray,start_date,end_date):
	st_dt_num=time.strptime(start_date,'%Y-%m-%d')
	end_dt_num=time.strptime(end_date,'%Y-%m-%d')
	
	#remove values below start date	
	for set in ndarray:
		while time.strptime(set[i][0],'%Y-%m-%d')<st_dt_num:
			set=np.delete(set,i,axis=0)
		break
	new_list_of_sets1.append(set)
	#remove values above end date
	for set in new_list_of_sets1:
		for i in range(len(set)-1,-1,-1):
			while time.strptime(set[i][0],'%Y-%m-%d')>end_dt_num:
				set=np.delete(set,i,axis=0)
				i-=1
			break
		new_list_of_sets2.append(set)
	
	# Return full sliced data sets
	# return new_list_of_sets2
	
	#return only price data, not date info	
	# out_set=[]
	# for set in new_list_of_sets2:
		# mid_set=[]
		# for i in range(len(set)):
			# mid_set.append(set[i][1])
		# out_set.append(mid_set)

	# return [[set[i][1] for i in range(len(set))] for set in new_list_of_sets2]
	
	
def main():
	read_file='NKE.csv'
	#import_data returns an nd_array
	clean_data_init=import_data(read_file)
	#set a date range in '%Y-%m-%d' format
	start_date='1995-1-1'
	end_date='2005-1-1'
	clean_data=slice_set(clean_data_init,start_date,end_date)
	# init_plot(clean_data)
	interday_returns=[((clean_data[i][1]/clean_data[i-1][1])-1) for i in range(1,len(clean_data))]
	interday_returns.insert(0,0)

	# print the variance ratio graph for a given date
	index=1000
	# print('date under consideration: '+str(clean_data[index][0]))
	time_lengths=[5,10,20,25,50,100,150,200,250]
	# volatilities=[volatility_sing(interday_returns,time,index) for time in time_lengths]
	# variance_ratio_plot(time_lengths,volatilities)
	
	# for the whole data set, find the average slope of the variance ratio plot
	# and plot that on the dataset.
	
	# want to have a list of the slopes of the variance plots as y values
	var_slopes=[]
	idxs=[]
	# time step is number of days to step over. Want to use 250 days(1yr) for long term trends
	time_step=250
	# resolution is the level of resolution on the graph so that we can get more fine measurements
	resolution=10
	for i in range(250,len(clean_data),time_step):
		# start the index at a number above the longest time length in order to get a
		# good slope value
		idxs.append(i)
		#generate the variances for the given time lengths
		var_slope_vol=[volatility_sing(interday_returns,time,i) for time in time_lengths]
		#get the slope of the variance ratio plot
		var_slopes.append(var_slope(time_lengths,var_slope_vol))
	#need to get a list of x values of the dates based on time step used
	# print(var_slopes)
	#plot the var slopes on the plot with original data
	var_slope_plot(clean_data,idxs,var_slopes,resolution)


main()
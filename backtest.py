'''
Backtest
This analysis assumes both long and short bets, and the proper choice on long vs short position


Given:
1 data set
Data set must be sorted by date from oldest at the top to newest date

Return:
- variance_ratio_plot: a graph of the autocorrelation for the data set and the crossover
points for the slope of the variance.
- return the dates where the slopes cross over to signal start of trend or start of mean reversion
- measure returns from trading on those signals.
- return percent winning trades, number of consec losses
- return expectancy (odds, # win/losses) and edge (median ammt won/lost)

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
	read = pd.read_csv(file_name,header=0)
	read['Close']=read['Close'].apply(pd.to_numeric, errors='coerce')
	# arr=pd.np.array(read[['Date','Close']])
	return pd.np.array(read[['Date','Close']])
	
	
# Slice sets cuts out the dates before the max/min start date and
# after the min/max end date
def slice_array(ndarray,start_date,end_date):
	st_dt_num=datetime.datetime.strptime(start_date,'%Y-%m-%d')
	end_dt_num=datetime.datetime.strptime(end_date,'%Y-%m-%d')

	#remove values below start date	
	for i in range(len(ndarray)):
		while datetime.datetime.strptime(ndarray[i][0],'%Y-%m-%d')<st_dt_num:
			ndarray=np.delete(ndarray,i,axis=0)
		break
		
	#remove values above end date
	for i in range(len(ndarray)-1,-1,-1):
		while datetime.datetime.strptime(ndarray[i][0],'%Y-%m-%d')>end_dt_num:
			ndarray=np.delete(ndarray,i,axis=0)
			i-=1
		break

	# Return full sliced data sets
	return ndarray
	
	
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
	
def var_slope(timespan,vols):
	# get the slope of the variance plot
	slope, intercept, r_value, p_value, std_err  = stats.linregress(timespan,vols)
	return slope
	
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
	# plot the variance ratio slopes on the same graph of the orig signal
	# plot vertical lines at the points where the variance slope crosses zero
	
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
	
def var_slope_zc(pri_dataset,idxs,var_slopes,resolution):
	# this function returns a list of the zero crossings of the variance slope
	# also a list of +1.0 and -1.0 is returned
	# if the slope crosses from neg to pos (+1.0) or pos to neg (-1.0)
	
	#want to add datapoints to variance slope line for more resolution
	new_dx=len(pri_dataset)/resolution
	new_x=np.linspace(min(idxs),max(idxs),new_dx)
	var_ydata=sp.interpolate.interp1d(idxs,var_slopes,kind='cubic')(new_x)
		
	#draw a vertical line at any zero crossing on the var_xdata
	#get the index for zero crossings. this index is in relation to the primary dataset
	z_c=np.where(np.diff(np.signbit(var_ydata)))[0]
	zc_idx=[new_x[i] for i in z_c]
	z_cross=[datetime.datetime.strptime(pri_dataset[i][0],'%Y-%m-%d') for i in zc_idx]
	#zcs: 6,59,86,124(pos to neg),142
	
	# print(np.where(np.diff(np.signbit(var_ydata))))
	# print(new_x[-1])
	# print(len(pri_dataset))
	# print(len(var_slopes))
	# print(len(var_ydata))
	# print(len(zc_idx))
	# print(var_ydata[125])
	
	# generate slope change
	slope_change=[]
	for i in range(len(z_c)):
		if i == 0:
			half_idx_delta_low=int(z_c[i]/2.0)
		else:
			half_idx_delta_low=int((z_c[i]-z_c[i-1])/2.0)
		# print(z_c[i]-half_idx_delta_low)
		# print(var_ydata[z_c[i]-half_idx_delta_low])

		if var_ydata[z_c[i]-half_idx_delta_low] < 0:
			slope_change.append(1.0)
		else:
			slope_change.append(-1.0)
		# slope_change.append(z_c[i]-half_idx_delta_low)
		# slope_change.append(var_ydata[z_c[i]-5])
		# slope_change.append(var_ydata[int(idx-5)])
		# print(var_ydata[int(idx)])
		# slope_change.append(var_ydata[int(idx)])
		# slope_change.append(var_slopes[int(idx)+5])
		# if var_slopes[idx-5]


	return z_cross,slope_change,zc_idx
	
	
def main():
	read_file='AAPL.csv'
	#import_data returns an nd_array
	clean_data_init=import_data(read_file)
	
	#set a date range in '%Y-%m-%d' format
	start_date='1985-1-1'
	end_date='2001-9-5'
	clean_data=slice_array(clean_data_init,start_date,end_date)

	# print(clean_data)

	# init_plot(clean_data)
	interday_returns=[((float(clean_data[i][1])/float(clean_data[i-1][1]))-1) for i in range(1,len(clean_data))]
	interday_returns.insert(0,0)

	# print the variance ratio graph for a given date
	# index=1000
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
	###############
	# plot the var slopes on the plot with original data
	###############
	var_slope_plot(clean_data,idxs,var_slopes,resolution)
	
	# generate a list of the zero crossings of the variance slope and slope change at those spots
	# the zero crossings list is the dates of the zero crossing
	# the slope crossing list contains transitions from neg to pos (+1.0) or pos to neg (-1.0)
	zcs,slope,date_index=var_slope_zc(clean_data,idxs,var_slopes,resolution)
	# print([datetime.datetime.strftime(zcs[i],'%Y-%m-%d') for i in range(len(zcs))])
	# print(slope)
	
	# if the first zero crossing is from positive to negative (-1.0),
	# remove it to make the first zero crossing an initiate trade signal
	if slope[0] == -1.0:
		slope=slope[1:]
		zcs=zcs[1:]
	
	# generate a list of the dates that were trade signals(slope change from neg to pos)
	open_trade_d=[]
	open_trade_idx=[]
	close_trade_d=[]
	close_trade_idx=[]
	for i in range(len(slope)):
		if slope[i] == 1.0:
			open_trade_d.append(zcs[i])
			open_trade_idx.append(date_index[i])
		elif slope[i] == -1.0:
			close_trade_d.append(zcs[i])
			close_trade_idx.append(date_index[i])

	
	# generate a list of the returns from making trades on those dates
	returns=[]
	trade_dates=[]
	price_adv=[]
	
	# print(zcs[3])
	# print(date_index[3])
	# print(clean_data[date_index[3]][0])
	num_trades=min(len(open_trade_idx),len(close_trade_idx))
	for i in range(num_trades):
		trade_dates.append('open trade signal on '+datetime.datetime.strftime(open_trade_d[i],'%Y-%m-%d')+', close trade signal on '+datetime.datetime.strftime(close_trade_d[i],'%Y-%m-%d'))
		# get holding time
		elapsed_time=(close_trade_d[i]-open_trade_d[i]).days/365
		# get annualized return on each trade
		cagr=100*(((clean_data[close_trade_idx[i]][1]/clean_data[open_trade_idx[i]][1])**(1/elapsed_time))-1.0)
		returns.append(abs(round(cagr,2)))
		
		#get actual return on each trade
		price_adv.append(abs(clean_data[close_trade_idx[i]][1]-clean_data[open_trade_idx[i]][1]))
	for i in range(len(trade_dates)):
		print(trade_dates[i])
		print('return on trade: '+str(returns[i]))
		
	#sum of total price gains
	price_gains=sum(price_adv)
	st_dt=datetime.datetime.strptime(start_date,'%Y-%m-%d')
	end_dt=datetime.datetime.strptime(end_date,'%Y-%m-%d')
	eta=(end_dt-st_dt).days/365
	# compare the cagr using trade method vs just buy and hold
	cagr_trade=100*(((price_gains/clean_data[open_trade_idx[0]][1])**(1/eta))-1.0)
	cagr_bh=100*(((clean_data[-1][1]/clean_data[0][1])**(1/eta))-1.0)
	print('cagr using trading method: '+str(round(cagr_trade,2)))
	print('cagr using buy and hold method: '+str(round(cagr_bh,2)))
	
	# last thing is to come up with edge offered by this strategy
	# assume every trade is a win, ie edge is 1.0
	# what is the payout rate?
	
main()

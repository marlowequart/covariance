'''
Use this script to create candle plots of data.



'''

import pandas as pd
import re
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.finance import candlestick2_ochl
from matplotlib.finance import volume_overlay2
import matplotlib.ticker as ticker
from matplotlib import gridspec



#open csv file, return the data in a pandas dataframe
def import_data(file_name):
	#open the file using pandas, use the first row as the header
	data = pd.read_csv(file_name,header=0)
	
	#remove Adj Close column
	data=data.drop('Adj Close', axis=1)
	
	return data

def gen_plot(dataframe,startidx,endidx):
	#dataframe is a pandas dataframe with open, high, low, close and volume for each time interval
	
	open=dataframe['Open'][startidx:endidx].tolist()
	high=dataframe['High'][startidx:endidx].tolist()
	low=dataframe['Low'][startidx:endidx].tolist()
	close=dataframe['Close'][startidx:endidx].tolist()
	volume=dataframe['Volume'][startidx:endidx].tolist()
	
	date=dataframe['Date'][startidx:endidx].tolist()
	num_ticks=6

	def mydate(x,pos):
		try:
			return date[int(x)]
		except IndexError:
			return ''
	
	#####
	# plot just price
	#####
	'''
	fig = plt.figure()
	ax = plt.subplot()
	candlestick2_ochl(ax,open,low,high,close,width=0.5,colorup='b',colordown='r',alpha=0.75)
	ax.xaxis.set_major_locator(ticker.MaxNLocator(num_ticks))
	ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
	fig.autofmt_xdate()
	fig.tight_layout()
	ax.set_ylabel('Price')
	ax.set_xlabel('Date')
	ax.set_xlim(-1.0,len(date)-1.0)
	ax.xaxis.set_major_locator(ticker.MaxNLocator(num_ticks))
	ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
	ax.grid()
	plt.show()
	'''
	
	#####
	# plot price with volume by price
	#####
	fig = plt.figure()
	
	ax4 = plt.subplot()
	candlestick2_ochl(ax4,open,low,high,close,width=0.5,colorup='b',colordown='r',alpha=0.75)
	ax4.xaxis.set_major_locator(ticker.MaxNLocator(num_ticks))
	ax4.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
	fig.autofmt_xdate()
	fig.tight_layout()
	ax4.set_ylabel('Price')
	ax4.set_xlabel('Date')
	ax4.set_xlim(-1.0,len(date)-1.0)
	ax4.grid()
	# plt.show()
	
	#plot horizontal bar chart with volume
	#generate volume by price, using value at close
	min_price=min(close)
	max_price=max(close)
	
	
	###############
	###############
	#set the nbins for qty of volume bars
	nbins=75
	barheight=5
	num_ticks_vol=5
	###############
	###############
	
	
	dy=(max_price-min_price)/nbins
	ys = np.arange(min_price,max_price+dy,dy).round(decimals=2)
	pairs=[]
	bins=[0 for x in range(len(ys))]
	for i in range(len(close)):
		for z in range(len(ys)-1):
			if ys[z] <= close[i] < ys[z+1]:
				bins[z]=bins[z]+volume[i]
				
				
	def setbins(x,pos):
		try:
			return ys[int(x)]
		except IndexError:
			return ''
	
	ax3 = ax4.twinx()
	ax3 = ax4.twiny()
	# ax3.yaxis.set_major_formatter(ticker.FuncFormatter(setbins))
	ax3.barh(ys,bins,align='center',height=barheight,color='gray',alpha=0.5)
	# ax3.set_yticks(ys)
	# ax3.yaxis.set_major_locator(ticker.MaxNLocator(num_ticks_vol))
	ax3.yaxis.set_visible(False)
	ax3.xaxis.set_visible(False)
	# ax3.set_yticklabels(ys)
	# ax3.grid()
	plt.show()
	
	
	#####
	# plot price with volume in second view below
	#####
	'''
	fig = plt.figure()
	gs = gridspec.GridSpec(2,1, height_ratios=[3,1])
	ax1 = plt.subplot(gs[0])
	ax2 = plt.subplot(gs[1])
	candlestick2_ochl(ax1,open,low,high,close,width=0.5,colorup='b',colordown='r',alpha=0.75)
	volume_overlay2(ax2,close,volume,width=0.5,colorup='b',colordown='r')
	ax1.xaxis.set_major_locator(ticker.MaxNLocator(num_ticks))
	ax1.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
	fig.autofmt_xdate()
	fig.tight_layout()
	ax1.set_ylabel('Price')
	ax2.set_ylabel('Volume')
	ax2.set_xlabel('Date')
	ax1.set_xlim(-1.0,len(date)-1.0)
	ax2.set_xlim(-1.0,len(date)-1.0)
	ax2.xaxis.set_major_locator(ticker.MaxNLocator(num_ticks))
	ax2.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))
	ax1.grid()
	ax2.grid()
	plt.show()
	'''
	
def main():
	#####
	# Change the file name here
	#####
	file_name='SP500.csv'
	
	df=import_data(file_name)
	
	# print(df.head())
	
	#####
	# modify the dataframe and plot it
	#####
	#set the date
	start_idx=int(df.index[df['Date'] == '2018-01-03'][0])
	# print('start_idx date check: idx: '+str(start_idx)+', date: '+str(df['Date'][start_idx]))
	end_idx=int(df.index[df['Date'] == '2018-08-31'][0])
	# print('end_idx date check: idx: '+str(end_idx)+', date: '+str(df['Date'][end_idx]))
	
	#plot it
	gen_plot(df,start_idx,end_idx)
	
main()

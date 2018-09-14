'''
Correlation Matrix
The plot output by this script shows the matrix of correlations between individual items
in the datasets.

Given:
n data sets of price values over a period of time in csv files
Data sets must be sorted by date from oldest at the top to newest date

Return: matrix showing correlation between the data sets


When adjusting the positions to be displayed in the matrix,
the following lines must be updated.
Check areas with ########## breakpoints:
			labels to match positions
			number of positions from 0 to n
			file names
			number of data sets
			include all sets
			include all sets

'''
#for data manipulation
import pandas as pd
import numpy as np
import time

#for correlation plot function
from matplotlib import pyplot as plt
from matplotlib import cm as cm
import seaborn as sns


#open csv file, return matrix of data, date in col1, data col2
def import_data(file_name):
	#open the file using pandas, use the second row as the header
	data = pd.read_csv(file_name,header=0)
	return pd.np.array(data[['Date','Close']])
	
def max_min_date(list_of_sets):
	#the purpose of this function is to return the highest low start date
	min_date=[]
	cnt=0
	for i in list_of_sets:
		# print('for symbol '+str(cnt)+' start date is '+str(time.strptime(i[0][0],'%Y-%m-%d')))
		min_date.append(time.strptime(i[0][0],'%Y-%m-%d'))
		cnt+=1
	
	return str(time.strftime('%Y-%m-%d',max(min_date)))

def min_max_date(list_of_sets):
	#the purpose of this function is to return the highest low start date
	max_date=[]
	for i in list_of_sets:
		max_date.append(time.strptime(i[-1][0],'%Y-%m-%d'))
	
	return str(time.strftime('%Y-%m-%d',min(max_date)))
	
# Slice sets cuts out the dates before the max/min start date and
# after the min/max end date
def slice_sets(list_of_sets,start_date,end_date):
	st_dt_num=time.strptime(start_date,'%Y-%m-%d')
	end_dt_num=time.strptime(end_date,'%Y-%m-%d')
	
	new_list_of_sets1=[]
	new_list_of_sets2=[]
	#remove values below start date	
	for set in list_of_sets:
		for i in range(len(set)):
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
	out_set=[]
	for set in new_list_of_sets2:
		mid_set=[]
		for i in range(len(set)):
			mid_set.append(set[i][1])
		out_set.append(mid_set)

	return [[set[i][1] for i in range(len(set))] for set in new_list_of_sets2]
	
	
def correlation_matrix(df,labels):
	# Create a correlation matrix, the input is a pandas dataframe with the columns being
	# the data that you want to make the correlation matrix from.

	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	

	###############
	# Use matplotlib colormap
	###############
	# create colormap, 'binary' is b&w, 'jet' is blue to red
	# 30 represents number of color divisions
	
	# cmap = cm.get_cmap('jet', 20)
	# cax = ax1.imshow(df.corr(), interpolation='none', cmap=cmap)
	# fig.colorbar(cax, ticks=np.arange(-1,1.1,0.1))
	############	
	# must change number of ticks to match number of positions
	############	
	# ax1.set_xticks([0,1,2,3,4])
	# ax1.set_yticks([0,1,2,3,4])
	# ax1.set_xticklabels(labels,fontsize=12)
	# ax1.set_yticklabels(labels,fontsize=12)
	
	##########
	# use seaborn heatmap
	##########
	corr = df.corr()
	ax1=sns.heatmap(corr, annot=True)
	
	


	# Add colorbar, make sure to specify tick locations to match desired ticklabels
	ax1.grid(which='major', axis='both')
	plt.title('Correlations')
	plt.show()
	
	
def main():
	#############	
	# define file names
	#############	
	read_file1='SWKS.csv'
	read_file2='AAPL.csv'
	read_file3='SYF.csv'
	read_file4='SILVER.csv'
	read_file5='GOLD.csv'

	#############	
	# create matrix of imported data
	#############	
	set1=import_data(read_file1)
	set2=import_data(read_file2)
	set3=import_data(read_file3)
	set4=import_data(read_file4)
	set5=import_data(read_file5)
	# set6=import_data(read_file6)
	
	# print(set1[:10])
	# print(set2[:10])
	# print(set3[:10])
	#############	
	# create list of matrices
	#############	
	sets=[set1,set2,set3,set4,set5]
	
	# For correlations and covariance we want to look at the same date range
	# slice out the dates we do not want to consider
	# find maximal minimum date in all sets
	start_date=max_min_date(sets)
	# find minimum of maximum date in all sets
	end_date=min_max_date(sets)
	print('date ranges under consideration: '+start_date+' to '+end_date)
	
	# create new sets with only specified date ranges and only return price data.
	new_list_sets=slice_sets(sets,start_date,end_date)
	
	# print correlation matrix
	df = pd.DataFrame(new_list_sets)
	df = df.transpose()
	
	#############	
	# list all datasets included in plot, change labels to match positions
	#############
	labels=['SWKS','AAPL','SYF','SILVER','GOLD']	
	df.columns = labels
	corr = df.corr()
	# print(corr)
	correlation_matrix(df,labels)
	


	
	
main()
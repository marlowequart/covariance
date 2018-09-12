'''
Correlation Matrix
The plot output by this script shows the matrix of correlations between individual items
in the datasets.

Given: n data sets of price values over a period of time

Return: matrix showing correlation between the data sets

'''
#for data manipulation
import pandas as pd
import numpy as np
import time

#for correlation plot function
from matplotlib import pyplot as plt
from matplotlib import cm as cm



#open csv file, return matrix of data, date in col1, data col2
def import_data(file_name):
	#open the file using pandas, use the second row as the header
	data = pd.read_csv(file_name,header=1)
	return pd.np.array(data[['header row 2 column 1','header row 2 column 3']])
	
def max_min_date(list_of_sets):
	#the purpose of this function is to return the highest low start date
	min_date=[]
	for i in list_of_sets:
		min_date.append(time.strptime(i[0][0],'%m/%d/%y'))
	
	return str(time.strftime('%m/%d/%y',max(min_date)))

def min_max_date(list_of_sets):
	#the purpose of this function is to return the highest low start date
	max_date=[]
	for i in list_of_sets:
		max_date.append(time.strptime(i[-1][0],'%m/%d/%y'))
	
	return str(time.strftime('%m/%d/%y',min(max_date)))
	
# Slice sets cuts out the dates before the max/min start date and
# after the min/max end date
def slice_sets(list_of_sets,start_date,end_date):
	st_dt_num=time.strptime(start_date,'%m/%d/%y')
	end_dt_num=time.strptime(end_date,'%m/%d/%y')
	
	new_list_of_sets1=[]
	new_list_of_sets2=[]
	#remove values below start date	
	for set in list_of_sets:
		for i in range(len(set)):
			while time.strptime(set[i][0],'%m/%d/%y')<st_dt_num:
				set=np.delete(set,i,axis=0)
			break
		new_list_of_sets1.append(set)
	#remove values above end date
	for set in new_list_of_sets1:
		for i in range(len(set)-1,-1,-1):
			while time.strptime(set[i][0],'%m/%d/%y')>end_dt_num:
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
	
	
def correlation_matrix(df):
	# Create a correlation matrix, the input is a pandas dataframe with the columns being
	# the data that you want to make the correlation matrix from.

	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	
	# create colormap, 'binary' is b&w, 'jet' is blue to red
	# 30 represents number of color divisions
	cmap = cm.get_cmap('jet', 30)
	
	
	cax = ax1.imshow(df.corr(), interpolation='none', cmap=cmap, )
	fig.colorbar(cax, ticks=np.arange(-1,1.1,0.1))
	labels=['set1','set2','set3']
	
	ax1.grid(which='major', axis='both')
	plt.title('Set Correlation')
	ax1.set_xticks([0,1,2])
	ax1.set_yticks([0,1,2])
	ax1.set_xticklabels(labels,fontsize=12)
	ax1.set_yticklabels(labels,fontsize=12)
	# Add colorbar, make sure to specify tick locations to match desired ticklabels
	plt.show()
	
	
def main():
	# define file names
	read_file1='csv_test_data_1.csv'
	read_file2='csv_test_data_2.csv'
	read_file3='csv_test_data_3.csv'
	
	# create matrix of imported data
	set1=import_data(read_file1)
	set2=import_data(read_file2)
	set3=import_data(read_file3)
	
	# create list of matrices
	sets=[set1,set2,set3]
	
	# For correlations and covariance we want to look at the same date range
	# slice out the dates we do not want to consider
	# find maximal minimum date in all sets
	start_date=max_min_date(sets)
	# find minimum of maximum date in all sets
	end_date=min_max_date(sets)
	# print('date ranges under consideration: '+start_date+' to '+end_date)
	
	# create new sets with only specified date ranges and only return price data.
	new_list_sets=slice_sets(sets,start_date,end_date)
	
	# print correlation matrix
	df = pd.DataFrame(new_list_sets)
	df = df.transpose()
	df.columns = ['set1','set2','set3']
	# print(df.corr())
	correlation_matrix(df)
	

	
	
main()
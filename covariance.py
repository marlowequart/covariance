'''
Variance, Covariance, std deviation

Sandard Deviation (sigma) is used to quantify the ammount of variation or dispersion of
a set of data values from its mean. Large std dev indicates the data points are spread out over wider
range of values. Std Deviation is known as historical volatility, used to estimate expected
volatility.

Variance (sigma squared) is a measure of the dispersion of a set of datapoints around
their mean value. Variance measures the variability from an average (volatility).
Variance uses squares because it weights outliers more heavily than data near the mean.

Covariance is a measure of the degree to which returns on two risky assets move in tandem.
Positive covariance means the asset returns move together and negative means they move inversely.
Larger positive numbers mean higher correlation, lower negative numbers means greater inversion.
Covariance is closely related to correlation, but covariance factors in the standard deviation.

Given1: n data sets

Return1: Variance and std deviation of data sets and covariance between individual data sets



'''
import pandas as pd
import numpy as np
import time


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


	


def variance(a_set):
	# Variance (sigma squared) is a measure of the dispersion of a set of datapoints around
	# their mean value. Variance measures the variability from an average (volatility).
	# Variance uses squares because it weights outliers more heavily than data near the mean.
	
	# std dev (sigma) is the ammount of variation or dispersion of a set of data values from its mean.
	# std dev measures the variability from an average (volatility).
	
	#pull out the price data column
	prices=[]
	for row in a_set:
		prices.append(row[1])
	# return variance and std deviation
	return np.var(prices),np.std(prices)
	




def main():
	# define file names
	read_file1='csv_test_data_1.csv'
	read_file2='csv_test_data_2.csv'
	read_file3='csv_test_data_3.csv'
	
	# create matrix of imported data
	set1=import_data(read_file1)
	set2=import_data(read_file2)
	set3=import_data(read_file3)
	
	# Variance and std deviation can be performed for each set individually
	# this gives a measure of the volatility.
	var1,std_dev1=variance(set1)
	print('Variance is ',var1)
	print('Std Dev is ', std_dev1)
	
	
	
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
	
	# run covariance of two sets
	cov1=np.cov(new_list_sets[1],new_list_sets[2])[0][1]
	print('Covariance set2 to set3 is: ',cov1)
	
	
	
main()
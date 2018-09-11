'''
Variance, Covariance, std deviation

Variance (sigma squared) is a measure of the dispersion of a set of datapoints around
their mean value. Variance measures the variability from an average (volatility).

Covariance is a measure of the degree to which returns on two risky assets move in tandem.
Positive covariance means the asset returns move together and negative means they move inversely.
Covariance is closely related to correlation, but covariance factors in the standard deviation.

Given: n data sets

Return: Variance, Covariance, std deviation between data sets

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
	

	return new_list_of_sets2


	


def variance(a_set):
	#pull out the price data column
	prices=[]
	for row in a_set:
		prices.append(row[1])
	return np.var(prices),np.std(prices)
	


	
	
	
def covariance(list_of_sets):
	#covariance
	list=list_of_sets





def main():
	# define file names
	read_file1='csv_test_data_1.csv'
	read_file2='csv_test_data_2.csv'
	read_file3='csv_test_data_3.csv'
	
	# create matrix of imported data
	set1=import_data(read_file1)
	set2=import_data(read_file2)
	set3=import_data(read_file3)
	
	# Variance can be performed for each set individually
	# this gives a measure of the volatility
	var1,std_dev1=variance(set1)
	print('Variance is ',var1)
	print('Std Dev is ', std_dev1)
	
	
	
	# create list of matrices
	sets=[set1,set2,set3]
	
	# For correlations and covariance we want to look at the same date range
	# slice out the dates we do not want to consider
	#find maximal minimum date in all sets
	start_date=max_min_date(sets)
	#find minimum of maximum date in all sets
	end_date=min_max_date(sets)
	# print('date ranges under consideration: '+start_date+' to '+end_date)
	#create new sets with only specified date ranges
	new_list_sets=slice_sets(sets,start_date,end_date)
	
	
	# run variance, covariance and std dev
	
#	covariance=covariance(sets)
#	std_dev=std_deviation(sets)
	
	# Print results
#	print('variance is %d', % variance)
#	print('covariance is %d', % covariance)
#	print('std deviation is %d', % std_dev)
	
	
main()
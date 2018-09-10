'''
Variance, Covariance, std deviation

Given: n data sets

Return: Variance, Covariance, std deviation between data sets

'''
import pandas as pd



#open csv file, return matrix of data, date in col1, data col2
def import_data(file_name)
	#open the file using pandas, use the second row as the header
	data = pd.read_csv(file_name,header=1)
	return data[['header row 2 column 1','header row 2 column 3']]



# list_of_sets is a list of 2 col matrices with date and data
def variance(list_of_sets)

def covariance(list_of_sets)

def std_deviation(list_of_sets)



def main()
	# define file names
	read_file1='csv_test_data_1.csv'
	read_file2='csv_test_data_2.csv'
	read_file3='csv_test_data_3.csv'
	
	# create matrix of imported data
	set1=import_data(read_file1)
	set2=import_data(read_file2)
	set3=import_data(read_file3)
	
	print(set1)
	'''
	# create list of matrices
	sets=[set1,set2,set3]
	
	# run variance, covariance and std dev
	variance=variance(sets)
	covariance=covariance(sets)
	std_dev=std_deviation(sets)
	
	# Print results
	print('variance is %d', % variance)
	print('covariance is %d', % covariance)
	print('std deviation is %d', % std_dev)
	'''
	
main()
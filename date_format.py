'''
Format and sort by date in csv file

Given:
csv file with Date column in one of following formats:
case 0: %m/%d/%y
case 1: %m/%d/%Y

Return:
CSV file with Date in %Y-%m-%d format that is sorted by date
from oldest to newest date

'''
#for data manipulation
import pandas as pd
import time



#open csv file, return dataframe of data with updated date
def import_data(file_name):
	#open the file using pandas DataFrame, use the first row as the header
	data = pd.read_csv(file_name,header=0)
	
	#this converts the date column to the standard pandas format, %Y-%m-%d
	data['Date']=pd.to_datetime(data.Date)

	#this sorts the data by date from earliest to latest date
	data=data.sort_values(by=['Date'],ascending=True)

	return data
	
	
	
def main():
	# define file names
	read_file='SILVER.csv'
	
	#######################
	# Acceptable date formats:
	# case 0: %m/%d/%y
	# case 1: %m/%d/%Y
	#######################
	
	updated_data=import_data(read_file)
	
	# write over existing csv file with the new file that has the adjusted date format
	updated_data.to_csv(read_file,sep=',', index=False)
	
	
main()
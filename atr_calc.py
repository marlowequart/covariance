'''
Use this script to calculate the atr of a stock based on data in the .csv file.


Only need to change symbol at beginning of main and length of atr you wish
to calculate.

csv file must be in ascending order by date

'''

import pandas as pd
import re
# ~ from yahoofinancials import YahooFinancials as yf
# ~ import numpy as np
# ~ import datetime
# ~ from datetime import timedelta
# ~ from openpyxl import load_workbook


#open csv file, return dataframe of the timespan under consideration
#only need to return date, high, low

def import_data(file_name,timespan):
	#open the file using pandas, use the first row as the header
	data = pd.read_csv(file_name,header=0)
	
	#Slice the dataframe to the number of days under consideration
	df = data[['Date','High','Low','Close']][-timespan-1:]
	
	print(df['Date'].iloc[-1])
	
	return df

def main():
	
	#####
	# insert name of symbol under consideration
	#####
	file_name='ACGL.csv'
	timespan=10
	
	table=import_data(file_name,timespan)
	
	
	daily_atr=[]
	for i in range(1,len(table)):
		one=round(float(table.iloc[i]['High'])-float(table.iloc[i]['Low']),4)
		two=round(float(table.iloc[i]['High'])-float(table.iloc[i-1]['Close']),4)
		three=round(float(table.iloc[i-1]['Close'])-float(table.iloc[i]['Low']),4)
		daily_atr.append(max(one,two,three))
	
	atr=round(sum(daily_atr)/timespan,4)
	
	print()
	print(str(timespan)+' day avg true range for '+re.findall(r"^([^.csv]*).*",file_name)[0]+' is '+str(atr))
	print()
main()

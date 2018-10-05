'''
This script is used to pull historical price data from yahoo finance
and update the data on an existing csv file from yahoo finance.



'''

import pandas as pd
from yahoofinancials import YahooFinancials as yf
import numpy as np
import datetime
from datetime import timedelta
# ~ from openpyxl import load_workbook


#open csv file, return list of symbols
def import_data(file_name):
	#open the file using pandas, use the first row as the header
	data = pd.read_csv(file_name,header=0)
	
	#get the last date in the csv file
	last_day=data['Date'].iloc[-1]
	
	#get yesterdays date
	today=datetime.datetime.today() - timedelta(1)
	today_str=datetime.datetime.strftime(today,'%Y-%m-%d')
	
	
	return last_day,today_str,data



def save_data():
	#Save the data as a .csv file
	return

def main():
	
	# import the data from an existing file
	# generate the latest date in the file
	file_name='AAPL.csv'
	sym='AAPL'
	recent_date,today_date,df=import_data(file_name)
	
	print(recent_date,today_date)
	return
	
	#Update the companies data
	print('now updating data')
	
	data=yf(sym)
	historical_prices = data.get_historical_price_data(today_date, recent_date, 'daily')
	print(historical_prices[sym]['firstTradeDate']['formatted_date'])
	print(type(historical_prices))
		
		
	
	#format the date in a simple format
	# ~ doc['Date'] = [today.date() for today in doc['Date']]
	
	#Save the data to csv file
	print('saving data')
	# ~ save_data()
	

main()
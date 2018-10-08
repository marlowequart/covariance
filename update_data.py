'''
This script is used to pull historical price data from yahoo finance
and update the data on an existing csv file from yahoo finance.

Only need to change symbol at beginning of main

'''

import pandas as pd
from yahoofinancials import YahooFinancials as yf
import datetime
from datetime import timedelta



#open csv file, return important dates and pandas dataframe of csv file
def import_data(file_name):
	#open the file using pandas, use the first row as the header
	data = pd.read_csv(file_name,header=0)
	
	#get the last date in the csv file
	last_day=data['Date'].iloc[-1]
	
	#get yesterdays date
	today=datetime.datetime.today() - timedelta(1)
	today_str=datetime.datetime.strftime(today,'%Y-%m-%d')
	
	#want to check data for duplicate dates and remove any duplicates
	
	
	return last_day,today_str,data



def main():
	
	# import the data from an existing file
	# generate the latest date in the file
	
	#####
	# Change the symbol here
	#####
	file_name='ACGL.csv'
	sym='ACGL'
	
	recent_date,today_date,df=import_data(file_name)
	
	# ~ print(recent_date,today_date)
	
	#Update the companies data
	print('now updating data')
	
	data=yf(sym)
	historical_prices = data.get_historical_price_data(recent_date, today_date, 'daily')
	
	new_data_df=pd.DataFrame(historical_prices[sym]['prices'])
	
	new_data_df=new_data_df[['formatted_date','open','high','low','close','adjclose','volume']]
	new_data_df=new_data_df.rename(index=str,columns={'formatted_date':'Date','open':'Open','high':'High','low':'Low','close':'Close','adjclose':'Adj Close','volume':'Volume'})
	
	#need to make this part better, can get repeated dates on here
	final_df=df.append(new_data_df[1:])
	
	# ~ print(df.tail())
	# ~ print(new_data_df.tail())
	# ~ print(final_df.tail())
	
	
	#Save the data to csv file
	print('saving data')
	
	print(str(len(new_data_df)-1)+' rows added to file. Old num rows = '+str(len(df))+'. New num rows = '+str(len(final_df)))
	print('Old end date: '+str(df['Date'].iloc[-1])+'. New end date: '+str(final_df['Date'].iloc[-1]))
	final_df.to_csv(file_name, index=False, float_format='%.5f')
	

main()

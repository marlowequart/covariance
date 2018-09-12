'''
Portfolio weight

Given: positions and sizes

Return: matrix of percentage weights of each position

'''
from yahoofinancials import YahooFinancials as yf




# Here symbols input into update_quote strings of the actual symbol. 
# update_quote will pull the current price for the symbol and return that price 
# the function that calls update_quote is responsible for putting the data in the right place. 
def update_quote(symbols): 
	pull_data = yf(symbols) 
	all_data = pull_data.get_stock_price_data(reformat=True)
	current_price = [all_data[sym]['regularMarketPrice'] for sym in symbols]
	return current_price 

	
	
def main():
	gold=3
	#Gold: XAUUSD=X
	silver=157
	#Silver: XAGUSD=X
	AAPL=105
	SYF=699
	MHK=125
	NKE=40

	holdings=[gold,silver,AAPL,SYF,MHK,NKE]
	#for implementation use the following
	# prices=update_quote(['XAUUSD=X','XAGUSD=X','AAPL','SYF','MHK','NKE'])
	
	#for test use the values below
	prices=[1209.10,14.17,223.85,32.44,189.74,82.63]
	# print(prices)
	
	position_val=[a*b for a,b in zip(holdings,prices)]
	total_val=sum(position_val)
	# for i in len(holdings):
		# total_val=total_val+holdings[i]*prices[i]

	# print(total_val)
	weights=[a/total_val for a in position_val]
	print(weights)








main()
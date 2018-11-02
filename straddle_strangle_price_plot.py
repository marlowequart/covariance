'''
Straddle/Strangle Plots

Given: Option price data
# Spot Price: s0


# long put
strikeprice_long_put = 32.5
premium_long_put = 1.80
long_put='long_put'

# long call
strikeprice_long_put = 32.5
premium_long_put = 1.80
long_put='long_put'


# Range of stock prices at expiration
sT = np.arange(10,60,1)


Return:
All the plots of the individual options as well as the plot of the spread
the max profit and loss

'''

#for data manipulation
import numpy as np
import datetime
import seaborn
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")


def option_payoff (sT, strike_price, premium,o_type):
	if o_type == 'long_call':
		return np.where(sT>strike_price, sT-strike_price, 0)-premium
	elif o_type == 'short_call':
		opt = np.where(sT>strike_price, sT-strike_price, 0)-premium
		return opt*-1.0
	elif o_type == 'long_put':
		return np.where(sT<strike_price, strike_price-sT, 0)-premium
	elif o_type == 'short_put':
		opt = np.where(sT<strike_price, strike_price-sT, 0)-premium
		return opt*-1.0


def plot_option(sT,option_payoff,title):
	#sT is the ndarray of possible stock prices we are graphing
	#option_payoff is the ndarray of option payoffs
	#title is the graph title
	fig, ax = plt.subplots()
	ax.spines['bottom'].set_position('zero')
	ax.plot(sT,option_payoff, color='b')
	ax.set_title(title)
	plt.xlabel('Stock Price')
	plt.ylabel('Profit & Loss')
	plt.show()


def main():
	############
	#
	# Option price data input
	# Oct 19 expiration nflx
	# 
	############

	# Spot Price
	s0 = 346.4

	# long put
	strikeprice_long_put = 345.0
	premium_long_put = 16.5
	long_put='long_put'
	
	# long call
	strikeprice_long_call = 345.0
	premium_long_call = 18.5
	long_call='long_call'

	# Range of stock prices at expiration
	sT = np.arange(225,525,5)


	#####
	# long put payoff
	#####
	long_put_payoff = option_payoff(sT,strikeprice_long_put,premium_long_put,long_put)
	title='long 32.5 put'
	# ~ plot_option(sT,long_put_payoff,title)
	
	#####
	# long call payoff
	#####
	long_call_payoff = option_payoff(sT,strikeprice_long_call,premium_long_call,long_call)
	title='long 32.5 call'
	# ~ plot_option(sT,long_put_payoff,title)


	#####
	# straddle payoff
	#####
	straddle_payoff = long_put_payoff+long_call_payoff
	title='Straddle payoff'
	# ~ plot_option(sT,Butterfly_spread_payoff,title)
	low_zero=np.where(straddle_payoff == 0)[0][0]
	high_zero=np.where(straddle_payoff == 0)[0][1]
	
	
	
	#####
	# Print profit/loss
	#####
	profit = max(straddle_payoff)
	loss = min(straddle_payoff)
	

	print()
	print("Cost: %.2f" %-loss)
	# ~ print ("Max Profit: %.2f" %profit)
	# ~ print ("Max Loss: %.2f" %loss)
	print('strike: '+str(s0))
	print('low breakeven: '+str(sT[low_zero]))
	print('high breakeven: '+str(sT[high_zero]))
	print()


	#####
	# Print all options and payoff on one plot
	#####
	fig, ax = plt.subplots()
	ax.spines['bottom'].set_position('zero')
	ax.plot(sT, straddle_payoff ,color='b', label= 'Straddle Payoff')
	ax.plot(sT, long_put_payoff, '--', color='r', label='long put')
	ax.plot(sT, long_call_payoff, '--', color='g', label='long call')
	plt.legend()
	plt.xlabel('Stock Price')
	plt.ylabel('Profit & Loss')
	plt.show()







main()

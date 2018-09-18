'''
Long Call Butterfly Plots

Given: Option price data
# Spot Price: s0

# Long Call
higher_strikeprice_long_call = 35
premium_higher_strike_long_call = 0.85
higher_call='long_call'

lower_strikeprice_long_call=30
premium_lower_strike_long_call = 3.15
lower_call='long_call'

# Short Call
strikeprice_short_call = 32.5
premium_short_call = 1.80
short_call='short_call'

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
	# 
	############

	# Spot Price
	s0 = 40

	# Long Call
	higher_strikeprice_long_call = 35
	premium_higher_strike_long_call = 0.85
	higher_call='short_put'

	lower_strikeprice_long_call=30
	premium_lower_strike_long_call = 3.15
	lower_call='long_call'

	# Short Call
	strikeprice_short_call = 32.5
	premium_short_call = 1.80
	short_call='short_call'

	# Range of stock prices at expiration
	sT = np.arange(10,60,1)


	#####
	# Long call payoff (lower strike)
	#####
	# OTM Strike Long Call Payoff
	lower_strike_long_call_payoff = option_payoff(sT,lower_strikeprice_long_call,premium_lower_strike_long_call,lower_call)
	title='Long 30 strike call'
	# ~ plot_option(sT,lower_strike_long_call_payoff,title)



	#####
	# Long call payoff (Higher Strike)
	#####
	higher_strike_long_call_payoff = option_payoff(sT,higher_strikeprice_long_call,premium_higher_strike_long_call,higher_call)
	title='Long 35 strike call'
	plot_option(sT,higher_strike_long_call_payoff,title)


	#####
	# Short Call Payoff
	#####
	Short_call_payoff = option_payoff(sT,strikeprice_short_call,premium_short_call,short_call)
	title='Short 32.5 Call'
	# ~ plot_option(sT,Short_call_payoff,title)


	#####
	# Butterfly spread payoff
	#####
	Butterfly_spread_payoff = lower_strike_long_call_payoff + higher_strike_long_call_payoff + 2 *Short_call_payoff
	title='Butterfly spread payoff'
	# ~ plot_option(sT,Butterfly_spread_payoff,title)
	
	
	#####
	# Print profit/loss
	#####
	profit = max(Butterfly_spread_payoff)
	loss = min(Butterfly_spread_payoff)

	# ~ print ("Max Profit: %.2f" %profit)
	# ~ print ("Max Loss: %.2f" %loss)


	# ~ #####
	# ~ # Print all options and payoff on one plot
	# ~ #####
	# ~ fig, ax = plt.subplots()
	# ~ ax.spines['bottom'].set_position('zero')
	# ~ ax.plot(sT,Butterfly_spread_payoff ,color='b', label= 'Butterfly Spread')
	# ~ ax.plot(sT, lower_strike_long_call_payoff,'--', color='m',label='Lower Strike Long Call')
	# ~ ax.plot(sT, higher_strike_long_call_payoff,'--', color='g', label='Higher Strike Long Call')
	# ~ ax.plot(sT, Short_call_payoff, '--', color='r', label='Short call')
	# ~ plt.legend()
	# ~ plt.xlabel('Stock Price')
	# ~ plt.ylabel('Profit & Loss')
	# ~ plt.show()







main()

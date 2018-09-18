'''
Short Put Butterfly Plots

Given: Option price data
# Spot Price: s0

# Short puts
higher_strikeprice_short_put = 35
premium_higher_strike_short_put = 0.85
higher_put='short_put'

lower_strikeprice_short_put = 30
premium_lower_strike_short_put = 3.15
lower_put='short_put'

# long put
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


def main():
	############
	#
	# Option price data input
	# Nov 16 2018
	# 
	############
	
	# transaction costs
	fee=5.0/400.
	
	# time value of money (holding period in years)
	risk_free_rate=0.03
	holding_period=0.5

	# Spot Price
	s0 = 83.50

	# Short puts 81,85
	higher_strikeprice_short_put = 85.0
	#3.6
	premium_higher_strike_short_put = 2.40
	higher_put='short_put'

	lower_strikeprice_short_put = 80.0
	#1.8
	premium_lower_strike_short_put = 1.17
	lower_put='short_put'

	# long put
	strikeprice_long_put = 82.50
	premium_long_put = 1.65
	long_put='long_put'

	# Range of stock prices at expiration
	sT = np.arange(70,100,1)
	
	
	#####
	# short put payoff (lower strike)
	#####
	# OTM Strike Long Call Payoff
	lower_strike_short_put_payoff = option_payoff(sT,lower_strikeprice_short_put,premium_lower_strike_short_put,lower_put)
	
	#####
	# short put payoff (Higher Strike)
	#####
	higher_strike_short_put_payoff = option_payoff(sT,higher_strikeprice_short_put,premium_higher_strike_short_put,higher_put)
	
	#####
	# long put payoff
	#####
	long_put_payoff = option_payoff(sT,strikeprice_long_put,premium_long_put,long_put)
	
	#####
	# Butterfly spread payoff
	#####
	Butterfly_spread_payoff = lower_strike_short_put_payoff + higher_strike_short_put_payoff + 2 *long_put_payoff
	
	#####
	# Optimal profit/loss
	#####
	profit = max(Butterfly_spread_payoff)
	loss = min(Butterfly_spread_payoff)
	print ("Max Profit: %.2f" %profit)
	print ("Max Loss: %.2f" %loss)
	
	####
	# holding costs
	####
	# out of pocket
	oop=premium_higher_strike_short_put+premium_lower_strike_short_put-2.0*premium_long_put
	# out of pocket invested at risk free rate
	final=oop*(1.0+risk_free_rate)**holding_period
	cost=final-oop+fee
	
	
	#####
	# adjusted profit/loss
	#####
	profit = max(Butterfly_spread_payoff)-cost
	loss = min(Butterfly_spread_payoff)-cost
	print ("Max Adjusted Profit: %.2f" %profit)
	print ("Max Adjusted Loss: %.2f" %loss)

	
main()

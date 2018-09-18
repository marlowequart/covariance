'''
Autocorrelation
The variance ratio looks at how the volatility changes over time. If the recent
volatility is higher than longer term, this is likely indicative of a mean reverting period
However if the longer term volatility is higher than recent, this could indicate a trend.
In this way, the variance ratio can be used to determine trends.
Another way to say this is a tool to separate the signal(trend) from the noise.

Given:
1 data set
Data set must be sorted by date from oldest at the top to newest date

Return:
variance_ratio_plot: a graph of the autocorrelation for a given date

want to see how this changes over time and how we might be able to detect a crossover
from sideways to trend.
Positive slope indicates a trend. The trend could either be downards or upwards.

'''

#for data manipulation
import numpy as np
import datetime
import seaborn
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")


def call_payoff (sT, strike_price, premium):
	return np.where(sT>strike_price, sT-strike_price, 0)-premium



######
# Call Payoff
######

# Spot Price
s0 = 40

# Long Call
higher_strike_price_long_call = 35
lower_strike_price_long_call=30

premium_higher_strike_long_call = 0.85
premium_lower_strike_long_call = 3.15

# Short Call
strike_price_short_call = 32.5
premium_short_call = 1.80

# Range of call option at expiration
sT = np.arange(10,60,1)


#####
# Long call payoff
#####

# OTM Strike Long Call Payoff
lower_strike_long_call_payoff = call_payoff(sT, lower_strike_price_long_call, premium_lower_strike_long_call)

fig, ax = plt.subplots()
ax.spines['bottom'].set_position('zero')
ax.plot(sT,lower_strike_long_call_payoff, color='g')
ax.set_title('LONG 30 Strike Call')
plt.xlabel('Stock Price')
plt.ylabel('Profit & Loss')

plt.show()


#####
# Higher Strike Long Call Payoff
#####
higher_strike_long_call_payoff = call_payoff(sT, higher_strike_price_long_call, premium_higher_strike_long_call)

fig, ax = plt.subplots()
ax.spines['bottom'].set_position('zero')
ax.plot(sT,higher_strike_long_call_payoff, color='g')
ax.set_title('LONG 35 Strike Call')
plt.xlabel('Stock Price (sT)')
plt.ylabel('Profit & Loss')

plt.show()

#####
# Short Call Payoff
#####
Short_call_payoff = call_payoff(sT, strike_price_short_call, premium_short_call)*-1.0

fig, ax = plt.subplots()
ax.spines['bottom'].set_position('zero')
ax.plot(sT, Short_call_payoff, color='r')
ax.set_title('Short 32.5 Strike Call')
plt.xlabel('Stock Price')
plt.ylabel('Profit & Loss')

plt.show()

#####
# Butterfly spread payoff
#####
Butterfly_spread_payoff = lower_strike_long_call_payoff + higher_strike_long_call_payoff + 2 *Short_call_payoff

fig, ax = plt.subplots()
ax.spines['bottom'].set_position('zero')
ax.plot(sT,Butterfly_spread_payoff ,color='b', label= 'Butterfly Spread')
ax.plot(sT, lower_strike_long_call_payoff,'--', color='g',label='Lower Strike Long Call')
ax.plot(sT, higher_strike_long_call_payoff,'--', color='g', label='Higher Strike Long Call')
ax.plot(sT, Short_call_payoff, '--', color='r', label='Short call')
plt.legend()
plt.xlabel('Stock Price')
plt.ylabel('Profit & Loss')
plt.show()



Butterfly_spread_payoff = lower_strike_long_call_payoff + higher_strike_long_call_payoff + 2 *Short_call_payoff

fig, ax = plt.subplots()
ax.spines['bottom'].set_position('zero')
ax.plot(sT,Butterfly_spread_payoff ,color='b', label= 'Butterfly Spread')
plt.legend()
plt.xlabel('Stock Price')
plt.ylabel('Profit & Loss')
plt.show()


#####
# Print profit/loss
#####
profit = max(Butterfly_spread_payoff)
loss = min(Butterfly_spread_payoff)

print ("%.2f" %profit)
print ("%.2f" %loss)


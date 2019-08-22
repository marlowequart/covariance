'''
Long Call Butterfly Plots

Given: Option price data
C=Call option price
P=put option price
S=Current underlying price
K=strike price
r=risk-free interest rate
t=time to maturity(in days)
v=volatility


Example today is 8/21/19
Apple put strike: 210
expiration: 10/18/19 (58 days)
Underlying price: 212.64
premium: 7.17
2mo tresury: 1.98%
26% vol gives price of 7.24
25% vol gives price of 6.9




Return:
Solve the black scholes equation for different variables
-Solve for volatility
-Solve for pricing

'''

import numpy as np
import datetime
import matplotlib.pyplot as plt
import math as m
from scipy.stats import norm


def put_opt_price(S,K,r,t,v):
	d1=(m.log(S/K)+t*(r+(v**2/2)))/(v*m.sqrt(t))
	d2=d1-(v*m.sqrt(t))
	# print('time: '+str(t)+', ln(s/k): '+str(m.log(S/K))+', t(r-q+sig/2): '+str(t*(r+((v**2)/2)))+', sig*sqrt(t): '+str(v*m.sqrt(t)))
	# print(d1,d2)
	
	# calculate standard normal cumulative distribution function (mean=0, std=1)
	nd1=norm.cdf(-d1)
	nd2=norm.cdf(-d2)
	# print(nd1,nd2)
	
	p=K*m.exp(-r*t)*nd2-S*nd1
	# print('put price: '+str(p))
	return p
	
	
def call_opt_price(S,K,r,t,v):
	d1=(m.log(S/K)+t*(r+(v**2/2)))/(v*m.sqrt(t))
	d2=d1-(v*m.sqrt(t))
	# print('time: '+str(t)+', ln(s/k): '+str(m.log(S/K))+', t(r-q+sig/2): '+str(t*(r+((v**2)/2)))+', sig*sqrt(t): '+str(v*m.sqrt(t)))
	# print(d1,d2)
	
	# calculate standard normal cumulative distribution function (mean=0, std=1)
	nd1=norm.cdf(d1)
	nd2=norm.cdf(d2)
	# print(nd1,nd2)
	
	c=S*nd1-K*m.exp(-r*t)*nd2
	# print('call price: '+str(c))
	return c
	
def call_greeks(S,K,r,t,v):
	d1=(m.log(S/K)+t*(r+(v**2/2)))/(v*m.sqrt(t))
	d2=d1-(v*m.sqrt(t))
	nd1=norm.cdf(d1)
	nd2=norm.cdf(d2)
	
	delta=m.exp(-r*t)*nd1
	gamma=(m.exp(-r*t)/(S*v*m.sqrt(t)))*(m.exp(((-d1)**2)/2)/m.sqrt(2*m.pi))
	
	print('call delta: '+str(round(delta,4)))

def put_greeks(S,K,r,t,v):
	d1=(m.log(S/K)+t*(r+(v**2/2)))/(v*m.sqrt(t))
	d2=d1-(v*m.sqrt(t))
	nd1=norm.cdf(d1)
	nd2=norm.cdf(d2)
	
	delta=m.exp(-r*t)*(nd1-1)
	gamma=(m.exp(-r*t)/(S*v*m.sqrt(t)))*(m.exp(((-d1)**2)/2)/m.sqrt(2*m.pi))
	
	print('put delta: '+str(round(delta,4)))
	

def main():
	############
	#
	# 
	# 
	############
	
	# put/call option price
	P=2.42
	# current underlying price
	S=36.7
	# strike price
	K=35
	# risk free rate
	r=0.01
	# time to maturity (days)
	t1=26
	# time to maturity (% of year)
	t=t1/252
	
	
	
	# price=put_opt_price(S,K,r,t,v)
	# error=P-price
	# print('vol: '+str(round(100*v,2))+', price: '+str(round(price,2))+', error: '+str(round(error,2)))
	
	# Run this loop to optimize to find the volatility based on knowing the price
	# can run for both put and call
	#volatility
	v=1.0
	error=100
	while abs(error) > 0.01:
		# price=put_opt_price(S,K,r,t,v)
		price=call_opt_price(S,K,r,t,v)
		error=P-price
		if error > 0:
			v=v+v*.1
		else:
			v=v-v*.1
		# print('vol: '+str(round(100*v,2))+', price: '+str(round(price,2))+', error: '+str(round(error,2)))
	
	print()
	print('Final price: '+str(round(price,2))+', volatility: '+str(round(100*v,2)))
	
	# v=.48
	# put_greeks(S,K,r,t,v)
	call_greeks(S,K,r,t,v)
	
	
main()
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 15:00:36 2015

@author: assa
"""

import numpy as np
import scipy.stats as ss
import time
from math import math

#Black and Scholes


def d1(S0, K, r, sigma, T):
    return (np.log(S0/K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))


def d2(S0, K, r, sigma, T):
    return (np.log(S0/K) + (r - sigma**2 / 2) * T) / (sigma * np.sqrt(T))


def BlackScholes(Otype, S0, K, r, sigma, T):
    if Otype == "C":        
        return S0 * ss.norm.cdf(d1(S0,K,r,sigma,T)) - K * np.exp(-r*T) * ss.norm.cdf(d2(S0,K,r,sigma,T))
    elif Otype == "P":
        return K * np.exp(-r * T) * ss.norm.cdf(-d2(S0, K, r, sigma, T)) - S0 * ss.norm.cdf(-d1(S0, K, r, sigma, T))
    else:
        raise ValueError("only availalbe 'C' & 'P'")
        return ''


def CalcImpliedVolatility(Otype, S0, K, r, T, price, eps, Vol):    
    for i in xrange(5):
        pricev = BlackScholes(Otype, S0, K, r, Vol, T)
        if abs(price-pricev) < eps:
            break

        td1 = d1(S0, K, r, Vol, T)
        NPrime = ((2*np.pi)**(-0.5))*np.exp(-0.5*(td1)**2)
        vega = S0*np.exp(-r*T)*NPrime*np.sqrt(T)
        if vega == 0.0:
            return np.nan
            # raise ValueError("vega is zero, Otype: %s, K: %.2f, price: %.4f, Vol: %f"%(Otype,K,price,Vol))
        Vol += (price-pricev) / vega
    
    return Vol


def CalcBiSectionImpliedInterestRate(S0, K, r_low,r_high, T, callprice,putprice, eps, Vol):
    count = 0
    while True:
        r_mid = (r_low + r_high) * 0.5
        CallImVol = CalcImpliedVolatility('C', S0, K, r_mid, T, callprice, 0.000001, Vol)
        PutImVol = CalcImpliedVolatility('P', S0, K, r_mid, T, putprice, 0.000001, Vol)
        dVol = CallImVol - PutImVol
        if abs(dVol) < eps:
            break

        if dVol < 0:
            r_high = r_mid
        else:
            r_low = r_mid
            
        count += 1
        if count > 1000: break
            
    print CallImVol, PutImVol
    return r_mid

    
def CalcExplicitImpliedInterestRate(callprice, putprice, futureprice, strike, T_option, T_future):
    c = callprice
    p = putprice
    F = futureprice
    K = strike
    T1 = T_option
    T2 = T_future
    r = (F*T1 - K*T2 - T1*c + T1*p - T2*c + T2*p + sqrt(F**2*T1**2 - 2*F*K*T1*T2 - 2*F*T1**2*c + 2*F*T1**2*p + 2*F*T1*T2*c - 2*F*T1*T2*p + K**2*T2**2 - 2*K*T1*T2*c + 2*K*T1*T2*p + 2*K*T2**2*c - 2*K*T2**2*p + T1**2*c**2 - 2*T1**2*c*p + T1**2*p**2 - 2*T1*T2*c**2 + 4*T1*T2*c*p - 2*T1*T2*p**2 + T2**2*c**2 - 2*T2**2*c*p + T2**2*p**2))/(2*T1*T2*(c - p))
    return r
    pass
    
        
class optionGreek:
    def __init__(self):
        self.S0 = 0
        self.K = 0
        self.r = 0
        self.sigma = 0
        self.T = 0
        self.price=0
        self.delta=0
        self.gamma=0
        self.theta=0
        self.vega=0
        self.OptionType = ''
    
        
    def BlackScholesGreek(self):                
        if self.OptionType == '':
            raise ValueError("only availalbe 'C' & 'P'")
            return
        
        td1=d1(self.S0, self.K, self.r, self.sigma, self.T)
        td2=d2(self.S0, self.K, self.r, self.sigma, self.T)
        NPrime=((2*np.pi)**(-1/2))*np.exp(-0.5*(td1)**2)
        
        if self.OptionType == 'C':
            self.price=S0 * ss.norm.cdf(td1) - K * np.exp(-r * T) * ss.norm.cdf(td2)
            self.delta=ss.norm.cdf(td1)
            self.theta=(NPrime)*(-S0*sigma*0.5/np.sqrt(T))-r*K * np.exp(-r * T) * ss.norm.cdf(td2)
        elif self.OptionType == 'P':
            self.price=K * np.exp(-r * T) * ss.norm.cdf(-td2) - S0 * ss.norm.cdf(-td1)
            self.delta=ss.norm.cdf(td1)-1
            self.theta=(NPrime)*(-S0*sigma*0.5/np.sqrt(T))+r*K * np.exp(-r * T) * ss.norm.cdf(-td2)
            
        
        self.gamma=(NPrime/(S0*sigma*T**(0.5)))
        self.vega = S0*np.exp(-r*T)*NPrime*np.sqrt(T)
            

        
if __name__ == '__main__':
    r = 7.13775634766e-06
    T = 6.25 * 10 + 11 * 9 - 0.5
    # S0 = 252.48 * np.exp(-r*T)
    S0 = 252.19
    K = 252.5
    sigma = 0.001791864
    Otype = 'P'

    print '-' * 20
    t = time.time()
    r_high = 0.000009
    r_low = 0.000005
    r = CalcImpliedInterestRate(S0, K, r_low, r_high, T, 1.995, 2.015,0.000000001,0.0017)
    elapsed = time.time()-t
    print "Option\tBlack-Scholes ImR:", r
    print "Elapsed:", elapsed
    
    option = optionGreek()
    option.S0 = S0
    option.K = K
    option.r = r
    option.sigma = sigma
    option.T = T
    option.OptionType = Otype
    
    print '-' * 20
    print "S0\tstock price at time 0:", S0
    print "K\tstrike price:", K
    print "r\tcontinuously compounded risk-free rate:", r
    print "sigma\tvolatility of the stock price per hour:", sigma
    print "T\ttime to maturity in trading hours:", T
    
    print '-' * 20
    t=time.time()
    #c_BS = BlackScholes(Otype,S0, K, r, sigma, T)
    option.BlackScholesGreek()
    elapsed = time.time()-t
    print "Option\tBlack-Scholes price:", option.price
    print "Option\tBlack-Scholes delta:", option.delta
    print "Option\tBlack-Scholes gamma:", option.gamma
    print "Option\tBlack-Scholes theta:", option.theta
    print "Option\tBlack-Scholes vega:", option.vega
    print "Elapsed:", elapsed

    print '-' * 20

    t = time.time()
    CallImVol = CalcImpliedVolatility('C',S0,K,r,T,1.995,0.0001,0.0017)
    PutImVol = CalcImpliedVolatility('P',S0,K,r,T,2.015,0.0001,0.0017)
    elapsed = time.time()-t
    print "Option\tBlack-Scholes ImVol:", CallImVol, PutImVol
    print "Elapsed:", elapsed


    print '-' * 20
    pdb.set_trace()
    imvol = CalcImpliedVolatility('P', S0, 225.0, r, T, 0.015, 0.0001, 0.0035)
    print imvol



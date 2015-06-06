# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 12:57:25 2015

@author: assa
"""

import sys
import datetime as dt
import numpy as np
import pandas as pd
from PyQt4 import QtCore
from SubscribeReceiverThread import SubscribeThread
from OptionViewer_date import getoptionbusdayttm, getfuturebusdayttm, getoneyearday

sys.path.append('C:/Python/BlackSholesPricer')
import BlackSholesPricer as pricer


class BackTestReceiverThread(SubscribeThread):
    receiveData = QtCore.pyqtSignal(dict)
    updateImVol = QtCore.pyqtSignal(pd.DataFrame)

    def __init__(self, parent=None):
        SubscribeThread.__init__(self, parent, subtype='BackTest')

        self.df_quote = pd.DataFrame(columns=('Time', 'ShortCD', 'Ask1', 'Bid1'))
        self.df_imvol = pd.DataFrame(columns=('Time', 'ShortCD', 'Strike', 'Ask1', 'Bid1', 'ImVol'))
        self.nowtoday = dt.date(2015, 5, 26)
        self.optionBDTTM = getoptionbusdayttm(self.nowtoday)
        self.futureBDTTM = getfuturebusdayttm(self.nowtoday)
        self.oneyearBD = getoneyearday(self.nowtoday)
        self.r = 0.0175 / (252.0 * 6.25 + 251.0 * 11)
        # self.r = 0.0
        self.T_option = 9.0 / 252.0
        self.call_atm_midprc = 0.0
        self.put_atm_midprc = 0.0
        self.atm_strike = 0.0
        self.futures_midprc = 0.0
        self.T_option = 6.25 * self.optionBDTTM + 11 * (self.optionBDTTM - 1)
        self.T_future = 6.25 * self.futureBDTTM + 11 * (self.futureBDTTM - 1)
        self.T_oneyear = 6.25 * self.oneyearBD + 11 * (self.oneyearBD - 1)
        self.frontmonthcode = 'K6'

    def onReceiveData(self, row):
        if type(row) != dict:
            return

        self.updatetaqtime(row['Time'])


        if float(row['Ask1']) and float(row['Bid1']):
            item = [row['Time'], row['ShortCD'], row['Ask1'], row['Bid1']]
            if not row['ShortCD'] in list(self.df_quote['ShortCD']):
                self.df_quote.loc[len(self.df_quote)] = item
            else:
                index = self.df_quote[self.df_quote['ShortCD'] == row['ShortCD']].index[0]
                self.df_quote.ix[index] = item
            self.df_quote = self.df_quote.sort('ShortCD')
            # self.df_mid = self.df_mid[abs(self.df_mid['Ask1'].astype(float) - self.df_mid['Bid1'].astype(float)) < 0.3]
            # print self.df_mid
            if not self.updateatm(): return

            F = self.call_atm_midprc - self.put_atm_midprc + self.atm_strike
            S0 = F * np.exp(-self.r * self.T_option)
            K = float(row['ShortCD'][-3:])
            if K % 5: K += 0.5
            optiontype = ''
            if row['ShortCD'][0] == '2': optiontype = 'C'
            elif row['ShortCD'][0] == '3': optiontype = 'P'
            else:
                return

            midprice = (float(row['Ask1']) + float(row['Bid1'])) * 0.5
            Vol = 0.0017
            bid1 = float(row['Bid1'])
            ask1 = float(row['Ask1'])
            # imvol = pricer.CalcImpliedVolatility(OptionType, S0, K, self.r, self.T_option, midprice, 0.000001, Vol)
            imvol_bid1 = pricer.CalcImpliedVolatility(optiontype, S0, K, self.r, self.T_option, bid1, 0.000001, Vol)
            imvol_ask1 = pricer.CalcImpliedVolatility(optiontype, S0, K, self.r, self.T_option, ask1, 0.000001, Vol)
            incre = -0.0001
            count = 0

            # imvol = '%.6f'% (imvol * np.sqrt(self.T_oneyear))
            imvol_bid1 = '%.6f'% (imvol_bid1 * np.sqrt(self.T_oneyear))
            imvol_ask1 = '%.6f'% (imvol_ask1 * np.sqrt(self.T_oneyear))
            item = [row['Time'], row['ShortCD'], str(K), row['Ask1'], row['Bid1'], imvol_ask1, imvol_bid1]
            print item
        pass

    def updatetaqtime(self, strtime):
        self.T_option = 6.25 * self.optionBDTTM + 11 * (self.optionBDTTM - 1) - self.converttime(strtime)
        self.T_future = 6.25 * self.futureBDTTM + 11 * (self.futureBDTTM - 1) - self.converttime(strtime)

    def updatesnapshotdata(self, row):
        if row['TAQ'] != 'Q': return
        item = [row['Time'], row['ShortCD'], row['Ask1'], row['Bid1']]
        if not row['ShortCD'] in list(self.df_quote['ShortCD']):
            self.df_quote.loc[len(self.df_quote)] = item
        else:
            index = self.df_quote[self.df_quote['ShortCD'] == row['ShortCD']].index[0]
            self.df_quote.ix[index] = item
        pass

    def updateatm(self):
        df_quote = self.df_quote.copy()
        futureshortcd = '101' + self.frontmonthcode
        df_future_quote = df_quote[df_quote['ShortCD'].str[:5] == futureshortcd]
        df_quote = df_quote[df_quote['ShortCD'].str[:5] != futureshortcd]
        df_quote['Strike'] = df_quote['ShortCD'].str[-3:]
        df_quote['Strike'] = df_quote['Strike'].astype(float)

        if not len(df_future_quote): return False

        if len(df_quote) > 0:
            # df_quote['Strike'] = df_quote.apply(convert_df_strike,axis=1) # need time test
            df_quote.ix[df_quote['Strike'] % 5 != 0, 'Strike'] = df_quote.ix[df_quote['Strike'] % 5 != 0,'Strike'] + 0.5

        df_call_mid = df_quote[df_quote['ShortCD'].str[:3] == '201']
        df_put_mid = df_quote[df_quote['ShortCD'].str[:3] == '301']

        if len(df_call_mid) < 5 or len(df_put_mid) < 5: return False

        df_call_mid['Mid'] = (df_call_mid['Bid1'].astype(float) + df_call_mid['Ask1'].astype(float)) * 0.5  # warning pt
        df_put_mid['Mid'] = (df_put_mid['Bid1'].astype(float) + df_put_mid['Ask1'].astype(float)) * 0.5  # warning pt

        df_syth = df_call_mid.merge(df_put_mid, left_on='Strike', right_on='Strike', how='outer')

        df_syth['Differ'] = abs(df_syth['Mid_x'].astype(float) - df_syth['Mid_y'].astype(float))
        df_syth = df_syth.sort('Differ')

        maxdiff = (2.5 ** 2) * 0.25 * np.exp(self.r * self.T_option * -1)

        if df_syth.iloc[0]['Differ'] >= maxdiff: return False

        self.call_atm_midprc = df_syth.iloc[0]['Mid_x']
        self.put_atm_midprc = df_syth.iloc[0]['Mid_y']
        self.atm_strike = float(df_syth.iloc[0]['Strike'])
        self.futures_midprc = (float(df_future_quote.iloc[0]['Bid1']) + float(df_future_quote.iloc[0]['Ask1'])) * 0.5

        if not np.isnan(self.call_atm_midprc) and not np.isnan(self.put_atm_midprc) and not np.isnan(self.futures_midprc):
            # self.r = pricer.CalcExplicitImpliedInterestRate(self.call_atm_midprc,
            #                                                 self.put_atm_midprc,
            #                                                 self.futures_midprc,
            #                                                 self.atm_strike,
            #                                                 self.T_option,
            #                                                 self.T_option)
            # print 'ATM_Strike: ', self.atm_strike, 'call atm: ', self.call_atm_midprc, 'put atm: ', self.put_atm_midprc,
            # print 'Futures: ', self.futures_midprc,
            # print 'Call ATM Bid/Ask:', df_syth.iloc[0]['Ask1_x'], df_syth.iloc[0]['Bid1_x'],
            # print 'Put ATM Bid/Ask:', df_syth.iloc[0]['Ask1_y'], df_syth.iloc[0]['Bid1_y'],
            # print 'Future ATM Bid/Ask:', df_future_quote.iloc[0]['Ask1'], df_future_quote.iloc[0]['Bid1'],
            # print 'Synth Future Bid/Ask:', self.atm_strike + float(df_syth.iloc[0]['Ask1_x']) - float(df_syth.iloc[0]['Bid1_y']), \
            #                         self.atm_strike + float(df_syth.iloc[0]['Bid1_x']) - float(df_syth.iloc[0]['Ask1_y'])

            # print 'Interest Rate(hour): ', self.r, 'Interest Rate (Annual):', self.r * self.oneyearBD * (6.15 + 11)
            return True
        else:
            return False
        pass

    def converttime(self, strtime):
        starttime = dt.datetime(1900, 1, 1, 9, 0, 0)
        nowtime = dt.datetime.strptime(strtime, '%H:%M:%S.%f')
        td = nowtime - starttime
        # 1 hour = 3600 sec
        return td.seconds / 3600.0

    def updatefrontmonthcode(self):
        self.frontmonthcode = 'K6'

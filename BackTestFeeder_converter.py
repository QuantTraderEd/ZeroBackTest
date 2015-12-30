# -*- coding: utf-8 -*-
"""
Created on Sun Dec 06 22:37:47 2015

@author: assa
"""

names = [
    'ShortCD',
    'FeedSource',
    'TAQ',
    'SecuritiesType',
    'Time',
    'BuySell',
    'LastPrice', 'LastQty',
    'Bid1', 'Ask1','BidQty1', 'AskQty1','BidCnt1', 'AskCnt1',
    'Bid2', 'Ask2','BidQty2', 'AskQty2','BidCnt2', 'AskCnt2',
    'Bid3', 'Ask3','BidQty3', 'AskQty3','BidCnt3', 'AskCnt3',
    'Bid4', 'Ask4','BidQty4', 'AskQty4','BidCnt4', 'AskCnt4',
    'Bid5', 'Ask5','BidQty5', 'AskQty5','BidCnt5', 'AskCnt5',
    'TotalBidQty', 'TotalAskQty',
    'TotalBidCnt', 'TotalAskCnt']
    
def makeMsg(taq_dict, nightshift):
    msg_lst = []
    
    timestamp = taq_dict['Time']
    feedsource = taq_dict['FeedSource']
    TAQ = taq_dict['TAQ']
    SecuritiesType = taq_dict['SecuritiesType']
    buysell = taq_dict['buysell']
    lastprice = taq_dict['LastPrice']
    lastqty = taq_dict['LastQty']
    
    shortcd = taq_dict['shortcd']
    
    msg_lst = [timestamp, feedsource, TAQ, SecuritiesType]
    
    if feedsource == 'cybos' and TAQ == 'Q' and SecuritiesType == 'futures':
        msg_lst.append[shortcd]
        msg_lst.append['']
        msg_lst.append[str(taq_dict['Ask1'])]
        msg_lst.append[str(taq_dict['Ask2'])]
        msg_lst.append[str(taq_dict['Ask3'])]
        msg_lst.append[str(taq_dict['Ask4'])]
        msg_lst.append[str(taq_dict['Ask5'])]
        msg_lst.append[str(taq_dict['AskQty1'])]
        msg_lst.append[str(taq_dict['AskQty2'])]
        msg_lst.append[str(taq_dict['AskQty3'])]
        msg_lst.append[str(taq_dict['AskQty4'])]
        msg_lst.append[str(taq_dict['AskQty5'])]
        
        
    

def msgParser(msg,nightshift):
    lst = msg.split(',')

    timestamp = lst[0]
    feedsource = lst[1]
    TAQ = lst[2]
    SecuritiesType = lst[3]
    buysell = ''
    lastprice = ''
    lastqty = ''

    if lst[1] == 'cybos' and lst[2] == 'Q' and lst[3] == 'futures':
        shcode = str(lst[4]) + '000'
        if nightshift == 0:
            ask1 = convert(lst[6])
            ask2 = convert(lst[7])
            ask3 = convert(lst[8])
            ask4 = convert(lst[9])
            ask5 = convert(lst[10])
            bid1 = convert(lst[23])
            bid2 = convert(lst[24])
            bid3 = convert(lst[25])
            bid4 = convert(lst[26])
            bid5 = convert(lst[27])
            askqty1 = str(lst[11])
            askqty2 = str(lst[12])
            askqty3 = str(lst[13])
            askqty4 = str(lst[14])
            askqty5 = str(lst[15])
            totalaskqty = str(lst[16])
            askcnt1 = str(lst[17])
            askcnt2 = str(lst[18])
            askcnt3 = str(lst[19])
            askcnt4 = str(lst[20])
            askcnt5 = str(lst[21])
            totalaskcnt = str(lst[22])
            bidqty1 = str(lst[28])
            bidqty2 = str(lst[29])
            bidqty3 = str(lst[30])
            bidqty4 = str(lst[31])
            bidqty5 = str(lst[32])
            totalbidqty = str(lst[33])
            bidcnt1 = str(lst[34])
            bidcnt2 = str(lst[35])
            bidcnt3 = str(lst[36])
            bidcnt4 = str(lst[37])
            bidcnt5 = str(lst[38])
            totalbidcnt = str(lst[39])
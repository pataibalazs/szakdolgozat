
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import time
import datetime
from binance.client import Client
from binance import BinanceSocketManager
import statistics
import database as database
import requests

class financeData:
    def __init__(self,database,target):
        self.db=database
        self.stocks=['BTC','ETH']
        self.target=target
        self.client=Client('wiEbycXmBgpz7CC5ZwRyY9eZnqmzwg5xEKQHjhwR0uklOCsJFDuA0NOxAd33G8cs','ZuPPyiEUNfK4b8vFa7wzEA3Yb08zAEkXX6AMEFJGCMS767ZHHx2HUecyE7thMSq2')
        self.savedTime='temp'
    
    def stockFormatting(self,datas):
        currentStockDatas=datas[:-1]
        currentStockDatas[0]=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(currentStockDatas[0]/1000))
        currentStockDatas[6]=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(currentStockDatas[6]/1000))
        stringToInt=[1,2,3,4,5,7,9,10]
        for number in stringToInt:
            currentStockDatas[number]=float(currentStockDatas[number])

        return currentStockDatas
    
    
    def dataMiningCycle(self):
        print("DataMiningCycle has started!")
        counter=0
        self.db.deleteAllFromTemp('allStock_temp')
        while True:
            candles = self.client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE)
            currentStockDatas=self.stockFormatting(candles[-1])

            if(self.savedTime=='temp'):
                self.db.deleteAllFromTemp('allStock_temp')
                self.db.insertIntoStockTable('allStock_temp',currentStockDatas)
                self.db.insertIntoStockTable('allStock',currentStockDatas)
                self.savedTime=currentStockDatas[0]
            elif(self.savedTime==currentStockDatas[0]):
                self.db.insertIntoStockTable('allStock_temp',currentStockDatas)
                self.db.deleteLastRow('allStock')
                datas=self.db.avgInStockTable('allStock_temp')
                self.db.insertIntoStockTable('allStock',datas)
            else:
                self.db.deleteAllFromTemp('allStock_temp')
                self.db.insertIntoStockTable('allStock_temp',currentStockDatas)
                self.db.insertIntoStockTable('allStock',currentStockDatas)
                self.savedTime=currentStockDatas[0]
            counter=counter+1
            if(counter==self.target):
                requests.put("https://api.binance.com/api/v3/userDataStream")
                counter=0
            time.sleep(1)

db=database.dataBase()
fd=financeData(db,1500)
fd.dataMiningCycle()






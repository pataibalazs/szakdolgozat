
from numpy.core.fromnumeric import mean
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import time
import datetime
from binance.client import Client
from binance import BinanceSocketManager
import database as database
import requests
import numpy as np
from datetime import datetime,timezone,timedelta

class financeData:
    def __init__(self):
        self.stocks=['BTC','ETH']
        self.client=Client('wiEbycXmBgpz7CC5ZwRyY9eZnqmzwg5xEKQHjhwR0uklOCsJFDuA0NOxAd33G8cs','ZuPPyiEUNfK4b8vFa7wzEA3Yb08zAEkXX6AMEFJGCMS767ZHHx2HUecyE7thMSq2')
        self.savedTime='temp'
        self.file = open("/home/balazs/Desktop/kaka.txt", "a")
    
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
        final=[]
        lista0=[]
        lista1=[]
        lista2=[]
        lista3=[]
        lista4=[]
        lista5=[]
        utc=[]
        cest=[]
        while True:
            candles = self.client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE)
            currentStockDatas=self.stockFormatting(candles[-1])
            print(currentStockDatas)
            if(len(lista0)!=0):
                if(currentStockDatas[0]!=lista0[-1]):
                        now_utc = datetime.now(timezone.utc)-timedelta(minutes=1)
                        #elem=(lista0[0],np.mean(lista1),np.mean(lista2),np.mean(lista3),np.mean(lista4),np.mean(lista5))
                        #self.file.write(f"""{lista0[0]};{round(np.mean(lista1),3)};{round(np.mean(lista2),3)};{round(np.mean(lista3),3)};{round(np.mean(lista4),3)};{round(np.mean(lista5),3)};{now_utc+timedelta(hours=2)};{now_utc}\n""")
                        self.file.write(f"""{lista0[-1]};{round(lista1[-1],3)};{round(lista2[-1],3)};{round(lista3[-1],3)};{round(lista4[-1],3)};{round(lista5[-1],3)};{now_utc+timedelta(hours=2)};{now_utc}\n""")
                        lista0=[currentStockDatas[0]]
                        lista1=[currentStockDatas[1]]
                        lista2=[currentStockDatas[2]]
                        lista3=[currentStockDatas[3]]
                        lista4=[currentStockDatas[4]]
                        lista5=[currentStockDatas[5]]
                        print(final)
                else:
                        lista0.append(currentStockDatas[0])
                        lista1.append(currentStockDatas[1])
                        lista2.append(currentStockDatas[2])
                        lista3.append(currentStockDatas[3])
                        lista4.append(currentStockDatas[4])
                        lista5.append(currentStockDatas[5])
            else:
                    lista0.append(currentStockDatas[0])
                    lista1.append(currentStockDatas[1])
                    lista2.append(currentStockDatas[2])
                    lista3.append(currentStockDatas[3])
                    lista4.append(currentStockDatas[4])
                    lista5.append(currentStockDatas[5])
            counter=counter+1
            if(counter==600):
                requests.put("https://api.binance.com/api/v3/userDataStream")
                counter=0
                
            time.sleep(1)


fd=financeData()
fd.dataMiningCycle()






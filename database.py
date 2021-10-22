import pandas as pd
import random

import dash_html_components as html
from dash.dependencies import Input, Output, State
import time
from datetime import datetime, date, time, timedelta
import threading
import mysql.connector
from icecream import ic
import random
import threading
import statistics
import datetime



class dataBase:
    def __init__(self):

        self.lock=threading.Lock()
        self.connection=mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="angi",
            database="financeProgram",
            auth_plugin='mysql_native_password')
        
    def createStockTable(self,name):
        mycursor = self.connection.cursor() 
        query = f""" 
            CREATE TABLE IF NOT EXISTS `{name}` ( 
            `time` datetime NOT NULL,       
            `open` float,
            `high` float,
            `low` float,   
            `close` float,   
            `volume` float,
            `close_time` datetime NOT NULL,
            `quoteAssetVolume` float,
            `tradeNumber` float,   
            `buyBaseAsset` float,   
            `buyQuoteAsset` float,
            `id` int primary KEY auto_increment
            );"""
        mycursor.execute(query,)

        self.connection.commit()
        mycursor.close()

        mycursor = self.connection.cursor() 
        query = f""" 
            CREATE TABLE IF NOT EXISTS `{name+'_temp'}` ( 
            `time` datetime NOT NULL,       
            `open` float,
            `high` float,
            `low` float,   
            `close` float,   
            `volume` float,
            `close_time` datetime NOT NULL,
            `quoteAssetVolume` float,
            `tradeNumber` float,   
            `buyBaseAsset` float,   
            `buyQuoteAsset` float,
            `id` int primary KEY auto_increment
            );"""
        mycursor.execute(query,)

        self.connection.commit()
        mycursor.close()

    def countRecords(self):
        self.lock.acquire()
        mycursor = self.connection.cursor() 
        query_count=f"""select count(*) from allStock_temp"""
        mycursor.execute(query_count,)
        records = mycursor.fetchall()
        self.connection.commit()


        
        mycursor.close()
        self.lock.release()
        return records[0][0]

    def avgInStockTable(self,name):
        self.lock.acquire()
        
        mycursor = self.connection.cursor() 
        query = f""" 
            select 
            time,
            avg(btc_open),
            avg(btc_high),
            avg(btc_low),
            avg(btc_close),
            avg(btc_volume),
            close_time,
            avg(btc_quoteAssetVolume),
            avg(btc_tradeNumber),
            avg(btc_buyBaseAsset),
            avg(btc_buyQuoteAsset)
            from {name}
            group by time"""
        

        mycursor.execute(query,)
        records = mycursor.fetchall()

        self.connection.commit()
        mycursor.close()
        self.lock.release()
        return records[0]

    def insertIntoStockTable(self,name,datas):
        self.lock.acquire()
        
        mycursor = self.connection.cursor() 

        query=f"""INSERT INTO {name} VALUES {str(datas[0]),datas[1],datas[2],datas[3],datas[4],datas[5],str(datas[6]),datas[7],datas[8],datas[9],datas[10],0};"""
        mycursor.execute(query,)
        

        self.connection.commit()
        mycursor.close()
        self.lock.release()

    def deleteAllFromTemp(self,name):
        mycursor = self.connection.cursor() 

        query=f"""truncate {name}"""
        mycursor.execute(query,)
        
        self.connection.commit()
        mycursor.close()
    
    def deleteLastRow(self,name):
        self.lock.acquire()
        mycursor = self.connection.cursor() 
        query_delete=f"DELETE FROM {name} ORDER BY id DESC LIMIT 1"
        mycursor.execute(query_delete,)
        self.connection.commit()
        mycursor.close()
        self.lock.release()

    def dataForGauge(self,name):
        self.lock.acquire()
        mycursor = self.connection.cursor() 

        query=f"""SELECT btc_close FROM {name} ORDER BY ID DESC LIMIT 2;"""
        mycursor.execute(query,)
        records = mycursor.fetchall()
                
        self.connection.commit()
        mycursor.close()

        values=[records[0][0],records[1][0]]
        self.lock.release()
        return values
    
    
    def dataForGraphs(self,name):
        self.lock.acquire()
        mycursor = self.connection.cursor()
        query=f"""SELECT btc_open,btc_close,btc_high,btc_low,time FROM
                (SELECT ID,btc_open,btc_close,btc_high,btc_low,time
                FROM {name}
                group by time
                ORDER BY ID DESC LIMIT 30) sub
                order by id ASC;"""
        mycursor.execute(query,)
        records = mycursor.fetchall()
        self.connection.commit()
        mycursor.close()
        self.lock.release()
        return records

    def percentChange(self,lastValue,secondLastValue):
        return round((float(lastValue)-secondLastValue)/abs(secondLastValue),6)

    
    def dataForPrediction(self,name):
        self.lock.acquire()
        mycursor = self.connection.cursor() 
        query=f"""select btc_close,btc_high,btc_low from
            (SELECT * FROM {name} ORDER BY id DESC LIMIT 3) sub
            order by id 
            limit 2"""
        mycursor.execute(query,)
        records = mycursor.fetchall()
                
        self.connection.commit()
        mycursor.close()

        self.lock.release()
       
        values=[self.percentChange(records[1][i],records[0][i]) for i in range(len(records)+1)]
        return values

    def dataForInitialPrediction(self,name):
        self.lock.acquire()
        mycursor = self.connection.cursor() 
        query=f"""SELECT btc_close,btc_high,btc_low FROM {name} ORDER BY ID DESC LIMIT 2;"""
        mycursor.execute(query,)
        records = mycursor.fetchall()     
        self.connection.commit()
        mycursor.close()
        self.lock.release()
        values=[self.percentChange(records[0][i],records[1][i]) for i in range(len(records)+1)]
        return values



db=dataBase()
#print(db.dataForPrediction('allStock'))


#db.createStockTable('btcusdt')
#
# 
# (db.dataForGraph('btcusdt'))

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_daq as daq
import plotly.graph_objects as go
from PIL import Image
import numpy as np
import base64
import datetime
import plotly
# import warnings
# warnings.filterwarnings("error")


class homepage:
    def __init__(self,database,models):
        self.database=database
        self.trainedModels=models
        self.stocks=['BTC','S&P 500']
        # self.listOfImages={
        #     'strongbuy':'/home/balazs/Desktop/meter/strongbuy.png',
        #     'buy':'/home/balazs/Desktop/meter/buy.png',
        #     'neutral':'/home/balazs/Desktop/meter/neutral.png',
        #     'sell':'/home/balazs/Desktop/meter/sell.png',
        #     'strongsell':'/home/balazs/Desktop/meter/strongsell.png'
        # }
        self.listOfImages={
                -1:"/home/balazs/Desktop/meter/3 célváltozós meter/meter_sell_3.png",
                0:"/home/balazs/Desktop/meter/3 célváltozós meter/meter_neutral_3.png",
                1:"/home/balazs/Desktop/meter/3 célváltozós meter/meter_buy_3.png"
        }




    def figInitialStyle(self):
        fig = plotly.subplots.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
        fig['layout']['margin'] = {
                'l': 30, 'r': 10, 'b': 30, 't': 10
            }
        fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
        data=self.database.dataForGraph('allStock')
        values=[]
        times=[]
        for elem in data:
            values.append(elem[0])
            times.append(elem[1])

        fig.add_trace(go.Scatter(x=times, y=values,
        mode='lines+markers',
        name='lines+markers'))
        fig.update_layout(go.Layout(height=300,width=750,margin={'t': 0,'l':0,'b':0,'r':0}))

        #fig.update_layout(autosize=False,width=700,height=600)
                
        
        return fig
    def whichIsBigger(self,num1,num2):
        percentageChange=((num1/num2)-1)*100
        if(percentageChange<0):
            return html.Div(str(round(percentageChange,4))+'%',style={"text-align":"center","font-size":"30px",'margin-top':'55px',"color":"rgb(255,0,0)"}),
        elif(percentageChange>0):
            return html.Div(str(round(percentageChange,4))+'%',style={"text-align":"center","font-size":"30px",'margin-top':'55px',"color":"rgb(11,102,35)"}),
        else:
            return html.Div(str(round(percentageChange,4))+'%',style={"text-align":"center","font-size":"30px",'margin-top':'55px',"color":"rgb(142,142,142)"}),

            

    def predictionUpdateCallback(self,app):
        app.callback(Output('btcusdt_predDiv','children'),
                Input('predictionRefreshTime', 'n_intervals')
        )(self.predictionUpdate)

    def predictionUpdate(self,n):

        prediction=self.trainedModels.decisionTreePrediction(*self.database.dataForPrediction('allStock'))

        return self.imageLoader(self.listOfImages[prediction[0]])


    def timeUpdate(self,n):
        ido=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return [ido]

    def timeUpdateCallback(self,app):
        app.callback(Output('timeInBlue','children'),
                Input('secondRefreshTime', 'n_intervals')
        )(self.timeUpdate)

    def gaugeRefresh(self,n):
        values=self.database.dataForGauge('allStock')
        div=self.whichIsBigger(values[0],values[1])
        return values[0],div

    def gaugeRefreshCallback(self,app):
        app.callback([Output('btcusdt_div','children'),Output('btcusdt_before_div','children')],
                Input('pageValueRefreshTime', 'n_intervals')
        )(self.gaugeRefresh)

    def updateGraphCallback(self,app):
        app.callback(Output('btcusdt_graph','figure'),
                Input('pageValueRefreshTime', 'n_intervals')
        )(self.updateGraph)

    def updateGraph(self,n):
        fig = plotly.subplots.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
        fig['layout']['margin'] = {
                'l': 30, 'r': 10, 'b': 30, 't': 10
            }
        fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
        data=self.database.dataForGraph('allStock')
        values=[]
        times=[]
        for elem in data:
            values.append(elem[0])
            times.append(elem[1])

        fig.add_trace(go.Scatter(x=times, y=values,
        mode='lines+markers',
        name='lines+markers'))
        fig.update_layout(go.Layout(height=300,width=750,margin={'t': 0,'l':0,'b':0,'r':0}))
        return fig
    



    def layoutMaker(self):
        return html.Div([
            dbc.Row(
                [
                    dcc.Interval(id='secondRefreshTime',interval=1*1000, n_intervals=0),
                    dcc.Interval(id='pageValueRefreshTime',interval=1*1000, n_intervals=0),
                    dcc.Interval(id='predictionRefreshTime',interval=2*1000, n_intervals=0),
                    dbc.Col(dbc.NavbarBrand(id="timeInBlue",children=[""],style={"font-size":"30px",'color':'white',"margin-left":"10px",'margin-top':'15px','font-weight': 'bold'}),width={'size':2}),
                    dbc.Col(width={'size':6}),
                    dbc.Col(dcc.Dropdown(id='a_dropdown', placeholder='examine',
                                        options=[{'label': 'BTC', 'value': 'optA'},
                                                {'label': 'S&P500', 'value': 'optB'}],style={"margin-top":"25px"}),width={'size': 3}),
                    dbc.Col(dbc.Button('Themes',id='themes'),width={'size':1},style={'margin-top':'24px'})
                ],style={'background-color': 'rgb(30, 144, 255)','height':'80px'}
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div("Stock Name",style={"text-align":"center","font-size":"30px"}),width={'size':2}),
                    dbc.Col(html.Div("Stock Price",style={"text-align":"center","font-size":"30px"}),width={'size':2}),
                    dbc.Col(html.Div("Stock Graph",style={"text-align":"center","font-size":"30px"}),width={'size':5}),
                    dbc.Col(html.Div("Forecast",style={"text-align":"center","font-size":"30px"}),width={'size':3}),
                ]
            ),
            self.stockRowMaker('btcusdt',2000,300),
            self.stockRowMaker('S&P 500',1000,14)
        ])
    

    # def stockPriceIndicator(self,stockCurrentPrice,priceBefore,id):
    #     fig = go.Figure(go.Indicator(
    #     mode = "number+delta",
    #     value = stockCurrentPrice,
    #     number = {'prefix': "$"},
    #     delta = {'position': "top", 'reference': priceBefore},
    #     domain = {'x': [0, 1], 'y': [0, 1]}))

    #     fig.update_layout(
    #     autosize=False,
    #     width=300,
    #     height=270)
    #     return dcc.Graph(id,figure=fig,style={})

    def imageLoader(self,src):
        
        test_base64 = base64.b64encode(open(src, 'rb').read()).decode('ascii')
        return html.Img(src='data:image/png;base64,{}'.format(test_base64),height="250px")
    
    def stockRowMaker(self,stockName,stockCurrentPrice,priceBefore):        
        return dbc.Row(
            [
                dbc.Col(html.Div(stockName),style={"text-align":"center","font-size":"50px",'margin-top':"100px"},width={'size':2}),
                #dbc.Col(self.stockPriceIndicator(stockCurrentPrice,priceBefore,stockName+'_price'),width={'size':2}),
                dbc.Col(
                    children=[
                        html.Div(
                            id=stockName+'_before_div',children=[]),
                        html.Div(
                            id=stockName+'_div',
                            style={"text-align":"center","font-size":"50px"}
                            )
                        
                ]),
                #dbc.Col(dcc.Graph(id=stockName+'_graph', figure={self.figInitialStyle()},style={},config={'modeBarButtonsToRemove':['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d']}),width=5),
                dbc.Col(dcc.Graph(id=stockName+'_graph', figure=self.figInitialStyle()),width=5),
                dbc.Col(html.Div(id=stockName+'_predDiv',children=[]),width=3)
            ])          

from pickle import TRUE
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash_daq as daq
import plotly.graph_objects as go
from PIL import Image
import numpy as np
import base64
import datetime
import plotly
import modal as m
from dash.exceptions import PreventUpdate
# import warnings
# warnings.filterwarnings("error")


class homepage:
    def __init__(self,database,models,modal,inputListOfImages):
        self.modal=modal.createModal()
        self.database=database
        self.trainedModels=models
        self.stocks=['BTC']
        self.listOfImages=inputListOfImages
        self.currentstrat="allStrategy"


    def figInitialStyle(self):
        fig = plotly.subplots.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
        fig['layout']['margin'] = {
                'l': 30, 'r': 10, 'b': 30, 't': 10
            }
        fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
        data=self.database.dataForGraphs('allStock')
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


    def whichIsBigger(self,num1,num2):
        percentageChange=((num1/num2)-1)*100
        if(percentageChange<0):
            return html.Div(str(round(percentageChange,4))+'%',style={"text-align":"center","font-size":"30px",'margin-top':'55px',"color":"rgb(255,0,0)"}),
        elif(percentageChange>0):
            return html.Div(str(round(percentageChange,4))+'%',style={"text-align":"center","font-size":"30px",'margin-top':'55px',"color":"rgb(11,102,35)"}),
        else:
            return html.Div(str(round(percentageChange,4))+'%',style={"text-align":"center","font-size":"30px",'margin-top':'55px',"color":"rgb(142,142,142)"}),
 

    def predictionUpdateCallback(self,app):
        app.callback([
            Output('btcusdt_predDiv','children'),
            Output('decisionTree_predDiv','children'),
            Output('xgbBoost_predDiv','children'),
            Output('kneigh','children'),
            Output('linear','children'),
            Output('knnreg','children'),
            Output('bayreg','children')],
            [Input('pageValueRefreshTime', 'n_intervals'),Input('strategy_dropdown','value')],
            State("modal", "is_open")
        )(self.predictionUpdate)

 
    def predictionUpdate(self,n,strategy,state):
        gSize=220

        if(self.currentstrat!=strategy and self.database.countRecords() != 1):

            datas=self.database.dataForPrediction('allStock')
            if(strategy=='aggressive'):
                self.currentstrat='aggressive'
                return self.imageLoader(self.listOfImages[self.trainedModels.aggressive(*datas)],270),dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update
            if(strategy=='justClass'):
                self.currentstrat='justClass'
                return self.imageLoader(self.listOfImages[self.trainedModels.justClassificationHP(*datas)],270),dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update
            if(strategy=='justReg'):
                self.currentstrat='justReg' 
                return self.imageLoader(self.listOfImages[self.trainedModels.justRegressionHP(*datas)],270),dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update
            if(strategy=='allStrategy' or strategy==None):
                self.currentstrat='allStrategy'
                return self.imageLoader(self.listOfImages[self.trainedModels.allStrategyHP(*datas)],270),dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update
            if(strategy==None):
                self.currentstrat=None
                return self.imageLoader(self.listOfImages[self.trainedModels.allStrategyHP(*datas)],270),dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update
            if(strategy=='xgbBoost'):
                self.currentstrat='xgbBoost'
                return self.imageLoader(self.listOfImages[self.trainedModels.xgbBoostPrediction(*datas)[0]],270),dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update
            if(strategy=='decisionTree'):
                self.currentstrat='decisionTree'
                return self.imageLoader(self.listOfImages[self.trainedModels.decisionTreePrediction(*datas)[0]],270),dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update
            if(strategy=='kNeighbour'):
                self.currentstrat='kNeighbour'
                return self.imageLoader(self.listOfImages[self.trainedModels.kneighbourPrediction(*datas)[0]],270),dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update
            if(strategy=='lin-reg'):
                self.currentstrat='lin-reg'
                return self.imageLoader(self.listOfImages[self.trainedModels.linearRegressionPrediction(*datas)[0]],270),dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update
            if(strategy=='kNeighbour-reg'):
                self.currentstrat='kNeighbour-reg'
                return self.imageLoader(self.listOfImages[self.trainedModels.knnRegressionPrediction(*datas)[0]],270),dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update
            if(strategy=='bay-reg'):
                self.currentstrat='bay-reg'
                return self.imageLoader(self.listOfImages[self.trainedModels.bayesianRegressionPrediction(*datas)[0]],270),dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update        
            print("itt valami hiba van")
        if(self.currentstrat!=strategy and self.database.countRecords() == 1):
            self.currenstrat=strategy
            datas=self.database.dataForPrediction('allStock')
            prediction=self.trainedModels.homepagePrediction(*datas)
            fa=self.trainedModels.decisionTreePrediction(*datas)
            xgb=self.trainedModels.xgbBoostPrediction(*datas)
            kneigh=self.trainedModels.kneighbourPrediction(*datas)
            linear=self.trainedModels.linearRegressionPrediction(*datas)
            knnreg=self.trainedModels.knnRegressionPrediction(*datas)
            bayreg=self.trainedModels.bayesianRegressionPrediction(*datas)
            main_pred=""
            if(strategy=='allStrategy' or strategy==None):
                main_pred=prediction
            elif(strategy=='justClass'):
                main_pred=self.trainedModels.justClassificationHP(*datas)
            elif(strategy=='justReg'):
                main_pred=self.trainedModels.justRegressionHP(*datas)
            elif(strategy=='aggressive'):
                main_pred=self.trainedModels.aggressive(*datas)
            elif(strategy=='xgbBoost'):
                main_pred=xgb[0]
            elif(strategy=='decisionTree'):
                main_pred=fa[0]
            elif(strategy=='kNeighbour'):
                main_pred=kneigh[0]
            elif(strategy=='lin-reg'):
                main_pred=linear[0]
            elif(strategy=='kNeighbour-reg'):
                main_pred=knnreg[0]
            elif(strategy=='bay-reg'):
                main_pred=bayreg[0]

            return [
                self.imageLoader(self.listOfImages[main_pred],270),
                self.imageLoader(self.listOfImages[fa[0]],gSize),
                self.imageLoader(self.listOfImages[xgb[0]],gSize),
                self.imageLoader(self.listOfImages[kneigh[0]],gSize),
                self.imageLoader(self.listOfImages[linear[0]],gSize),
                self.imageLoader(self.listOfImages[knnreg[0]],gSize),
                self.imageLoader(self.listOfImages[bayreg[0]],gSize),
            ]


        returnValue='refresh' if self.database.countRecords() == 1 else 'dont-refresh'
        if(returnValue=='dont-refresh'):

            return dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update

        datas=self.database.dataForPrediction('allStock')
        prediction=self.trainedModels.homepagePrediction(*datas)
        fa=self.trainedModels.decisionTreePrediction(*datas)
        xgb=self.trainedModels.xgbBoostPrediction(*datas)
        kneigh=self.trainedModels.kneighbourPrediction(*datas)
        linear=self.trainedModels.linearRegressionPrediction(*datas)
        knnreg=self.trainedModels.knnRegressionPrediction(*datas)
        bayreg=self.trainedModels.bayesianRegressionPrediction(*datas)
        
        return [
            self.imageLoader(self.listOfImages[prediction],270),
            self.imageLoader(self.listOfImages[fa[0]],gSize),
            self.imageLoader(self.listOfImages[xgb[0]],gSize),
            self.imageLoader(self.listOfImages[kneigh[0]],gSize),
            self.imageLoader(self.listOfImages[linear[0]],gSize),
            self.imageLoader(self.listOfImages[knnreg[0]],gSize),
            self.imageLoader(self.listOfImages[bayreg[0]],gSize),
        ]

    def timeUpdate(self,n):
        ido=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return [ido],ido

    def timeUpdateCallback(self,app):
        app.callback(
            [Output('timeInBlue','children'),Output('modalTime','children')],
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

    def updateGraphsCallback(self,app):
        app.callback([Output('btcusdt_graph','figure'),Output('bitcoin_graph_modal','figure')],
                Input('pageValueRefreshTime', 'n_intervals'),
                State("modal", "is_open")
        )(self.updateGraphs)


    def basicFigMaker(self):
        fig = plotly.subplots.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
        fig['layout']['margin'] = {
                'l': 30, 'r': 10, 'b': 30, 't': 10
            }
        fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
        return fig


    def updateGraphs(self,n,state):
        homepage_fig=self.basicFigMaker()
        modal_fig=self.basicFigMaker()

        data=self.database.dataForGraphs('allStock')
        open=[]
        close=[]
        high=[]
        low=[]
        times=[]
        for elem in data:
            open.append(elem[0])
            close.append(elem[1])
            high.append(elem[2])
            low.append(elem[3])
            times.append(elem[4])

        if(state==False):
            homepage_fig.add_trace(go.Scatter(x=times, y=close,
            mode='lines+markers',
            name='lines+markers'))
            homepage_fig.update_layout(go.Layout(height=300,width=750,margin={'t': 0,'l':0,'b':0,'r':0}))
            return homepage_fig,dash.no_update
        elif(state==True):
            modal_fig = go.Figure(data=[go.Candlestick(x=times,
                open=open,
                high=high,
                low=low,
                close=close)])
            
            modal_fig.update_layout(xaxis_rangeslider_visible=False)
            modal_fig.update_layout(go.Layout(height=400,width=1105,margin={'t': 0,'l':0,'b':0,'r':0}))
            return dash.no_update,modal_fig

    def dropdownMaker(self):
        dropdown=dcc.Dropdown(id='inspection_dropdown', placeholder='examine a stock',
                                        options=[{'label': 'BTC', 'value': 'BTC'}],
                                                style={"margin-top":"25px"}
                            )
        return dropdown

    def strategyDropdownMaker(self):
        dropdown=dcc.Dropdown(id='strategy_dropdown', placeholder='pick a strategy',
                                        options=[
                                            {'label': 'All Strategy', 'value': 'allStrategy'},
                                            {'label': 'Just Regression', 'value': 'justReg'},
                                            {'label': 'Just Classification', 'value': 'justClass'},
                                            {'label': 'Aggressive', 'value': 'aggressive'},
                                            {'label': 'Decision Tree Classification', 'value': 'decisionTree'},
                                            {'label': 'XGB Boost Classification', 'value': 'xgbBoost'},
                                            {'label': 'Kneighbour Classification', 'value': 'kNeighbour'},
                                            {'label': 'Linear Regression', 'value': 'lin-reg'},
                                            {'label': 'Kneighbour Regression', 'value': 'kNeighbour-reg'},
                                            {'label': 'Bayesian Regression', 'value': 'bay-reg'}],
                                            style={"margin-top":"25px"},
                                            value='allStrategy'

                            )
        return dropdown

    def layoutMaker(self):
        return html.Div([
            
            self.modal,
            dbc.Row(
                [
                    dcc.Interval(id='secondRefreshTime',interval=1*1000, n_intervals=0),
                    dcc.Interval(id='pageValueRefreshTime',interval=1*1000, n_intervals=0),
                    dbc.Col(dbc.NavbarBrand(id="timeInBlue",children=[""],style={"font-size":"30px",'color':'white',"margin-left":"10px",'margin-top':'15px','font-weight': 'bold'}),width={'size':2}),
                    dbc.Col(width={'size':5}),
                    dbc.Col(self.dropdownMaker(),width={'size': 2}),
                    dbc.Col(self.strategyDropdownMaker(),width={'size': 2}),
                    # dbc.Col(dbc.Button('Themes',id='themes'),width={'size':1},style={'margin-top':'24px'})
                    dbc.Col(self.createToastButton(),width={'size':1})],
                    style={'background-color': 'rgb(30, 144, 255)','height':'80px'}
            ),
            dbc.Row(
                [
                    dbc.Col(html.Div("Stock Name",style={"text-align":"center","font-size":"30px"}),width={'size':2}),
                    dbc.Col(html.Div("Stock Price",style={"text-align":"center","font-size":"30px"}),width={'size':2}),
                    dbc.Col(html.Div("Stock Graph",style={"text-align":"center","font-size":"30px"}),width={'size':5}),
                    dbc.Col(html.Div("Forecast",style={"text-align":"center","font-size":"30px"}),width={'size':3}),
                ]
            ),
            self.stockRowMaker('btcusdt'),
            #self.stockRowMaker('S&P 500',1000,14),
            html.Div(id='placeholder'),
            html.Div(id='countPlaceholder'),
            self.dbcToast()

        ])
    

    def imageLoader(self,src,height):
        
        test_base64 = base64.b64encode(open(src, 'rb').read()).decode('ascii')
        return html.Img(src='data:image/png;base64,{}'.format(test_base64),height=f"""{height}px""")
    

    def initialHomepagePrediction(self):
        # datas=self.database.dataForInitialPrediction('allStock')
        # prediction=self.trainedModels.homepagePrediction(*datas)

        
        # return self.imageLoader(self.listOfImages[prediction],270)
        datas=self.database.dataForPrediction('allStock')
        prediction=self.trainedModels.homepagePrediction(*datas)

        
        return self.imageLoader(self.listOfImages[prediction],270)
   
    def toastCallback(self,app):
        app.callback(
        Output("simple-toast", "is_open"),
        [Input("simple-toast-toggle", "n_clicks")],
    )(self.open_toast)

    def open_toast(self,n):
        if(n):
            return True
        return False

    def createToastButton(self):
        return dbc.Button(
            "help",
            id="simple-toast-toggle",
            color="warning",
            className="mb-3",
            n_clicks=0,
            style={"margin-top":"23px","width":"100px"}
        )

    
    def dbcToast(self):
        szoveg="""
        Az examine stock lehetőségnél van opciója kiválasztani hogy melyik alapból betöltött valutát szeretné mélyebben megvizsgálni. A mély vizsgálat az candlestick
        diagrammot és az egyéni modellek predikcióját jelenti. A pick strategy fülnél ki tudja választani hogy melyik stratégiát szeretné felhasználni. Ekkor a
        főképernyőn annak a stratégiának a becslése fog megjelenni. Lehetőségek között fel vannak sorolva számos stratégiák és ezek mellett összevontak is, pl. csak klasszifikációs-, regressziós 
        stratégiákat vegyük számításba, vegyük az összes stratégiát, vegyük az összes stratégiát de agresszívan (tehát ha valamennyire az egyik döntés felé hajlik az érték az lesz az)
        """
        t=dbc.Toast(
            [html.P(szoveg, className="mb-0")],
            id="simple-toast",
            header="usage information about graph",
            dismissable=True,
            is_open=False,
            fade=True,
            duration=60*1000,
            style={"position": "fixed", "top": 70, "right": 30, "width": 250},
        )
        return t



    def stockRowMaker(self,stockName):        
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
                dbc.Col(dcc.Graph(id=stockName+'_graph', figure=self.figInitialStyle(),config={'modeBarButtonsToRemove': 
                [ 'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d']})),
                dbc.Col(html.Div(id=stockName+'_predDiv',children=self.initialHomepagePrediction()),width=3)
            ])   




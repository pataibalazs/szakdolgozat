
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


class Modal:
    def __init__(self,database,models):
        self.database=database
        self.trainedModels=models
        self.listOfImages={
                -1:"/home/balazs/Desktop/meter/3 célváltozós meter/meter_sell_3.png",
                0:"/home/balazs/Desktop/meter/3 célváltozós meter/meter_neutral_3.png",
                1:"/home/balazs/Desktop/meter/3 célváltozós meter/meter_buy_3.png"
        }


    def imageLoader(self,src,height):
        
        test_base64 = base64.b64encode(open(src, 'rb').read()).decode('ascii')
        return html.Img(src='data:image/png;base64,{}'.format(test_base64),height=f"""{height}px""")


    def figInitialStyle(self):
        fig = plotly.subplots.make_subplots(rows=1, cols=1, vertical_spacing=0.2)
        fig['layout']['margin'] = {
                'l': 30, 'r': 10, 'b': 30, 't': 10
            }
        fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
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

        fig = go.Figure(data=[go.Candlestick(x=times,
                open=open,
                high=high,
                low=low,
                close=close)])
        fig.update_layout(xaxis_rangeslider_visible=False)
        fig.update_layout(go.Layout(height=400,width=1122,margin={'t': 0,'l':0,'b':0,'r':0}))
        return fig

        
    def createModal(self):
        datas=self.database.dataForPrediction('allStock')
        fa_pred=self.trainedModels.decisionTreePrediction(*datas)
        xgb_pred=self.trainedModels.xgbBoostPrediction(*datas)
        kneigh_pred=self.trainedModels.kneighbourPrediction(*datas)
        linear=self.trainedModels.linearRegressionPrediction(*datas)
        knnreg=self.trainedModels.knnRegressionPrediction(*datas)
        bay=self.trainedModels.bayesianRegressionPrediction(*datas)


        modal = html.Div([
        dbc.Modal(
            [
                dbc.Container
                ([
                   
                    dbc.Row([
                        dbc.Col([
                            html.Div(id="modalTime",children=[],style={"font-size":"20px",'color':'white','font-weight': 'bold','margin-top':'25px'})],width=3),
                        dbc.Col([
                            html.Div(children=["Bitcoin Inspection"],
                            style={"font-size":"35px",'color':'white','font-weight': 'bold','text-align':'center','margin-top':'13px','margin-right':'250px'})],width=9)
                        ],style={'background-color': 'rgb(30, 144, 255)','height':'80px'}),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='bitcoin_graph_modal', figure=self.figInitialStyle(),config={'modeBarButtonsToRemove': 
                [ 'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d']}),width=5),
                    ]),
                    html.Br(),
                    dbc.Row([
                    dbc.Col([dbc.Button("Decision Tree",style={"width":"100%",'font-weight': 'bold'},color='warning',disabled=True)],width=4),
                    dbc.Col([dbc.Button("XGBboost", style={"width": "100%",'font-weight': 'bold'},color='warning',disabled=True)],width=4),
                    dbc.Col([dbc.Button("KNeighbour",style={"width":"100%",'font-weight': 'bold'},color='warning',disabled=True)],width=4),
                    ]),
                    html.Br(),
                    dbc.Row([
                                

                    dbc.Col([html.Div(id='decisionTree_predDiv',children=self.imageLoader(self.listOfImages[fa_pred[0]],220))],width=4),
                    dbc.Col([html.Div(id='xgbBoost_predDiv',children=self.imageLoader(self.listOfImages[xgb_pred[0]],220))],width=4),
                    dbc.Col([html.Div(id='kneigh',children=self.imageLoader(self.listOfImages[kneigh_pred[0]],220))],width=4),

                    ]),
                    dbc.Row([
                    dbc.Col([dbc.Button("Linear Regression",style={"width":"100%",'font-weight': 'bold'},color='warning',disabled=True)],width=4),
                    dbc.Col([dbc.Button("KNN Regression", style={"width": "100%",'font-weight': 'bold'},color='warning',disabled=True)],width=4),
                    dbc.Col([dbc.Button("Bayesian Regression",style={"width":"100%",'font-weight': 'bold'},color='warning',disabled=True)],width=4),
                    ]),
                    html.Br(),
                    dbc.Row([
                    dbc.Col([html.Div(id='linear',children=self.imageLoader(self.listOfImages[linear[0]],220))],width=4),
                    dbc.Col([html.Div(id='knnreg',children=self.imageLoader(self.listOfImages[knnreg[0]],220))],width=4),
                    dbc.Col([html.Div(id='bayreg',children=self.imageLoader(self.listOfImages[bay[0]],220))],width=4),
                    ]),
                ]),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close", className="ml-auto",color="danger", n_clicks=0
                    )
                ),
            ],
            id="modal",
            is_open=False,
            size="xl")])

        return modal


    def updateModalCallback(self,app):
        app.callback(
            Output("modal", "is_open"),
            [Input("inspection_dropdown", "value"),Input("close", "n_clicks")],
            State("modal", "is_open")
            )(self.updateModal)

    def updateModal(self,value,n_clicks,is_open):
        if (value!=None or n_clicks):
            return not is_open
        return is_open
    
    def clearDropdownCallback(self,app):
        app.callback(
            Output("inspection_dropdown", "value"),
            Input("close", "n_clicks"),
            )(self.clearDropdown)

    def clearDropdown(self,n):
        return None


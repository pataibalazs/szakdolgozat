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
import homepage as hp
import database as db
import joblib
import pretrainedModels as tm
import initialisationClass as initialC
#import financeData as fd


# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# database=db.dataBase()
# models=tm.pretrainedModels()
# homepage=hp.homepage(database,models)
# homepage.timeUpdateCallback(app)
# homepage.gaugeRefreshCallback(app)
# homepage.updateGraphCallback(app)
# homepage.predictionUpdateCallback(app)
##dataMiningScript= fd.financeData(database,1600)

#app.layout = homepage.layoutMaker()

app=dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
init = initialC.initializationClass(app)
init.callbackStarter()
app.layout=init.layoutMaker()

if __name__ == "__main__":
    app.run_server(debug=True)






# def random(app):
#     if __name__ == "__main__":
#         app.run_server(debug=True)

# t1 = Thread(target = dataMiningScript.dataMiningCycle())
# t2 = Thread(target = random(app))


# t1.start()
# t2.start()
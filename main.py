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
#ez a warning elnyomás amiatt van itt mert egy dataframe-t várna be a predikciós modell de mi adatot adunk be neki, nem dataframe-t így az oszlopokhoz nevet kéne hozzáadni.
import warnings
warnings.filterwarnings("ignore", category=UserWarning) 

    
app=dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions = True)
init = initialC.initializationClass(app)
init.callbackStarter()
app.layout=init.layoutMaker()

if __name__ == "__main__":
    app.run_server(debug=True)


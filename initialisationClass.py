import dash_bootstrap_components as dbc
import dash
import homepage as hp
import database as db
import pretrainedModels as tm


class initializationClass:
    def __init__(self,app):
        self.app=app
        self.database=db.dataBase()
        self.models=tm.pretrainedModels()
        self.homepage=hp.homepage(self.database,self.models)
        self.layout=self.homepage.layoutMaker()
    
    def callbackStarter(self):
        self.homepage.timeUpdateCallback(self.app)
        self.homepage.gaugeRefreshCallback(self.app)
        self.homepage.updateGraphCallback(self.app)
        self.homepage.predictionUpdateCallback(self.app)
    
    def layoutMaker(self):
        return self.homepage.layoutMaker()
    

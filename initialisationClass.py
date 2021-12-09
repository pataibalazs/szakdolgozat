import dash_bootstrap_components as dbc
import dash
import homepage as hp
import database as db
import pretrainedModels as tm
import modal as m

class initializationClass:
    def __init__(self,app):
        self.app=app
        self.database=db.dataBase()
        self.models=tm.pretrainedModels()
        self.modal=m.Modal(self.database,self.models)
        self.homepage=hp.homepage(self.database,self.models,self.modal,self.modal.listOfImages)
        
        
    
    def callbackStarter(self):
        self.homepage.toastCallback(self.app)
        self.modal.updateModalCallback(self.app)
        self.modal.clearDropdownCallback(self.app)
        self.homepage.timeUpdateCallback(self.app)
        self.homepage.gaugeRefreshCallback(self.app)
        self.homepage.updateGraphsCallback(self.app)
        self.homepage.predictionUpdateCallback(self.app)
        

        
        
    
    def layoutMaker(self):
        return self.homepage.layoutMaker()
    

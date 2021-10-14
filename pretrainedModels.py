import joblib


class pretrainedModels:
    def __init__(self):
        self.decisionTree=joblib.load('/home/balazs/preTrainedModels/decisionTree.joblib')
    
    def decisionTreePrediction(self,close,high,low):
        prediction = self.decisionTree.predict([[close,high,low]])
        return prediction
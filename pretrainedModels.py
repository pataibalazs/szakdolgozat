import joblib
import warnings
import math
import numpy as np
#from hummingbird.ml import convert

class pretrainedModels:
    def __init__(self):
        self.decisionTree=joblib.load('/home/balazs/preTrainedModels/decisionTree.joblib')
        self.xgbBoost=joblib.load('/home/balazs/preTrainedModels/xgbBoost.joblib')
        self.kneighbour=joblib.load('/home/balazs/preTrainedModels/knear.joblib')

        #self.betterRandomForest=convert(self.randomForest,'pytorch')

    def normal_round(self,n):
        minus=False
        if (n==0):
            return 0
        if(n<0):
            minus=True
            n=abs(n)
        if(n>0):
            if n - math.floor(n) < 0.5:
                n= math.floor(n)
            n= math.ceil(n)
        if(minus==True):
            return -n
        else:
            return n

    def decisionTreePrediction(self,close,high,low):
        prediction = self.decisionTree.predict([[close,high,low]])
        return prediction

    def kneighbourPrediction(self,close,high,low):
        prediction = self.kneighbour.predict([[close,high,low]])
        return prediction
    
    def xgbBoostPrediction(self,close,high,low):
        lista=np.array([[close,high,low]])
        prediction = self.xgbBoost.predict(lista)
        return prediction

    def homepagePrediction(self,close,high,low):
        strategy=3
        tree=self.decisionTreePrediction(close,high,low)
        xgb=self.xgbBoostPrediction(close,high,low)
        neigh=self.kneighbourPrediction(close,high,low)
        
        #random=self.randomForestPrediction(close,high,low)
        print('-----------------')
        print(tree)
        print(xgb)
        print(neigh)


        # print(self.normal_round((tree[0]+xgb[0]+random[0])/strategy))
        # return self.normal_round((tree[0]+xgb[0]+random[0])/strategy)

        print(self.normal_round((tree[0]+xgb[0]+neigh[0])/strategy))
        return self.normal_round((tree[0]+xgb[0]+neigh[0])/strategy)
        #print(self.normal_round((tree[0])/strategy))
        #return self.normal_round((tree[0])/strategy)


p=pretrainedModels()
# print("kaki")
#print(p.xgbBoostPrediction(-0.000518,-0.000001,-0.000216))

import joblib
import warnings
import math
import numpy as np

class pretrainedModels:
    def __init__(self):
        self.decisionTree=joblib.load('/home/balazs/preTrainedModels/decisionTree.joblib')
        self.xgbBoost=joblib.load('/home/balazs/preTrainedModels/xgbBoost.joblib')
        self.kneighbour=joblib.load('/home/balazs/preTrainedModels/knear.joblib')
        self.linearRegression=joblib.load('/home/balazs/preTrainedModels/linearRegression.joblib')
        self.bayesianRegression=joblib.load('/home/balazs/preTrainedModels/bayesianRegression.joblib')
        self.knnRegression=joblib.load('/home/balazs/preTrainedModels/knnRegression.joblib')

    def my_round(self,szam,erzekenyseg):
        if(szam<0 and szam<-(erzekenyseg)):
            return -1
        elif(szam>0 and szam>erzekenyseg):
            return 1
        else:
            return 0
        
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

    def xgbBoostPrediction(self,close,high,low):
        lista=np.array([[close,high,low]])
        prediction = self.xgbBoost.predict(lista)
        return prediction

    def kneighbourPrediction(self,close,high,low):
        prediction = self.kneighbour.predict([[close,high,low]])
        return prediction
    
    def linearRegressionPrediction(self,close,high,low):
        prediction = self.linearRegression.predict([[close,high,low]])
        return [self.my_round(prediction,0.1)]
    
    def bayesianRegressionPrediction(self,close,high,low):
        prediction = self.bayesianRegression.predict([[close,high,low]])
        return [self.my_round(prediction,0.12)]

    def knnRegressionPrediction(self,close,high,low):
        prediction = self.knnRegression.predict([[close,high,low]])
        return [self.my_round(prediction,0.2)]

    def homepagePrediction(self,close,high,low):
        strategy=6
        tree=self.decisionTreePrediction(close,high,low)
        xgb=self.xgbBoostPrediction(close,high,low)
        neigh=self.kneighbourPrediction(close,high,low)
        linear=self.linearRegressionPrediction(close,high,low)
        knnreg=self.knnRegressionPrediction(close,high,low)
        bayreg=self.bayesianRegressionPrediction(close,high,low)
        
        print('-----------------')
        print(tree)
        print(xgb)
        print(neigh)
        print(linear)
        print(knnreg)
        print(bayreg)

        print(self.normal_round((tree[0]+xgb[0]+neigh[0]+linear[0]+bayreg[0]+knnreg[0])/strategy))
        return self.normal_round((tree[0]+xgb[0]+neigh[0]+linear[0]+bayreg[0]+knnreg[0])/strategy)
    
    def allStrategyHP(self,close,high,low):
        strategy=6
        tree=self.decisionTreePrediction(close,high,low)
        xgb=self.xgbBoostPrediction(close,high,low)
        neigh=self.kneighbourPrediction(close,high,low)
        linear=self.linearRegressionPrediction(close,high,low)
        knnreg=self.knnRegressionPrediction(close,high,low)
        bayreg=self.bayesianRegressionPrediction(close,high,low)
        
        print('-----------------')
        print(tree)
        print(xgb)
        print(neigh)
        print(linear)
        print(knnreg)
        print(bayreg)

        print(self.normal_round((tree[0]+xgb[0]+neigh[0]+linear[0]+bayreg[0]+knnreg[0])/strategy))
        return self.normal_round((tree[0]+xgb[0]+neigh[0]+linear[0]+bayreg[0]+knnreg[0])/strategy)
    
    def justClassificationHP(self,close,high,low):
        strategy=3
        tree=self.decisionTreePrediction(close,high,low)
        xgb=self.xgbBoostPrediction(close,high,low)
        neigh=self.kneighbourPrediction(close,high,low)

        
        print('-----------------')
        print(tree)
        print(xgb)
        print(neigh)

        print(self.normal_round((tree[0]+xgb[0]+neigh[0])/strategy))
        return self.normal_round((tree[0]+xgb[0]+neigh[0])/strategy)

    def justRegressionHP(self,close,high,low):
        strategy=3
        linear=self.linearRegressionPrediction(close,high,low)
        knnreg=self.knnRegressionPrediction(close,high,low)
        bayreg=self.bayesianRegressionPrediction(close,high,low)
        print('-----------------')
        print(f"close: {close} | high: {high} | low: {low}")
        print(linear)
        print(knnreg)
        print(bayreg)

        print(self.normal_round((linear[0]+bayreg[0]+knnreg[0])/strategy))
        return self.normal_round((linear[0]+bayreg[0]+knnreg[0])/strategy)

    def aggressive(self,close,high,low):
        strategy=6
        tree=self.decisionTreePrediction(close,high,low)
        xgb=self.xgbBoostPrediction(close,high,low)
        neigh=self.kneighbourPrediction(close,high,low)
        linear=self.linearRegressionPrediction(close,high,low)
        knnreg=self.knnRegressionPrediction(close,high,low)
        bayreg=self.bayesianRegressionPrediction(close,high,low)
        
        print('-----------------')
        print(tree)
        print(xgb)
        print(neigh)
        print(linear)
        print(knnreg)
        print(bayreg)

        szam=(tree[0]+xgb[0]+neigh[0]+linear[0]+bayreg[0]+knnreg[0])/strategy
        if(szam>0):
            szam=math.ceil(szam)
        elif(szam<0):
            szam=math.floor(szam)
        else:
            szam=0

        return szam







# p=pretrainedModels()
# # print("kaki")
# print(p.decisionTreePrediction(0.000587,0.000618,0.000963))

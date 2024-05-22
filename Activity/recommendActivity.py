import pandas as pd
import numpy as np
import geopy.distance
from  .utils import getDistance2Point, getListPhase1, getListPhase2 ,  nightOpenTime, generate_combinations ,ThreePoint 
import operator 

class ActivityRecommend:
    def __init__(self , days ,city , types , maxBudget , df ) :
        self.city = city
        self.days = days
        self.types = types
        self.maxBudget = maxBudget
        self.df = df 

        self.finalPlan1 = []
        self.spendingPlan1 = 0

        self.finalPlan2 = []
        self.spendingPlan2 = 0

        self.finalPlan3 = []
        self.spendingPlan3 = 0


    def perform(self):
        getDF = getListPhase1(self.types , self.city , self.df )
        getDF2 = getListPhase2( self.city , self.df )

        numberActivity = self.days * 3 + self.days + 2

        if len(getDF) < numberActivity:
            i = 0
            while len(getDF) <  numberActivity:
                if getDF2['idActivity'].iloc[i] not in list(getDF['idActivity']):
                    getDF.loc[len(getDF)] = getDF2.iloc[i]
                i+=1

        nightOpenDF = nightOpenTime(self.df, self.city)
        nightOpenDF.drop_duplicates(inplace=True)

        ## GET OPEN NIGHT 
        getDFNight  = pd.DataFrame(columns=getDF.columns)

        for i in range(len(getDF)):
            if getDF['idActivity'].iloc[i] in list(nightOpenDF['idActivity']):
                getDFNight.loc[len(getDFNight)] = getDF.iloc[i]

        if len(getDFNight) < self.days+2:
            i= 0
            while len(getDFNight) < self.days + 2:
                if getDF2['idActivity'].iloc[i] in list(nightOpenDF['idActivity']) and  getDF2['idActivity'].iloc[i] not in list(getDFNight['idActivity']):
                    getDFNight.loc[len(getDFNight)] = getDF2.iloc[i]
                i+=1 

        if len(getDFNight) > self.days+2:
            getDFNight= getDFNight[:self.days+2]

        for i in getDF['idActivity']:
            if i in list(getDFNight['idActivity']):
                getDF = getDF[getDF['idActivity'] != i]
        
        if len(getDF) > numberActivity:
            getDF = getDF[:numberActivity]

        n = len(getDF) - 1
        m = len(getDFNight)
        k = 2
        getPoint  = generate_combinations(n, k)
        allGetPoint = list()
        for i in getPoint:
            for j in range(m):
                i.append(j)
                allGetPoint.append(i.copy())
                i.pop(-1)

        dctActivity = {}
        for index, val in enumerate(allGetPoint):
            perform = ThreePoint(val.copy() , getDF , getDFNight )
            perform.getTotalDistance()
            dctActivity[index] = [perform.distance , perform.points , perform.nightpoint]


        import operator 
        dctActivity  =  sorted(dctActivity .items(), key=operator.itemgetter(1))

        def getSpendingActivity( plan  , planNight , maxBudget):
            sumSpending = 0
            for i in plan:
                sumSpending += getDF['priceActivity'].iloc[i]
            for i in planNight:
                sumSpending += getDFNight['priceActivity'].iloc[i]

            if maxBudget > sumSpending:
                return sumSpending, True
            return sumSpending , False
        
    
        plan1 = set()
        planNight1  = set()
        finalPlan1 = []

        sumSpending1 = 0

        for i , val in dctActivity:
            _, points, night = val
            if night not in planNight1 and len(planNight1) < self.days:
                plan1.update(points)
                planNight1.add(night)
                for i in points:
                    finalPlan1.append(getDF['idActivity'].iloc[i])
                finalPlan1.append(getDFNight['idActivity'].iloc[night])
        
                ## Check Budget Activity
                sumSpending1 , checkBuget1 = getSpendingActivity(plan1, planNight1, self.maxBudget)
                if checkBuget1 == False:
                    plan1 = set()
                    planNight1  = set()
                    finalPlan1 = []
        self.finalPlan1 = finalPlan1
        self.spendingPlan1 = sumSpending1

    

        plan2 = set()
        planNight2  = set()
        finalPlan2 = []

        sumSpending2 = 0

        for i , val in dctActivity[2:]:
            _, points, night = val
            if night not in planNight2 and len(planNight2) < self.days:
                plan2.update(points)
                planNight2.add(night)
                for i in points:
                    finalPlan2.append(getDF['idActivity'].iloc[i])
                finalPlan2.append(getDFNight['idActivity'].iloc[night])
        
                ## Check Budget Activity
                sumSpending2 , checkBuget2 = getSpendingActivity(plan2, planNight2 , self.maxBudget)
                if checkBuget2 == False:
                    plan2 = set()
                    planNight2 = set()
                    finalPlan2 = []
        self.finalPlan2 = finalPlan2
        self.spendingPlan2 = sumSpending2


        plan3= set()
        planNight3  = set()
        finalPlan3 = []

        sumSpending3 = 0

        for i , val in dctActivity[4:]:
            _, points, night = val
            if night not in planNight3 and len(planNight3) < self.days:
                plan3.update(points)
                planNight3.add(night)
                for i in points:
                    finalPlan3.append(getDF['idActivity'].iloc[i])
                finalPlan3.append(getDFNight['idActivity'].iloc[night])
        
                ## Check Budget Activity
                sumSpending3 , checkBuget3 = getSpendingActivity(plan1, planNight1, self.maxBudget)
                if checkBuget3 == False:
                    plan3 = set()
                    planNight3  = set()
                    finalPlan3 = []
        self.finalPlan3 = finalPlan3
        self.spendingPlan3= sumSpending3
        


    



        












    


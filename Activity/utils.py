import pandas as pd
import numpy as np
import geopy.distance

def getListPhase1( types , city , df ): 
    
    getDF = pd.DataFrame(columns=df.columns)
    for val in types:
        getDF2 =  df[(df['typeActivity'] == val) & (df['city'] == city )  ]
        getDF  = pd.concat([getDF,getDF2])

    weight_rating = 0.06
    weight_comments = 0.04
 
    lstRateActivity    = getDF['rateActivity'].apply(lambda x: x * weight_rating  if x != 'nan' else 3* weight_rating)  
    lstCommentActivity =  getDF['numComment'].apply(lambda x:  x * weight_rating  if x != 'nan' else 100* weight_comments) 
    getDF['popularity'] = [sum(i) for i in zip(lstRateActivity,lstCommentActivity)]
    getDF.sort_values(by='popularity' , ascending=False  , inplace=True)
    getDF.drop('popularity' , axis=1, inplace=True)
    
    return getDF

def getListPhase2( city , df ):
        
    getDF2 = df[ df['city'] == city ]

    weight_rating = 0.06
    weight_comments = 0.04
 
    lstRateActivity    = getDF2['rateActivity'].apply(lambda x: x * weight_rating  if x != 'nan' else 3* weight_rating)  
    lstCommentActivity =  getDF2['numComment'].apply(lambda x:  x * weight_rating  if x != 'nan' else 100* weight_comments) 
    getDF2['popularity'] = [sum(i) for i in zip(lstRateActivity,lstCommentActivity)]
    getDF2.sort_values(by='popularity' , ascending=False  , inplace=True)
    getDF2.drop( 'popularity' ,axis=1, inplace=True )
    
    
    return getDF2[:40]

def getDistance2Point(point1, point2):
    if point1 == "(0, 0)" or point2 == "(0, 0)":
        return 1000
    _,lat1 , _ , lon1,*_ = point1.split("'")
    _,lat2 , _ , lon2,*_ = point2.split("'")
    coords_1 = (lat1,lon1)
    coords_2 = (lat2,lon2)  
    return geopy.distance.geodesic(coords_1, coords_2).km



def nightOpenTime(df , city ):
    nightDF = pd.DataFrame( columns=df.columns)
    timeNight = [0,1]
    df = df[ df['city'] == city]
    df =   df[(df['openTime'].isna() == False) | (df['closeTime'].isna() == False) ]
    
    for i , val in enumerate(df['openTime']):
        getTime,_ = str(val).split(':')
        if int(getTime) >= 16:
            nightDF.loc[len(nightDF)] = df.iloc[i]

    for i , val in enumerate(df['closeTime']):
        getTime,_ = str(val).split(':')
        if int(getTime) > 17 or int(getTime) in timeNight:
            nightDF.loc[len(nightDF)] = df.iloc[i]
            
    return nightDF

def generate_combinations(n, k):
    result = []
    combination = []
    
    def backtrack(start):
        if len(combination) == k:
            result.append(combination[:])
            return
        for i in range(start, n + 1):
            combination.append(i)
            backtrack(i + 1)
            combination.pop()
    
    backtrack(0)
    return result

class ThreePoint:
    def __init__(self , points : list ,  getDF , getDFNight ):
        ## INPUT
        self.point1 = points[0]
        self.point2 = points[1]
        self.getDF = getDF
        self.getDFNight = getDFNight
        
        self.nightpoint = points[2]

        ## OUTPUT
        self.distance = 1000
        self.points = list()
    
    def getTotalDistance(self):        
        ## Case 1
        dis1_2 = getDistance2Point( self.getDF['distance'].iloc[self.point1] , self.getDF['distance'].iloc[self.point2] )
        dis2_night = getDistance2Point(self.getDF['distance'].iloc[self.point2] , self.getDFNight['distance'].iloc[self.nightpoint] )
        disTotalCase1 = dis1_2 + dis2_night

        ## Case 2
        dis2_1= getDistance2Point( self.getDF['distance'].iloc[self.point2] , self.getDF['distance'].iloc[self.point1] )
        dis1_night = getDistance2Point( self.getDF['distance'].iloc[self.point1] , self.getDFNight['distance'].iloc[self.nightpoint] )
        disTotalCase2 = dis2_1 + dis1_night

        if disTotalCase2 < disTotalCase1:
            self.points.append(self.point2)
            self.points.append(self.point1)
        else:
            self.points.append(self.point1)
            self.points.append(self.point2)

        self.distance =  min(disTotalCase1, disTotalCase2)








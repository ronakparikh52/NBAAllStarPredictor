from Data import Data
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

import time as t
#Creating Data

incorrect = True
while incorrect:
    years = input("Which years will you want the data from? Add multiple years with a space: ").split()
    incorrect = False
    for index, year in enumerate(years):
        try:
            year = int(year.replace(",", ""))
            years[index] = year
            if year < 1950 or year > 2024:
                print("Please enter valid years (between 1950 and 2024)")
                incorrect = True
                break
        except ValueError:
            print("Please enter a valid year")
            incorrect = True
            break

data = Data()
dfyear = []
seconds = len(years) * 3
print()
print("Delay is added to ensure webscraping works properly")
print("Results will show in")
for year in years:
    dfyear.append(data.finalData(year))
    print(seconds)
    t.sleep(1)
    seconds -=1
    print(seconds)
    t.sleep(1)
    seconds -=1
    print(seconds)
    t.sleep(1)
    seconds -=1

df = pd.concat(dfyear, axis=0)



#Creating x and y variables 
y = df['All Star']
x = df.drop(['All Star', 'Name'], axis = 1)

#Splitting the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 100)

#TRAIN MODEL
  
lr = LogisticRegression(max_iter=2000)
lr.fit(x_train, y_train)

y_train_predict = lr.predict(x_train)
y_test_predict = lr.predict(x_test)

# EVALUATE MODEL PERFORMANCE

def DatasetStats(actualData, predictedData, type):
    zeroTotal = 0
    zeroCorrect = 0
    oneTotal = 0
    oneCorrect = 0
    for actual, predicted in zip(actualData, predictedData):
        if actual == 0:
            zeroTotal+=1
            if predicted == 0:
                zeroCorrect+=1
        else:
            oneTotal+=1
            if predicted == 1:
                oneCorrect+=1
    
    zeroAccuracy = zeroCorrect/zeroTotal * 100
    oneAccuracy = oneCorrect/oneTotal * 100
    macroAvg = (zeroAccuracy + oneAccuracy) / 2
    weightedAvg = (zeroCorrect + oneCorrect) / (zeroTotal + oneTotal) * 100

    matrix =[
            [zeroCorrect, zeroTotal-zeroCorrect],
            [oneTotal-oneCorrect, oneCorrect]          
            ]
    
    confusionMatrix = pd.DataFrame(matrix, columns = ['Predicted Non-All Stars', 'Predicted All Stars'])
    row_names = ['Actual Non-All Stars', 'Actual All Stars']
    confusionMatrix.index = row_names
    print()
    print(f"{type.upper()} DATASET STATISTICS")
    print()

    print("CONFUSION MATRIX:")
    print()
    print(confusionMatrix)
    print()

    print(f"Non-All Star Accuracy: {round(zeroAccuracy, 2)}%")
    print(f"All Star Accuracy: {round(oneAccuracy, 2)}%")
    print(f"Macro Average: {round(macroAvg, 2)}%")
    print(f"Weighted Average: {round(weightedAvg, 2)}%")
    print()
    print()

DatasetStats(y_train, y_train_predict, "train")
DatasetStats(y_test, y_test_predict, "test")
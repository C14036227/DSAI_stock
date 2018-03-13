#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 18:11:27 2018

@author: james
"""

from pandas import DataFrame, Series
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from matplotlib.finance import candlestick_ohlc

title = [
        'Open',
        'High',
        'Low',
        'Close',
        ]
df = pd.DataFrame()
dtr = pd.read_csv('training_data.csv', header=None, names = title)
dtr = pd.read_csv('testing_data.csv', header=None, names = title)
df = pd.concat([dtr, df])

op, hi, lo, clo = df.iloc[:,0], df.iloc[:,1], df.iloc[:,2], df.iloc[:,3]
x = 0
ohlc = []
while x < len(df):
    app_tmp = x, op[x], hi[x], lo[x], clo[x]
    ohlc.append(app_tmp)
    x+=1

fig, ax1 = plt.subplots()
#candlestick_ohlc(ax1, ohlc, width=0.6, colorup='r', colordown='black')


upline = (df.High - df[['Open','Close']].max(axis=1)).to_frame()
dwline = (df[['Open','Close']].min(axis=1) - df.Low).to_frame()
amount = df.Close - df.Open
growth = amount > 0
nogrow = amount == 0
long = abs(df.Close - df.Open) > 10
middle = (abs(df.Close - df.Open) < 10) & (abs(df.Close - df.Open) >5)

x = 5
y = 0
it = 0
sumtmp = clo[0]
mean_5 = []
mean_20 = []
mean_60 = []
mean_180 = []
mean_5.append(sumtmp)
mean_20.append(sumtmp)
mean_60.append(sumtmp)
mean_180.append(sumtmp)
sumtmp = 0
for y in range(1,5):
    sumtmp+=clo[y-1]
    mean_5.append(sumtmp/y)
sumtmp = 0
for y in range(1,20):
    sumtmp+=clo[y-1]
    mean_20.append(sumtmp/y)
sumtmp = 0
for y in range(1,60):
    sumtmp+=clo[y-1]
    mean_60.append(sumtmp/y)
sumtmp = 0
for y in range(1,180):
    sumtmp+=clo[y-1]
    mean_180.append(sumtmp/y)
sumtmp = 0
while x < len(df):
    if x >= 180:
        for y in range(x-180, x):
            sumtmp+=clo[y]
        mean_180.append(sumtmp/180)
        sumtmp=0
    if x >= 60:
        for y in range(x-60, x):
            sumtmp+=clo[y]
        mean_60.append(sumtmp/60)
        sumtmp=0
    if x >= 20:
        for y in range(x-20, x):
            sumtmp+=clo[y]
        mean_20.append(sumtmp/20)
        sumtmp=0
    for y in range(x-5, x):
        sumtmp+=clo[y]
    mean_5.append(sumtmp/5)
    sumtmp=0
    x+=1

x_ran = range(len(df))
plt.plot(x_ran, mean_5)
plt.plot(x_ran, mean_20)
plt.plot(x_ran, mean_60)
plt.plot(x_ran, mean_180)    
    
#manipulate starts, first consider 5MA
status = 0
act_arr = []
stat_arr = []
stat_arr.append(0)
price_b = 0
price_s = 0
sig1 = False #5 over 20
sig2 = False #5 over 60
sig3 = False #5 over 180
profit = 0
trade_sig = True

#moving avg calculation case

for y in range(len(df)-1):
    
    if y >= 5 and trade_sig:
        trade_sig = False
        sig1 = mean_5[y] > mean_20[y] #after trading, new action next day
        if sig1 and status == 0:
            status = 1
            price_b = op[y+1]
            act_arr.append(int(1))
            stat_arr.append(status)
            continue
        elif status == 0:
            status = -1
            price_s = op[y+1]
            act_arr.append(int(-1))
            stat_arr.append(status)
            continue
            
    
    sig1 = (mean_5[y-1] - mean_20[y-1])*(mean_5[y]-mean_20[y])<0
    sig2 = (mean_5[y-1] - mean_60[y-1])*(mean_5[y]-mean_60[y])<0
    sig3 = (mean_5[y-1] - mean_180[y-1])*(mean_5[y]-mean_180[y])<0
    
    rule1 = [sig1 and mean_5[y] > mean_20[y],
             sig2 and mean_5[y] > mean_60[y],
             sig3 and mean_5[y] > mean_180[y]
         ]
    
    rule2 = [sig1 and mean_5[y] < mean_20[y],
             sig2 and mean_5[y] < mean_60[y],
             sig3 and mean_5[y] < mean_180[y]
         ]
    
    if any(rule1):
        if status!=1:
            status = status+1
            act_arr.append(int(1))
            stat_arr.append(status)
            price_b = op[y+1]
            if status == 0:
                    profit += price_s - price_b
                    print(price_s - price_b, price_b, price_s, y)
                    price_s = 0
                    price_b = 0
                    trade_sig = True
        else:
            stat_arr.append(status)
            act_arr.append(int(0))
    elif any(rule2):
        if status !=-1:
            status = status-1
            act_arr.append(int(-1))
            stat_arr.append(status)
            price_s = op[y+1]
            if status == 0:
                profit += price_s - price_b
                print(price_s - price_b, price_s, price_b, y)
                price_s = 0
                price_b = 0
                trade_sig = True
        else:
            stat_arr.append(status)
            act_arr.append(int(0))
    else:
        stat_arr.append(status)
        act_arr.append(int(0))

if stat_arr[len(df)-1] == 1:
    profit+=clo[len(df)-1] - price_b
elif stat_arr[len(df)-1] == -1:
    profit+=price_b - clo[len(df)-1]

print(profit)
np.savetxt('output.csv', act_arr, fmt = '%d')
    


if __name__ == '__main__':
    # You should not modify this part.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--training',
                       default='training_data.csv',
                       help='input training data file name')
    parser.add_argument('--testing',
                        default='testing_data.csv',
                        help='input testing data file name')
    parser.add_argument('--output',
                        default='output.csv',
                        help='output file name')
    args = parser.parse_args()
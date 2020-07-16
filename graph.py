# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 16:24:05 2020

@author: marya
"""

import pandas as pd

df = pd.read_csv('results.csv')

df.shape

df.keys()


emma = df[df.name=='emma']

not_emma = df[~(df.name=='emma')]

truevalues = [emma[emma.label==True].label.count(),not_emma[not_emma.label==True].label.count()]
falsevalues = [emma[emma.label==False].label.count(),not_emma[not_emma.label==False].label.count()]

print(emma.shape, not_emma.shape)

import matplotlib.pyplot as plt
import numpy as np

ind = np.arange(2)
p1 = plt.bar(ind, truevalues, width=0.5)
p2 = plt.bar(ind, falsevalues, width=0.5, bottom=truevalues)

plt.ylabel('Count')
plt.title('Predictions')
plt.xticks(ind, ('Emma', 'Not emma'))
plt.legend((p1[0], p2[0]), ('True', 'False'))
plt.show()
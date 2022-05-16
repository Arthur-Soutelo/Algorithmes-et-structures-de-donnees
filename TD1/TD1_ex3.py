"""
INF-tc1
Created on Mon Jan 31 08:07:15 2022
@author: Arthur

TD 1
"""
# Exercice V-3

import random

echantillon = [random.gauss(16,2) for i in range (100)]
def moyenne(a):
    moy = sum(a)/len(a)
    print (moy)
    return(moy)

mi = moyenne(echantillon)
list2 = [None]*100

for i, item in enumerate(echantillon):
    list2[i] = (item - mi)*(item - mi)

variance = moyenne(list2)
print ('Variance : ', variance)
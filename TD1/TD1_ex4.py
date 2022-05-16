"""
INF-tc1
Created on Mon Jan 31 08:07:15 2022
@author: Arthur

TD 1
"""
# Exercice V-4

import random
import statistics
import numpy

echantillon = [random.gauss(16,2) for i in range (100)]
moy = statistics.mean(echantillon)
echantillon2 = numpy.power(echantillon,2)

list2 = [None]*len(echantillon)

for i, item in enumerate(echantillon):
    list2[i] = numpy.power(item,2) - numpy.power(moy,2)

variance = abs((1/len(echantillon)) * sum(list2))
print ('Variance : ', variance)
"""
INF-tc1
Created on Mon Jan 31 08:07:15 2022
@author: Arthur

TD 1
"""
# Exercice V-2
# Reprendre l’exemple du calcul des racines d’une équation de seconde degré et placer les calculs dans la fonction
# quadratique(a, b, c) qui reçoit en paramètre les coefficients a,b et c et renvoie les racines de cette équation.

import math;


def quadratique(a,b,c):    
    if (a == 0):
        if (b != 0):
            print ('Pas de seconde degre. Racine simple x = ', -c/b)
            
    else:
        delta = (b^2 - 4*a*c)
    
        if (delta < 0):
            print ('Pas de racine reel')
        else:
            if (delta > 0):
                x1 = (-b + math.sqrt(delta))/(2*a)
                x2 = (-b - math.sqrt(delta))/(2*a)
                print ('x1 = ', x1)
                print ('x2 = ', x2)
            else:
                x1 = x2 = -b/(2*a)
                print ('Racine double x1 = x2 = ', x1)

quadratique(0,30,6)
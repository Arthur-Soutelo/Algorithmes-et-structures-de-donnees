"""
INF-tc1
@author: Arthur

TD 1
"""
# Exercice VIII-2

def convertir(S):
    str1 = ''.join(S)
    if (str1.isdigit()):
        int(str1)
        print('Safe')
    else:
        print('Pas possible. String contient valeurs non acceptees')
        
string = ['1','2','3']       
convertir(string)
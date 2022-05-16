"""
INF-tc1
@author: Arthur

TD 1
"""
# Exercice VIII-2

def convertir2r(S):
    str1 = '.'.join(S)
    print(str1)
    if (isinstance(str1, float)):
        float(str1)
        print('Safe')
    else:
        print('Pas possible. String contient valeurs non acceptees')
        
string = ['1','2','3']       
convertir2r(string)
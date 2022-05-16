"""
Authors: Arthur SOUTELO ARAUJO
         Valentin CHAZALON
"""
from math import inf
import time
import tracemalloc

#%% Partie 1
#%% Exercice 1.1
def Monnaie_Gloutonne_Illimite(S,M):
    M1=M
    T=[]
    for i in reversed(range(13)):
        if S[i]<=M1 and M1!=0:
            A=M1//S[i]
            T.insert(0,A)
            M1=M1-A*S[i]
        else:
            T.insert(0,0)
    return(T,sum(T))
        
print('\nExercice 1.1 : \n')    
S=(1,2,5,10,20,50,100,200,500,1000,2000,5000,10000)
M=23665
print(Monnaie_Gloutonne_Illimite(S, M))

#%% Exercice 1.2 et 1.3 :
def Monnaie_Gloutonne_Limite(S,M,D):
    M1=M
    T=[]
    for i in reversed(range(13)):
        if S[i]<=M1 and M1!=0 and D[i] > 0:
            A=M1//S[i]
            if A <= D[i]:
                T.insert(0,A)
                D[i] = D[i]-A
                M1=M1-A*S[i]
            else:
                T.insert(0,D[i])
                M1=M1-(D[i])*S[i]
                D[i] = 0
        else:
            T.insert(0,0)
    return(T,sum(T))
 
    print('\nExercice 1.2 et 1.3 : \n')
S=(1,2,5,10,20,50,100,200,500,1000,2000,5000,10000)
M=23665
D = [10000,5000,2000,1000,500,200,100,50,20,10,5,2,1]       # Nombre de pieces disponibles
print(Monnaie_Gloutonne_Limite(S, M, D))  
print(D)       

#%% Partie 2
#%% Exercice 2.1 et 2.2 :
def Monnaie_graphe(S:list[int], M:int, D:list[int]): #fonction récursive qui crée l'arbre sous la forme d'un dict
    graphe = {M : [(M-S[i]) for i in range(len(S))]}
    def Niveau_graphe(S, M, D, niveau):
        new = {}
        for argent ,list_monaies in niveau.items():
            for unit in list_monaies:
                
                rest = []
                for valeur_monaie in S:
                    if valeur_monaie <= unit:
                        rest.append(unit-valeur_monaie)
                new[unit] = rest
        return new

    while 0 not in graphe.keys() and len(graphe)>0 :
        new = Niveau_graphe(S, M, D, graphe)
        graphe = graphe | new       # Merge dicts
        
    return graphe
  
print('\nExercice 2.1 : \n')
S = (1,2,5,10)
D = [10,10,10,10]
M = 15      
print(Monnaie_graphe(S, M, D))

#%% Partie 3 : Algorithme de Programmation Dynamique
#%% Exercice 3.1
def Monnaie_matrice(S:list[int], M:int):
    mat =[[0 for k in range(M+1)] for i in range(len(S)+1)]     #Creation de la Matrice avec zeros
    
    for i in range(len(S)+1):
        for m in range(M+1):
            if m == 0:
                mat[i][m] = 0
            elif i == 0:
                mat[i][m] = inf
            else:
                if m - S[i-1] >= 0:
                   val1 = 1 + mat[i][m - S[i-1]]
                else: 
                    val1 = inf
                
                if i >= 1:
                    val2 = mat[i-1][m]
                else:
                    val2 = inf
                
                mat[i][m] = min(val1, val2)
    return mat

print('\nExercice 3.1 : \n')
S = (1,2,5,10)
D = [10,10,10,10]
M = 27
print(Monnaie_matrice(S, M))

#%% Exercice 3.2
def pieces_utilisees(S:list[int], M:int):           #Matrice 3 dimensions
    mat = Monnaie_matrice(S, M)
    
    mat_pieces = [[0 for k in range(M+1)] for i in range(len(S)+1)]     
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            s_utilisees = []
            if i == 0 or j == 0:
                s_utilisees.append(0)
            else:
                if j - S[i-1] >= 0:
                    s_utilisees.append(S[i-1])
                    rest = j - S[i-1]
                    m = 1
                    while len(s_utilisees) < mat[i][j]:
                        if S[i-m] <= rest:
                            s_utilisees.append(S[i-m])
                            rest = rest - S[i-m]
                        else:
                            m = m+1
                else:
                    for k in reversed(range(len(S))):
                        if S[k] <= j and mat[i][j] != len(s_utilisees):
                            s_utilisees.append(S[k])
                            rest = j - S[k]
                            m = 0
                            while rest > 0:
                                if S[k-m] <= rest:
                                    s_utilisees.append(S[k-m])
                                    rest = rest - S[k-m]
                                else:
                                    m = m+1
            mat_pieces[i][j] = s_utilisees
    return mat_pieces                       # Matrice où chaque element est les pieces necessaires

print('\nExercice 3.2 : \n')
S = (1,2,5,10)
D = [10,10,10,10]
M = 16
print(pieces_utilisees(S, M))

#%% Exercice 3.3
def Monnaie_limite(S:list[int], M:int, D:list[int]):
    mat = Monnaie_matrice(S, M)
    T = {value : 0 for value in S}
    
    i = len(S)
    j = M
    if mat[-1][-1] == inf:
        return None
    else:
        while mat[i][j] > 0:
            if mat[i][j] == mat[i-1][j] and T[S[i-1]] < D[i-1]:
                if i > 0:
                    i = i - 1
            elif S[i-1] < j and T[S[i-1]] < D[i-1]:
                j = j - S[i-1]
                T[S[i-1]] += 1
            else:
                if i > 1:
                    i = i - 1
                j = j - S[i-1]
                T[S[i-1]] += 1
        return T        # Dictionaire avec les pieces qui doivent être utilisées

""""""" Un autre example de code, mais qui fait une matrice de 3 dimensions : """""""

# def Monnaie_limite(S:list[int], M:int, D:list[int]): 
#     mat = Monnaie_matrice(S, M)
    
#     mat_pieces = [[0 for k in range(M+1)] for i in range(len(S))]   # Matrice 3 dimensions
#     for i in range(len(mat)):
#         for j in range(len(mat[i])):
#             D_copy = D.copy()       # Pour ne pas changer les valeurs de D
#             s_utilisees = []        # Vecteur qui contient le pieces utilisées
#             if i == 0 or j == 0:
#                 s_utilisees.append(0)
#             else:
#                 if j - S[i-1] >= 0 and D_copy[i-1] > 0:     # Si une sole piece ne sufit pas
#                     s_utilisees.append(S[i-1])
#                     D_copy[i-1] = D_copy[i-1]-1
                    
#                     rest = j - S[i-1]
#                     m = 1
#                     while len(s_utilisees) < mat[i][j]:     
#                         if S[i-m] <= rest and D_copy[i-m] > 0:
#                             s_utilisees.append(S[i-m])
#                             D_copy[i-m] = D_copy[i-m]-1
#                             rest = rest - S[i-m]
#                         elif S[i-m] <= rest and D_copy[i-m] == 0:
#                             if rest >= S[i-(m+1)]:
#                                 m = m + 1
#                                 s_utilisees.append(S[i-m])
#                                 rest = rest - S[i-m]
#                                 while rest > 0:
#                                     if rest >= S[i-m]:
#                                         s_utilisees.append(S[i-m])
#                                         rest = rest - S[i-m]
#                                         m = m + 1
#                                     else:
#                                         m = m + 1
#                             else:
#                                 s_utilisees.append(None)
#                         else:
#                             m = m+1       
#                 else:                                       # Si le valeur j est plus petit que la piece actuelle
#                     for k in reversed(range(len(S))):
#                         if S[k] <= j and mat[i][j] != len(s_utilisees):
#                             s_utilisees.append(S[k])
#                             rest = j - S[k]
#                             m = 0
#                             while rest > 0:
#                                 if S[k-m] <= rest:
#                                     s_utilisees.append(S[k-m])
#                                     rest = rest - S[k-m]
#                                 else:
#                                     m = m+1
#             mat_pieces[i][j] = s_utilisees
#     return mat_pieces

print('\nExercice 3.3 : \n')
S = (1,2,5,10)
D = [8,10,0,10]
M = 29
print(Monnaie_limite(S, M, D))
    
#%% Exercice 3.4 et 3.5
def Matrice_poids(S:list[int], M:int, P:list[float]):       # Chaque élement de la matrice est le poids equivalent
    mat =[[0 for k in range(M+1)] for i in range(len(S)+1)]
    
    for i in range(len(S)+1):
        for m in range(M+1):
            if m == 0:
                mat[i][m] = 0
            elif i == 0:
                mat[i][m] = inf
            else:
                if m - S[i-1] >= 0:
                   val1 = P[i-1] + mat[i][m - S[i-1]]
                else: 
                    val1 = inf
                
                if i >= 1:
                    val2 = mat[i-1][m]
                else:
                    val2 = inf
                
                mat[i][m] = min(val1, val2)
    return mat

def Monnaie_poids(S:list[int], M:int, P:list[float]):       # Prendre les pieces utilisés pour le poids
    mat = Matrice_poids(S, M, P)
    rendu =[0 for k in range(len(S))]

    i = len(S)
    j = M
    if mat[-1][-1] == inf:
        return None
    else:
        while mat[i][j] > 0:
            if mat[i][j] == mat[i-1][j]:
                i = i - 1
            else:
                j = j - S[i-1]
                rendu[i-1] = rendu[i-1]+1
    return rendu


print('\nExercice 3.4 et 3.5 : \n')
S = (1, 3, 4, 7)
M = 7
P = (10, 27, 32, 55)
print(Matrice_poids(S, M, P))
print('\n')
print(Monnaie_poids(S, M, P))

#%% Exercice 3.6
def Poids_Gloutonne(S:list[int], M:int, P:list[float]):
    L = [(P[i]/S[i], S[i], P[i]) for i in range(len(S))]
    
    # take first element for sort
    def takeFirst(elem):
        return elem[0]
    L.sort(key=takeFirst)
    
    Mprime = M
    res = 0
    
    i = 0
    while Mprime >0:
        (r,s,p) = L[i]
        i = i + 1
        if s <= Mprime:
            res = res + p*(Mprime // s)
            Mprime = Mprime % s
        
    return res

print('\nExercice 3.6 : \n')
S = (1, 3, 4, 7)
M = 6
P = (10, 27, 32, 55)
print(Poids_Gloutonne(S, M, P))

#%% Exercice 3.6 : Examples
S = (1, 3, 4, 7)
P = (10, 27, 32, 55)

valeurs = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
glutonne = []
dynamique = []
for v in valeurs:
    poids = Monnaie_poids(S, v, P)
    poids_int = 0
    for i in range(len(poids)):
        poids_int = poids_int + poids[i]*P[i]
    dynamique.append(poids_int)
    glutonne.append(Poids_Gloutonne(S, v, P))
    
print('\nDynamique : \n')
print(dynamique)
print('\nGlutonne : \n')
print(glutonne)
dif = []
for i in range(len(dynamique)):
    if dynamique[i] != glutonne[i]:
        dif.append(i+1)
print('\nValeurs differentes de M : \n')
print(dif)

tglutonne = []
tdynamique = []
mglutonne = []
mdynamique = []

#%% Différences entre un algorithme Glouton et un Dynamique
S = (1, 3, 4, 7)
P = (10, 27, 32, 55)
for v in range(1,200):
    t0 = time.time()
    tracemalloc.start()
    a = Poids_Gloutonne(S, v, P)
    mem = tracemalloc.get_traced_memory()
    mglutonne.append(mem[1])
    tglutonne.append(time.time()- t0)
    tracemalloc.stop()
    
    t0 = time.time()
    tracemalloc.start()
    b = Monnaie_poids(S, v, P)
    mem = tracemalloc.get_traced_memory()
    mdynamique.append(mem[1])
    tdynamique.append(time.time()- t0)
    tracemalloc.stop()


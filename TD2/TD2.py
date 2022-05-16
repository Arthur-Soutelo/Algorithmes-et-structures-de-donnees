"""
Author: Arthur SOUTELO ARAUJO
"""

def critere(x):
    return(x['filiere']=="PC")

class Pile:
    def __init__(self, var=[]):
        self.__liste = []
        for v in var:
            self.__liste.append(v)
        
    def ajout(self,etudiant):
        self.__liste.append(etudiant) 
        
    def suprime(self):
        return self.__liste.pop()
    
    def taille(self):
        return len(self.__liste)
    
    def renvoie(self, critere = lambda x : True):
        for v in self.__liste:
            if critere(v):
                return(v)
        return False
    
    # def renvoie2(self, critere):
    #     for v in self.__liste:
    #         if critere(v):
    #             return(v)
    #     return False
       
    
class File:
    def __init__(self, var=[]):
        self.__liste = []
        for v in var:
            self.__liste.append(v)
        
    def ajout(self,etudiant):
        self.__liste.append(etudiant) 
        
    def suprime(self):
        return self.__liste.pop(0)
    
    def taille(self):
        return len(self.__liste)
    
    def renvoie(self, critere = lambda x : True):
        for v in self.__liste:
            if critere(v):
                return(v)
        return False
    
    # def renvoie2(self, critere):
    #     for v in self.__liste:
    #         if critere(v):
    #             return(v)
    #     return False

if __name__ == '__main__':
    data = []
    with open("etudiants.txt") as f:
        keys = None
        for line in f:
            l = [w.strip() for w in line.split(';')]
            if keys is None:
                keys = l
            else:
                data.append({k:v for k, v in zip(keys , l)})
    #print(data)

    moys = []
    for i in range(len(data)):
        moys.append(int(data[i]['moyenne']))
    moy = sum(moys)/len(data)
    print(moy)

    # TESTS
    test = File(data)
    # print(test.suprime())
    
    e=test.renvoie(lambda x : x['filiere']=="PC")
    print(e['nom']+ " " + e['prenom'])
    
    # e= File.renvoie2(critere)
    # print(e['nom']+ " " + e['prenom'])
    

    
    
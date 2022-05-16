"""
Author: Arthur SOUTELO ARAUJO
"""

class Labyrinthe:
    def __init__(self, lab):
        self.__l = lab
    
    def affiche_labyrinthe(self):
        print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
            for row in self.__l]))
        
    def voisin(self, x, y):
        res = ()
        for dx, dy in ((1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)):
            if (0 <= x+dx < len (self.__l[0]) and 0 <= y+dy < len(self.__l) and self.__l[y+dy][x+dx] == 0):
                res += ((x+dx, y+dy),)
        return res

    def existe_profondeur(self, x0=0, y0=0, chemin=()):
        if (x0, y0) == (len(self.__l[0])-1 , len(self.__l)-1):
            return True
        chemin += ((x0,y0),)
        
        for x, y in self.voisin(x0, y0):
            if (x,y) in chemin:
                continue
            if self.existe_profondeur(x,y,chemin):
                return True
        return False
    
    def parcours_en_largeur(self):
        todo = [(0,0)]
        for i in range(len(self.__l[0])):
            for j in range(len(self.__l)):
                self.existe_profondeur()
        pass
        
    
    
if __name__ == "__main__":

    labyrinthe = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    lab = Labyrinthe(labyrinthe)
    
    lab.affiche_labyrinthe()
    
    print(lab.voisin(0, 1))
    
    lab.existe_profondeur()
    
    
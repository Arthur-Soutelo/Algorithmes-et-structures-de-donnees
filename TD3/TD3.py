"""
Authors: Arthur SOUTELO ARAUJO
         Valentin CHAZALON
"""

from PIL import Image  # importation de la librairie d'image PILLOW
from math import sqrt, log10 # fonctions essentielles de la librairie math

import time
import tracemalloc

class Noeud:
    def __init__(self, x, y, l, h, r, v, b, hg, hd, bg, bd):
        self.x = x
        self.y = y
        self.l = l
        self.h = h
        self.r = r
        self.v = v
        self.b = b
        self.hg = hg # haut-gauche
        self.hd = hd # haut-droite
        self.bg = bg # bas-gauche
        self.bd = bd # bas-droite
        
    def __repr__(self, prefix=""):
        return "\n".join((f"{prefix}({self.x},{self.y},{self.l},{self.h}) couleur ({self.r},{self.v},{self.b}) enfants :",
			self.hg.__repr__(prefix+"  ") if self.hg!=None else prefix+"  None",
			self.hd.__repr__(prefix+"  ") if self.hd!=None else prefix+"  None",
			self.bg.__repr__(prefix+"  ") if self.bg!=None else prefix+"  None",
			self.bd.__repr__(prefix+"  ") if self.bd!=None else prefix+"  None"))


class CompressionImage:
    def __init__(self, fichier):
        self.__im = Image.open(fichier) # ouverture du fichier d’image
        self.__px = self.__im.load() # importation des pixels de l’image
        
        self.liste = []
    
    def save(self, nom):
        self.__im.save(nom)
        
    def get_dim(self):
        return self.__im.size
    
    def get_w(self):
        return self.get_dim()[0]
    
    def get_h(self):
        return self.get_dim()[1]
    
    def get_pixel(self, x, y):
        return self.__px[x,y]

    def afficher(self):
        self.__im.show()
        
    def __del__(self):
        self.__im.close()
    
    def peindre(self,x,y,l,h,r,g,b):
        for i in range(l):
            for j in range(h):              
                self.__px[x+i, y+j] = r, g, b
    
    def moyenne(self,x,y,l,h):
        sumrgb=[0,0,0]
        for i in range(l):
            for j in range(h):        
                r,g,b = self.__px[x+i, y+j]
                sumrgb[0] = sumrgb[0] + r
                sumrgb[1] = sumrgb[1] + g
                sumrgb[2] = sumrgb[2] + b
        n = l * h
        return sumrgb[0]/n, sumrgb[1]/n, sumrgb[2]/n
    
    def ecart_type(self,x,y,l,h):
        sumrgb=[0,0,0]
        sqrgb=[0,0,0]
        for i in range(l):
            for j in range(h):        
                r,g,b = self.__px[x+i, y+j]
                
                sumrgb[0] = sumrgb[0] + r
                sumrgb[1] = sumrgb[1] + g
                sumrgb[2] = sumrgb[2] + b
                
                sqrgb[0] = sqrgb[0] + r*r
                sqrgb[1] = sqrgb[1] + g*g
                sqrgb[2] = sqrgb[2] + b*b
        n = l*h
        return sqrt(sqrgb[0]/n - (sumrgb[0]/n)**2), sqrt(sqrgb[1]/n - (sumrgb[1]/n)**2), sqrt(sqrgb[2]/n - (sumrgb[2]/n)**2)
        
    def est_homogene(self,x,y,l,h,seuil):
        return (sum(self.ecart_type(x,y,l,h))/3 <= seuil)
    
    def partition(self, x, y, w, h):
        assert w>0 and h>0 and not w==h==1
        i = (w+1)//2
        j = (h+1)//2
        hg = (x, y, i, j)
        hd = (x+i, y, w-i, j) if w>1 else None
        bg = (x, y+j, i, h-j) if h>1 else None
        bd = (x+i, y+j, w-i, h-j) if w>1 and h>1 else None
        return (hg, hd, bg, bd)
        
    def arbre(self,x,y,l,h,seuil):     # Exercice 2.2
        r,g,b = self.moyenne(x,y,l,h)
        if self.est_homogene(x, y, l, h, seuil):
            return Noeud(x, y, l, h, r, g, b, None, None, None, None)
        else:
            hg,hd,bg,bd = self.partition(x, y, l, h)
            return Noeud(x, y,  l, h, r, g, b,
                         self.arbre(hg[0], hg[1], hg[2], hg[3], seuil) if hg != None else None,
                         self.arbre(hd[0], hd[1], hd[2], hd[3], seuil) if hd != None else None,
                         self.arbre(bg[0], bg[1], bg[2], bg[3], seuil) if bg != None else None,
                         self.arbre(bd[0], bd[1], bd[2], bd[3], seuil) if bd != None else None)
                    
    def compter(self,n):     # Exercice 2.3
        if n == None:
            return 0
        return 1 + self.compter(n.hg) + self.compter(n.hd) + self.compter(n.bg) + self.compter(n.bd)
        
    def peindre_arbre(self, n):     # Exercice 2.4
        if n == None:
            return
        if n.hg==n.hd==n.bg==n.bd==None:
            self.peindre(n.x, n.y, n.l, n.h, round(n.r), 
                         round(n.v), round(n.b))
        else:
            self.peindre_arbre(n.hg)
            self.peindre_arbre(n.hd)
            self.peindre_arbre(n.bg)
            self.peindre_arbre(n.bd)

    def profondeur(self, n):
        if n == None:
            return 0
        return 1 + max(self.profondeur(n.hg), self.profondeur(n.hd), self.profondeur(n.bg), self.profondeur(n.bd))
            
    def peindre_profondeur(self, n):     # Exercice 2.5
        profondeur = self.profondeur(n)
        def rec(n, p):
            if n == None:
                return
            if n.hg==n.hd==n.bg==n.bd==None:
                rvb=255*p//(profondeur-1)
                self.peindre(n.x, n.y, n.l, n.h, rvb, rvb, rvb)
            else:
                rec(n.hg, p+1); rec(n.hd, p+1); rec(n.bg, p+1); rec(n.bd, p+1)
        rec(n, 0)
    
    
    def EQ(self, n):      # Erreur Quadratique
        if n == None:
            return 0
        if n.hg==n.hd==n.bg==n.bd==None:
            eq = 0
            for i in range(n.x, n.x+n.l):
                for j in range(n.y, n.y+n.h):
                    r, g, b = self.__px[i, j]
                    eq += (r-n.r)**2 + (g-n.v)**2 + (b-n.b)**2
            return eq
        else:
            return self.EQ(n.hg) + self.EQ(n.hd) + self.EQ(n.bg) 
        + self.EQ(n.bd)
    
    def PSNR(self, n):     # Exercice 2.6
        return 20 * log10(255) - 10 * log10(self.EQ(n) / 3 / n.l / n.h)
    
    
    def compression(self, seuil, nom):
        arbre = self.arbre(0, 0, self.get_w(), self.get_h(), seuil)
        self.peindre_arbre(arbre)
        self.__im.save(nom)
        print('PSNR : ' + str(self.PSNR(arbre)))
        
        
    """ Partie 3 """
    
    #Formules permettant de calculer l'indice de l'enfant : haut gauche : 4*i+1 ; haut droit : 4*i+2
    #                                                       bas gauche  : 4*i+3 ; bas droit  : 4*i+4
    #Formules permettant de calculer l'indice du parent : E((i-1)/4)
    
    def arbre_implicite(self,x,y,l,h,seuil,index=0):     # Exercice 3.2
        r,g,b = self.moyenne(x,y,l,h)
        
        if len(self.liste) == 0:
            self.liste.append(NoeudImplicite(x, y, l, h, r, g, b))
        else:
            self.liste[index] = NoeudImplicite(x, y, l, h, r, g, b)
        
        if not self.est_homogene(x, y, l, h, seuil):
            hg,hd,bg,bd = self.partition(x, y, l, h)                        
            
            if len(self.liste) <= (index + 1)*4:      # Si la longueur de la liste n'est pas suffisante
                for i in range((index + 1)*4 - len(self.liste) + 1):
                    self.liste.append(None)           # On rajoute l'emplacement pour les fils
            
            if hg != None:
                self.arbre_implicite(*hg, seuil, 4*index+1)
            if hd != None:
                self.arbre_implicite(*hd, seuil, 4*index+2)
            if bg != None:
                self.arbre_implicite(*bg, seuil, 4*index+3)
            if bd != None:
                self.arbre_implicite(*bd, seuil, 4*index+4)
        else:
            return
        
    def peindre_arbre_implicite(self,index=0):     # Exercice 3.4
        if 4*index+4 > len(self.liste):
            return
        
        n = self.liste[index]
        if n == None:
            return
        if self.liste[4*index+1]==self.liste[4*index+2]==self.liste[4*index+3]==self.liste[4*index+4]==None:
            self.peindre(n.x, n.y, n.l, n.h, round(n.r), round(n.v), round(n.b))
        else:
            self.peindre_arbre_implicite(4*index+1)
            self.peindre_arbre_implicite(4*index+2)
            self.peindre_arbre_implicite(4*index+3)
            self.peindre_arbre_implicite(4*index+4)
    
    def compression_implicite(self, seuil, nom):
        self.arbre_implicite(0, 0, self.get_w(), self.get_h(), seuil)
        self.peindre_arbre_implicite()
        self.__im.save(nom)
        
    
    def est_homogene_optimisée(self,x,y,l,h,seuil):
        if self.get_w()/5 < x+l/2 < self.get_w()*4/5 and self.get_h()/5 < y+h/2 < self.get_h()*4/2:
            if self.get_w()*2/5 < x+l/2 < self.get_w()*3/2 and self.get_h()*2/5 < y+h/2 < self.get_h()*3/2:
                seuil = seuil * 0.5          # Région centrale
            else:
                seuil = seuil * 0.75         # Région intermediaire
        else:
            seuil = seuil * 1.               # Région périperique
            
        for ecart in self.ecart_type(x,y,l,h):
            if ecart >= 2 * seuil:          # Contraste
                return False
        
        return (sum(self.ecart_type(x,y,l,h))/3 <= seuil)
    
    def compression_optimisée(self, seuil, nom):     # Exercice 3.4
        arbre = self.arbre_optimisée(0, 0, self.get_w(), self.get_h(), seuil)
        self.peindre_arbre(arbre)
        self.__im.save(nom)
        print('PSNR : ' + str(self.PSNR(arbre)))
    
    def arbre_optimisée(self,x,y,l,h,seuil):     # Exercice 3.4
        r,g,b = self.moyenne(x,y,l,h)
        if self.est_homogene_optimisée(x, y, l, h, seuil):
            return Noeud(x, y, l, h, r, g, b, None, None, None, None)
        else:
            hg,hd,bg,bd = self.partition(x, y, l, h)
            return Noeud(x, y,  l, h, r, g, b,
                         self.arbre_optimisée(hg[0], hg[1], hg[2], hg[3], seuil) if hg != None else None,
                         self.arbre_optimisée(hd[0], hd[1], hd[2], hd[3], seuil) if hd != None else None,
                         self.arbre_optimisée(bg[0], bg[1], bg[2], bg[3], seuil) if bg != None else None,
                         self.arbre_optimisée(bd[0], bd[1], bd[2], bd[3], seuil) if bd != None else None)
    
    def filtre_gaussien(self):                             # Exercice 3.6
        # H = [[0.05, 0.15, 0.05], 
        #      [0.15, 0.2 , 0.15], 
        #      [0.05, 0.15, 0.05]]
        
        for i in range(self.get_w()-2):
            for j in range(self.get_h()-2):
                self.__px[i+1,j+1] = (round(0.2 * self.__px[i+1,j+1][0] + 0.05 * (self.__px[i,j][0] + self.__px[i+2,j+2][0] + self.__px[i,j+2][0] + self.__px[i+2,j][0]) + 0.15 * (self.__px[i+2,j+1][0] + self.__px[i,j+1][0] + self.__px[i+1,j][0] + self.__px[i+1,j+2][0])), 
                round(0.2 * self.__px[i+1,j+1][1] + 0.05 * (self.__px[i,j][1] + self.__px[i+2,j+2][1] + self.__px[i,j+2][1] + self.__px[i+2,j][1]) + 0.15 * (self.__px[i+2,j+1][1] + self.__px[i,j+1][1] + self.__px[i+1,j][1] + self.__px[i+1,j+2][1])), 
                round(0.2 * self.__px[i+1,j+1][2] + 0.05 * (self.__px[i,j][2] + self.__px[i+2,j+2][2] + self.__px[i,j+2][2] + self.__px[i+2,j][2]) + 0.15 * (self.__px[i+2,j+1][2] + self.__px[i,j+1][2] + self.__px[i+1,j][2] + self.__px[i+1,j+2][2])))
        
        # Bornes
                if j == 0:
                    self.__px[i+1,j] = (round(0.2 * self.__px[i+1,j][0] + 0.05 * (self.__px[i+2,j+1][0] + self.__px[i,j+1][0]) + 0.15 * (self.__px[i+2,j][0] + self.__px[i,j][0] + self.__px[i+1,j+1][0])),
                                        round(0.2 * self.__px[i+1,j][1] + 0.05 * (self.__px[i+2,j+1][1] + self.__px[i,j+1][1]) + 0.15 * (self.__px[i+2,j][1] + self.__px[i,j][1] + self.__px[i+1,j+1][1])),
                                        round(0.2 * self.__px[i+1,j][2] + 0.05 * (self.__px[i+2,j+1][2] + self.__px[i,j+1][2]) + 0.15 * (self.__px[i+2,j][2] + self.__px[i,j][2] + self.__px[i+1,j+1][2])))

            if i == 0:
                self.__px[i,j+1] = (round(0.2 * self.__px[i,j+1][0] + 0.05 * (self.__px[i+1,j+2][0] + self.__px[i+1,j][0]) + 0.15 * (self.__px[i+1,j+1][0] + self.__px[i,j][0] + self.__px[i,j+2][0])),
                                    round(0.2 * self.__px[i,j+1][1] + 0.05 * (self.__px[i+1,j+2][1] + self.__px[i+1,j][1]) + 0.15 * (self.__px[i+1,j+1][1] + self.__px[i,j][1] + self.__px[i,j+2][1])),
                                    round(0.2 * self.__px[i,j+1][2] + 0.05 * (self.__px[i+1,j+2][2] + self.__px[i+1,j][2]) + 0.15 * (self.__px[i+1,j+1][2] + self.__px[i,j][2] + self.__px[i,j+2][2])))
        
        i = self.get_w()-2    # i = W
        for j in range(self.get_h()-2):
            self.__px[i,j+1] = (round(0.2 * self.__px[i,j+1][0] + 0.05 * (self.__px[i-1,j][0] + self.__px[i-1,j+2][0]) + 0.15 * (self.__px[i-1,j+1][0] + self.__px[i,j][0] + self.__px[i,j+2][0])),
                                round(0.2 * self.__px[i,j+1][1] + 0.05 * (self.__px[i-1,j][1] + self.__px[i-1,j+2][1]) + 0.15 * (self.__px[i-1,j+1][1] + self.__px[i,j][1] + self.__px[i,j+2][1])),
                                round(0.2 * self.__px[i,j+1][2] + 0.05 * (self.__px[i-1,j][2] + self.__px[i-1,j+2][2]) + 0.15 * (self.__px[i-1,j+1][2] + self.__px[i,j][2] + self.__px[i,j+2][2])))
        
        j = self.get_h()-2     # j = H
        for i in range(self.get_w()-2):
            self.__px[i+1,j+1] = (round(0.2 * self.__px[i+1,j+1][0] + 0.05 * (self.__px[i,j][0] + self.__px[i+2,j][0]) + 0.15 * (self.__px[i+2,j+1][0] + self.__px[i,j+1][0] + self.__px[i+1,j][0])),
                                  round(0.2 * self.__px[i+1,j+1][1] + 0.05 * (self.__px[i,j][1] + self.__px[i+2,j][1]) + 0.15 * (self.__px[i+2,j+1][1] + self.__px[i,j+1][1] + self.__px[i+1,j][1])),
                                  round(0.2 * self.__px[i+1,j+1][2] + 0.05 * (self.__px[i,j][2] + self.__px[i+2,j][2]) + 0.15 * (self.__px[i+2,j+1][2] + self.__px[i,j+1][2] + self.__px[i+1,j][2])))       
                    

class NoeudImplicite:                            # Exercice 3.2
    def __init__(self, x, y, l, h, r, v, b):
        self.x = x
        self.y = y
        self.l = l
        self.h = h
        self.r = r
        self.v = v
        self.b = b
    
    

if __name__ == "__main__":
    seuil = 5
    
    nom = "the-mandalorian"   
    ce = CompressionImage(nom+'.jpg')
    ci = CompressionImage(nom+'.jpg')
    
    # nom = "Centrale"   
    # ce = CompressionImage(nom+'.jpeg')
    # ci = CompressionImage(nom+'.jpeg')
    
    # ---------------------------------------------------
    """ Filtre Gaussien """
    
    #ce.compression(seuil, nom+str(seuil)+'.jpg')
    #ce.afficher()
    #ce.filtre_gaussien()
    #ce.afficher()
    #ce.save(nom+str(seuil)+'_filtre'+'.jpg')
    
    # ci.compression_optimisée(seuil, nom+str(seuil)+'_optimisée'+'.jpg')
    # ci.afficher()
    # ci.filtre_gaussien()
    # ci.afficher()
    
    ce.filtre_gaussien()
    ce.afficher()
    ce.save(nom+'Original'+'_filtre'+'.jpg')
    
    # ---------------------------------------------------
    """ Graph memoire et temps """
    
    # seuil = [90, 80, 70, 60, 50, 40, 30, 20]
    # temps_explicite = []
    # temps_implicite = []
    # memoire_explicite = []
    # memoire_implicite = []
    
    # for s in seuil:
    #     ce = CompressionImage(nom+'.jpg')
    #     t0 = time.time()
    #     tracemalloc.start()
    #     ce.compression(s, nom+str(s)+'.jpg')
    #     ce.afficher()
    #     memoire_explicite.append(tracemalloc.get_traced_memory())
    #     temps_explicite.append(time.time()- t0)
    #     tracemalloc.stop()
        
    #     ci = CompressionImage(nom+'.jpg')
    #     t0 = time.time()
    #     tracemalloc.start()
    #     ci.compression_implicite(s, nom+'_implicite'+str(s)+'.jpg')
    #     ci.afficher()
    #     memoire_implicite.append(tracemalloc.get_traced_memory())
    #     temps_implicite.append(time.time()- t0)
    #     tracemalloc.stop()
    
    # ---------------------------------------------------
    """ Graph Homogeneité """
    
    # seuil = [60, 50, 40, 30, 20]
    # temps_normal = []
    # temps_optimisée = []
    # memoire_normal = []
    # memoire_optimisée = []
    
    # for s in seuil:
    #     ce = CompressionImage(nom+'.jpg')
    #     t0 = time.time()
    #     tracemalloc.start()
    #     ce.compression(s, nom+str(s)+'.jpg')
    #     ce.afficher()
    #     memoire_normal.append(tracemalloc.get_traced_memory())
    #     temps_normal.append(time.time()- t0)
    #     tracemalloc.stop()
        
    #     ci = CompressionImage(nom+'.jpg')
    #     t0 = time.time()
    #     tracemalloc.start()
    #     ci.compression_optimisée(s, nom+'_implicite'+str(s)+'.jpg')
    #     ci.afficher()
    #     memoire_optimisée.append(tracemalloc.get_traced_memory())
    #     temps_optimisée.append(time.time()- t0)
    #     tracemalloc.stop()    
    
    # ---------------------------------------------------    
    
    # W = ci.get_w()
    # H = ci.get_h()
    
    # racine = Noeud(0, 0, 4, 4, 128, 128, 128,
    #     Noeud(0, 0, 2, 2, 255, 255, 255, None, None, None, None),
    #     Noeud(2, 0, 2, 2, 128, 128, 128, 
    #           Noeud(2, 0, 1, 1, 128, 128, 128, None, None, None, None),
    #           Noeud(3, 0, 1, 1, 128, 128, 128, None, None, None, None),
    #           Noeud(2, 1, 1, 1, 0, 0, 0, None, None, None, None),
    #           Noeud(3, 1, 1, 1, 0, 0, 0, None, None, None, None)),
    #     Noeud(2, 2, 2, 2, 128, 128, 128, 
    #           Noeud(2, 2, 1, 1, 128, 128, 128, None, None, None, None),
    #           Noeud(3, 2, 1, 1, 128, 128, 128, None, None, None, None),
    #           Noeud(2, 3, 1, 1, 255, 255, 255, None, None, None, None),
    #           Noeud(3, 3, 1, 1, 255, 255, 255, None, None, None, None)),
    #     Noeud(0, 2, 2, 2, 0, 0, 0, None, None, None, None))
    
    # ---------------------------------------------------
    
    # l=W//4
    # h=H//4
    
    # ---------------------------------------------------
    
    # print(compter(racine))
    # peindre(0,0,l,h,255,0,0)
    # print(moyenne(0,0,W,H))
    # print(ecart_type(0, 0,W, H))
    # print(ecart_type(0, 0,10, 10))
    # peindre(0,0,l,h,255,0,0)
    # im.show()
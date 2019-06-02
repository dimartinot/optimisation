# Une particule définie par un dictionnaire ayant les clés/valeurs :
#  - vit : Vk (init 0,..., 0) avec dim valeurs (ex: une particule dans un espace en 3D, possède 3 valeurs)
#  - pos : Xk (aleatoire dans [inf,sup]^dim)
#  - fit : f(Xk) (fonction f)
#  - bestpos : Xpbest 
#  - bestfit : f(Xpbest) (à zero)
#  - bestVoisin : Xvbest (init à 0 puis on fait un deuxieme tour pour mettre à jour)
#
# L'essaim est donc généré en tant qu'une liste de dictionnaires

import numpy as np
import random

#constantes
num_iteration = 5000
dim = 3
inf = -5
sup = 10
nbParticules = 20
psi = 0.7
cmax = 1.47
#variables globales

def f(x,size):
    res = 0
    for i in range(size-1):
        res += 100*pow((x[i+1]-pow(x[i],2)),2)+pow((x[i]-1),2)
    return res

def difList(l1,l2,size):
    for i in range(size):
        if (l1[i] != l2[i]):
            return True
    return False

def initParticule():

    Xk = []
    for i in range(dim):
        Xk.append(random.uniform(inf,sup))

    Vit = []
    for i in range(dim):
        Vit.append(0)

    p = {
        "vit" : Vit,
        "pos" : Xk,
        "fit" : f(Xk,dim),
        "bestpos" : Xk,
        "bestfit" : f(Xk,dim),
        "bestVoisin" : Vit
    }

    return p

# À partir d'une liste de particules et d'une particule, renvoie tous ses voisins
def voisinage(x,list_of_particules):
    return list_of_particules

# À partir d'une liste de particules et d'une particule, revoie le meilleur voisin de celle ci
def bestVois(x,list_of_particules):
    best_val = voisinage(x,list_of_particules)[0]
    for part in voisinage(x,list_of_particules):
        if (part["fit"] < best_val["fit"] and difList(x["pos"],part["pos"],dim)):
            best_val = part
    return best_val

# Substraction de deux particules
def subPart(x1,x2,size):
    res = []
    for i in range(size):
        res.append(x1[i]-x2[i])
    return res

def vectSumn(vect1,vect2,size):
    res=[]
    for i in range(size):
        res.append(vect1[i]+vect2[i])
    return res

def multScalWithVect(scal,vec,dim):
    for i in range(dim):
        vec[i] = scal*vec[i]
    return vec   

def main():
    list_of_particules = []

    #premier tour d'initialisation des particules
    for i in range(nbParticules):
        p = initParticule()
        list_of_particules.append(p)

    #deuxième tour de mise-à-jour des Xvbest
    for i in range(nbParticules):
        # pour chaque particule, on récupère le meilleur voisin
        list_of_particules[i]["bestVoisin"] = bestVois(list_of_particules[i],list_of_particules)["pos"]
    
    for i in range(num_iteration):
        list_of_particules_renewed = list_of_particules

        # Calcul des nouvelles positions
        for particule_index in range(len(list_of_particules_renewed)):
            # calcul de la vitesse
            for n in range(dim):
                list_of_particules_renewed[particule_index]["vit"][n] = psi*list_of_particules[particule_index]["vit"][n]
            list_of_particules_renewed[particule_index]["vit"] = vectSumn(list_of_particules_renewed[particule_index]["vit"],multScalWithVect(cmax*random.uniform(0,1),(subPart(list_of_particules[particule_index]["bestpos"],list_of_particules[particule_index]["pos"],dim)),dim),dim)
            list_of_particules_renewed[particule_index]["vit"] = vectSumn(list_of_particules_renewed[particule_index]["vit"],multScalWithVect(cmax*random.uniform(0,1),(subPart(list_of_particules[particule_index]["bestVoisin"],list_of_particules[particule_index]["pos"],dim)),dim),dim)
            # repositionnement de la particule
            list_of_particules_renewed[particule_index]["pos"] = vectSumn(list_of_particules_renewed[particule_index]["vit"],list_of_particules_renewed[particule_index]["pos"],dim)
            # évaluation de la fonction f pour le fit
            list_of_particules_renewed[particule_index]["fit"] = f(list_of_particules_renewed[particule_index]["pos"], dim)

        bestPos = list_of_particules_renewed[0]["bestpos"]

        # Calcul du bestVoisin de chaque particule
        for particule_index in range(len(list_of_particules_renewed)):
            # Calcul de la position
            best_vois = bestVois(list_of_particules_renewed[particule_index],list_of_particules_renewed)["pos"]
            list_of_particules_renewed[particule_index]["bestVoisin"] = best_vois
            # Si le meilleur voisin calculé est plus optimale que l'ancien bestPos, on met-à-jour ce dernier
            if (f(bestPos,dim) > f(best_vois,dim)):
               bestPos = best_vois
        
        # Affectation du meilleur élément et de son évaluation de la fonction à toutes les particules
        for particule_index in range(len(list_of_particules_renewed)):
            list_of_particules_renewed[particule_index]["bestpos"] = bestPos
            list_of_particules_renewed[particule_index]["bestfit"] = f(bestPos,dim)

        list_of_particules = list_of_particules_renewed
    print(list_of_particules)
main()
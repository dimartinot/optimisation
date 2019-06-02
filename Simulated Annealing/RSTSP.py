# -*- coding: Latin-1 -*-
# programme de resolution du probleme du voyaguer de commerce
# par l'algorithme du recuit simule
# Dominique Lefebvre pour TangenteX.com
# Peio Loubiere pour l'EISTI
# septembre 2017
# usage : python RSTSP.py NOMFICHIER
from scipy import *
from math import *
from matplotlib.pyplot import *
import sys
import random as rdm

# Instance du problème
#FIC="NUMERO.tsp"
if (len(sys.argv) > 1):
    FIC=sys.argv[1]
else:
    print("Aucun fichier spécifié...")
    sys.exit("USAGE : python RSTSP.py NUMERO_INSTANCE.tsp")

# ###################################### Parametres du recuit ##################################
#T0 = 1e6  # temperature initiale
T0 = 150  # temperature initiale
Tmin = 1e-3 # temperature finale
tau = 1e4 # constante pour la décroissance de temperature
Alpha = 0.9 # constante pour la décroissance géométrique
Palier = 7 # nombre d'itérations sur un palier de température
IterMax = 15000 # nombre max d'itérations de l'algorithme
# ##############################################################################################

# Creation de la figure
TPSPause = 1e-10 # pour affichage
fig1 = figure()
canv = fig1.add_subplot(1,1,1)
xticks([])
yticks([])

# Parsing du fichier de données
# pre-condition : nomfic : nom de fichier (doit exister)
# post-condition : (x,y) coordonnees des villes
def parse(nomfic):
    absc=[]
    ordo=[]
    with open(nomfic,'r') as inf:
        for line in inf:
            absc.append(float(line.split(' ')[1]))
            ordo.append(float(line.split(' ')[2]))
    return (array(absc),array(ordo))


# Affiche les coordonnées des points du chemin ainsi que le meilleur trajet trouvé et sa longueur
# pre-conditions :
#   - best_trajet, best_dist : meilleur trajet trouvé et sa longueur,
def affRes(best_trajet, best_dist):
    print("trajet = {}".format(best_trajet))
    print("distance = {}".format(best_dist))

# Rafraichit la figure du trajet, on trace le meilleur trajet trouvé
# pre-conditions :
#   - best_trajet, best_dist : meilleur trajet trouvé et sa longueur,
#   - x, y : tableaux de coordonnées des points du chemin
def dessine(best_trajet, best_dist, x, y):
    global canv,lx,ly
    canv.clear()
    canv.plot(x[best_trajet],y[best_trajet],'k')
    canv.plot([x[best_trajet[-1]], x[best_trajet[0]]],[y[best_trajet[-1]], \
      y[best_trajet[0]]],'k')
    canv.plot(x,y,'ro')
    title("Distance : {}".format(best_dist))
    pause(TPSPause)

# Affiche la figure des graphes de :
#   - l'ensemble des energies des fluctuations retenues
#   - la meilleure energie
#   - la decroissance de temperature
def dessineStats(Htemps, Henergie, Hbest, HT):
    # affichage des courbes d'evolution
    fig2 = figure(2)
    subplot(1,3,1)
    semilogy(Htemps, Henergie)
    title("Evolution de l'energie totale du systeme")
    xlabel('Temps')
    ylabel('Energie')
    subplot(1,3,2)
    semilogy(Htemps, Hbest)
    title('Evolution de la meilleure distance')
    xlabel('Temps')
    ylabel('Distance')
    subplot(1,3,3)
    semilogy(Htemps, HT)
    title('Evolution de la temperature du systeme')
    xlabel('Temps')
    ylabel('Temperature')
    show()

# Factorisation des fonctions de calcul de la distance totale
# pre-condition : (x1,y1),(x2,y2) coordonnees des villes
# post-condition : distance euclidienne entre 2 villes
def distance(p1,p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# Fonction de calcul de l'energie du systeme,
# pre-condition : 
#   - coords : coordonnées des points du chemin
#   - chemin : ordre de parcours des villes
# post-condition : Pb du VC : la distance totale du trajet
def energieTotale(coords,chemin):
    energie = 0.0
    coord = coords[chemin]
#    print(coord)
    for i in range(-1,N-1): # on calcule la distance en fermant la boucle
        energie += distance(coord[i], coord[i+1])
    return energie

# fonction de fluctuation autour de l'etat "thermique" du systeme : echange de 2 points
# pre-condition :
#   - chemin : ordre de parcours des villes
#   - i,j indices des villes à permuter
# post-condition : nouvel ordre de parcours
def fluctuationDeux(chemin,i,j):
    nv = chemin[:]
    temp = nv[i]
    nv[i] = nv[j]
    nv[j] = temp
    return nv

# fonction d'implementation de l'algorithme de Metropolis pour un trajet par rapport a son voisin
# pre-conditions :
#   - ch1 voisin, ch2 : trajet init,
#   - disti : distance de chaque trajet
#   - T : température actuelle du système
# post-condition : retourne la fluctuation retenue par le critère de Metropolis
def metropolis(ch1,dist1,ch2,dist2,T):
    global best_trajet, best_dist, x, y,cptx,cpty,cptz
    delta = dist1 - dist2 # calcul du differentiel
    if delta <= 0: # si ameliore,
        if dist1 <= best_dist: # comparaison au best, si meilleur, enregistrement et refresh de la figure
            best_dist = dist1
            best_trajet = ch1[:]
            dessine(best_trajet, best_dist, x, y)
        cptx = cptx+1
        return (ch1, dist1) # la fluctuation est retenue, retourne le voisin
    else:
        if random.uniform() > exp(-delta/T): # la fluctuation n'est pas retenue selon la proba
            cpty = cpty+1
            return (ch2, dist2)              # trajet initial
        else:
            cptz = cptz+1
            return (ch1, dist1)              # la fluctuation est retenue, retourne le voisin

# initialisation des listes d'historique pour le graphique final
Henergie = []     # energie
Htemps = []       # temps
HT = []           # temperature
Hbest = []        # distance

# ##################################### INITIALISATION DE L'ALGORITHME ############################
# Construction des données depuis le fichier
(x,y) = parse(FIC) # x,y sont gardés en l'état pour l'affichage graphique
coords = array(list(zip(x,y)), dtype=float) # On contruit le tableau de coordonées (x,y)

# Paramètre du probleme
N = len(coords)    # nombre de villes

# definition du trajet initial : ordre croissant des villes
trajet = [i for i in range(N)]
# calcul de l'energie initiale du systeme (la distance initiale a minimiser)
dist = energieTotale(coords,trajet)
# initialisation du meilleur trajet
best_trajet = trajet[:]
best_dist = dist

# on trace le chemin de depart
dessine(best_trajet, best_dist, x, y)

# boucle principale de l'algorithme du recuit
t = 0
T = T0
iterPalier = Palier
cptx = 0
cpty = 0
cptz = 0

# ##################################### BOUCLE PRINCIPALE DE L'ALGORITHME ############################

# Boucle de convergence sur critère de nb d'itération (pour tester les paramètres)
#for i in range(IterMax):
# Boucle de convergence sur critère de température
n = 0
while T > Tmin:
    while iterPalier > 0:
        i = rdm.randint(0,N-1)
        j = rdm.randint(0,N-1)
        while j == i:
            j = rdm.randint(0,N-1)
        best_trajet_vois = fluctuationDeux(best_trajet,i,j)
        dist_vois = energieTotale(coords,best_trajet_vois)
        (best_trajet, dist) = metropolis(best_trajet_vois,dist_vois,best_trajet,dist,T)
        Henergie.append(dist)
        HT.append(T)
        n += 1
        Htemps.append(n)
        Hbest.append(best_dist)
        iterPalier -= 1
    T = Alpha*T
    iterPalier = Palier
# ##################################### FIN DE L'ALGORITHME - AFF DES RÉsSULTATS ############################

# affichage console du résultat
print("X = ",cptx,"Y = ",cpty,"Z = ",cptz)
print("Améliorations  = ",cptx/(cptx+cpty+cptz))
affRes(best_trajet, best_dist)
# graphique des stats
dessineStats(Htemps, Henergie, Hbest, HT)

import enumerate
from igraph import *

#Affichage des patterns

permutation = [
    3,6,8,11,14,18,20,24,28,31,34,39,43,47,49,52,54,57,60,62,65,67,70,72,
    10,17,23,27,30,33,38,42,46,51,56,59,64,69,
    1,4,12,15,22,26,35,37,41,45,73,
    2,5,7,9,13,16,19,21,25,29,32,36,40,44,48,50,53,55,58,61,63,66,68,71
]

pos_to_pattern = [
    1,
    2, 2,
    3,
    4, 4,
    5, 5,
    6, 6, 6,
    7,
    8, 8,
    9,
    10, 10, 10,
    11, 11,
    12, 12, 12, 12,
    13, 13, 13, 13,
    14, 14, 14,
    15, 15, 15,
    16,
    17, 17, 17, 17,
    18, 18, 18, 18,
    19, 19, 19, 19,
    20, 20, 
    21, 21, 21, 
    22, 22,
    23, 23, 23,
    24, 24, 24,
    25, 25,
    26, 26, 26,
    27, 27,
    28, 28, 28,
    29, 29,
    30
]

def max_couleur(rouge,vert,bleu,noir):
    if rouge > vert and rouge > bleu and rouge > noir :
        return "red"
    elif vert > bleu and vert > noir:
        return "green"
    elif bleu > noir:
        return "blue"
    else:
        return "white"
               
couple = enumerate.main()
fichier = open("resultats_motifs.csv","w")
graph = enumerate.create_graph(sys.argv[1])
couleur_chaque_noeud = []
bet = graph.betweenness()

fichier.write("motif;;")

i = 0
while i<30:
    fichier.write(str(i+1) + ";")
    i += 1
    
fichier.write("\n")  
fichier.write("nombre d'apparitions;;")
    
i = 0
while i<30:
    fichier.write(str(couple[0][i]) + ";")
    i += 1
    
fichier.write("\n") 
fichier.write("\n") 
fichier.write("\n") 
fichier.write("\n") 

fichier.write("position;;") 

i = 0
while i<24:
    fichier.write(str(permutation[i]) + ";")
    i += 1
fichier.write(";;")
while i<38:
    fichier.write(str(permutation[i]) + ";")
    i += 1
fichier.write(";;")
while i<49:
    fichier.write(str(permutation[i]) + ";")
    i += 1
fichier.write(";;")
while i<73:
    fichier.write(str(permutation[i]) + ";")
    i += 1


fichier.write(";;;nombre rouge; nombre vert; nombre bleu; nombre noir;;betweenness;;identifiant alter")
fichier.write("\n")

fichier.write("motif correspondant;;") 

i = 0

while i<24:
    fichier.write(str(pos_to_pattern[permutation[i]-1]) + ";")
    i += 1
fichier.write(";;")
while i<38:
    fichier.write(str(pos_to_pattern[permutation[i]-1]) + ";")
    i += 1
fichier.write(";;")
while i<49:
    fichier.write(str(pos_to_pattern[permutation[i]-1]) + ";")
    i += 1
fichier.write(";;")
while i<73:
    fichier.write(str(pos_to_pattern[permutation[i]-1]) + ";")
    i += 1
    
fichier.write("\n")
fichier.write("\n")

noeud = 0
while noeud < len(couple[1]):
    fichier.write(str(noeud) + ";;")
    somme_rouge = 0
    somme_vert = 0
    somme_bleu = 0
    somme_noir = 0
    i = 0
    while i<24:
        somme_rouge += couple[1][noeud][permutation[i]-1]
        fichier.write(str(couple[1][noeud][permutation[i]-1]) + ";")
        i += 1
    fichier.write(";;")
    while i<38:
        somme_vert += couple[1][noeud][permutation[i]-1]
        fichier.write(str(couple[1][noeud][permutation[i]-1]) + ";")
        i += 1
    fichier.write(";;")
    while i<49:
        somme_bleu += couple[1][noeud][permutation[i]-1]
        fichier.write(str(couple[1][noeud][permutation[i]-1]) + ";")
        i += 1
    fichier.write(";;")
    while i<73:
        somme_noir += couple[1][noeud][permutation[i]-1]
        fichier.write(str(couple[1][noeud][permutation[i]-1]) + ";")
        i += 1
        
    fichier.write(";;")    
    fichier.write(";"+str(somme_rouge) +";"+ str(somme_vert) + ";" + str(somme_bleu) + ";" + str(somme_noir) + ";;" + str(round(bet[noeud],2)) + ";;" + str(graph.vs[noeud]["name"]))
    
    couleur_chaque_noeud.append(max_couleur(somme_rouge,somme_vert,somme_bleu,somme_noir))
    noeud += 1
    fichier.write("\n")
        
permutation.sort()

i = 0
while i < len(graph.vs):
    graph.vs[i]["color"] = couleur_chaque_noeud[i]
    #graph.vs[i]["label_color"] = couleur_chaque_noeud[i]
    graph.vs[i]["label_dist"] = 0
    graph.vs[i]["size"] = 5*(1 + math.log(1+bet[i]))
    graph.vs[i]["label"] = i
    i += 1

layout = graph.layout("kk")
plot(graph, layout = layout, bbox = (800,800))

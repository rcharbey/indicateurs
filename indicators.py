import sys
sys.path.append('../Methodes_graphe')
import methods_graph
from igraph import *
import argparse


#python indicators.py export_sample 011171e509d303ecf1710551179e5c1a6e299f0e


def main():
    
    parser = argparse.ArgumentParser(description="truc")
    parser.add_argument('dossier', help="emplacement dans data de ego")
    parser.add_argument('nom', help="nom de ego")
    parser.add_argument('--option', '-o', nargs='+')
    args = parser.parse_args()
    
    fichier = open("Resultats/indicators.csv","a")
    
    fichier.write("\n")
   
    triplet = methods_graph.create_graph(args.dossier, args.nom)
    graph = triplet[0]
    
    #fichier.write("id ego : ")
    fichier.write(args.nom)
    fichier.write(";;")
    
    index_to_vertex = triplet[1]
    vertex_to_index = triplet[2]
    
    #fichier.write("nombre d'amis : ") 
    fichier.write(str(len(index_to_vertex)))
    fichier.write(";")
    
    #fichier.write("nombre de lien d'amitie : ") 
    fichier.write(str(len(graph.es)))
    fichier.write(";")
        
    if args.option == None:
        clusters_list = graph.community_multilevel()
        #fichier.write("nombre de communautes de Louvain : " 
        fichier.write(str(len(clusters_list)))
        fichier.write(";")
        
        graph_list = graph.decompose(minelements = 6)
        max_nb = 0
        max_index = -1
        for g in graph_list:
            if len(g.vs) > max_nb:
                max_index = graph_list.index(g)
                max_nb = len(g.vs)
        if max_index == -1:
            fichier.write("_")
        else:
            graph_max_cc = graph_list[max_index]
            clusters_list = graph_max_cc.community_multilevel()
        
            #fichier.write("nombre de noeuds de la plus grands composante connexe : ")
            fichier.write(str(len(graph_max_cc.vs)))
        fichier.write(";")
        
        #fichier.write("nombre de communautes de Louvain de la plus grande composante connexe: ")
        fichier.write(str(len(clusters_list)))
        fichier.write(";" )
    
        #fichier.write("diametre du graphe : ")
        fichier.write(str(graph.diameter()))
        fichier.write(";")
        
        #fichier.write("nombre de noeuds isoles : ")
        fichier.write(str(len(index_to_vertex) - len(graph.vs)))
        fichier.write(";")
    
        clusters_list = graph.community_multilevel()
        #fichier.write("modularite : ")
        fichier.write(str(round(clusters_list.modularity,2)))
        fichier.write(";")
            
        #fichier.write("coefficient de clustering : ")
        fichier.write(str(round(graph.transitivity_undirected(),2)))
        fichier.write(";")
        
        #fichier.write("densite du graphe : ")
        fichier.write(str(round(graph.density(),2)))
        fichier.write(";")
        
        #eigen = graph.eigenvector_centrality(directed = False)
        
        #for v in graph.vs:
            #fichier.write(v["name"] + " - degree : " + str(v.degree()) + " - betweenness : " + str(round(v.betweenness(),1)) + " - closeness : " + str(v.closeness()) +  " - eigenvector : " 
            #+ str(round(eigen[v.index],1)) + "\n")
            
        print args.nom + " ok"
        fichier.close()
        
    #if "louvain" in args.option:
        #clusters_list = graph.community_multilevel()
        #i = 0
        #for cluster in clusters_list:
            #for vertex in cluster:
                #colours[vertex] = rainbow[i]
            #i += 1
        #graph.vs['color'] = colours
        #layout = graph.layout_fruchterman_reingold(repulserad = len(graph.vs)**2.5)
        #print "nombre de communautes de Louvain : " + str(len(clusters_list))
        #plot(graph, layout=layout)
    
    #if "louvain_max_cc" in args.option:
        #graph_list = graph.decompose(minelements = 2)
        #max_nb = 0
        #max_index = 0
        #for g in graph_list:
            #if len(g.vs) > max_nb:
                #max_index = graph_list.index(g)
                #max_nb = len(g.vs)
        #graph_max_cc = graph_list[max_index]
        #clusters_list = graph_max_cc.community_multilevel()
        #i = 0
        #for cluster in clusters_list:
            #for vertex in cluster:
                #colours[vertex] = rainbow[i]
            #i += 1
        #graph_max_cc.vs['color'] = colours
        #layout = graph.layout_fruchterman_reingold(repulserad = len(graph.vs)**2.5)
        #print "nombre de communautes de Louvain de la plus grande composante connexe: " + str(len(clusters_list))
        #plot(graph_max_cc, layout=layout)
    
    #if "diameter" in args.option:
        #print "diametre du graphe : ",
        #print graph.diameter()
        
    #if "nb_iso" in args.option:
        #nb_iso = 0
        #for v in graph.vs:
            #if v.degree == 0:
                #nb_iso += 1
        #print "nombre de noeuds isoles : ",
        #print nb_iso
    
    #if "modularity" in args.option:
        #clusters_list = graph.community_multilevel()
        #print "modularite : ",
        #print clusters_list.modularity
            
    #if "coeff_clustering" in args.option:
        #print "coefficient de clusturing : ",
        #print graph.transitivity_undirected()
        
    #if "density" in args.option:
        #print "densite du graphe : ",
        #print graph.density()
main()
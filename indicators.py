import sys
sys.path.append('METHODES_GRAPHE')
import methods_graph
from igraph import *
import argparse


# python indicators.py DATA/export_sample/011171e509d303ecf1710551179e5c1a6e299f0e

rainbow = ["blue", "green", "red", "purple", "yellow", "grey", "black", "pink", "orange", "brown", "white", "cyan", "magenta"]

def main():
    
    parser = argparse.ArgumentParser(description="truc")
    parser.add_argument('ego', help="dossier où se trouvent les fichiers jsons de ego")
    parser.add_argument('--option', '-o', nargs='+')
    args = parser.parse_args()
    
    fichier = open("Resultats/indicators.csv","a")
    
    fichier.write("\n")
   
    triplet = methods_graph.create_graph(args.ego, args.nom)
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
        
    cmpt = 0
    for v in graph.vs:
        if v.degree() == 0:
            cmpt += 1
                
    if args.option == None:
        clusters_list = graph.community_multilevel()
        #fichier.write("nombre de communautes de Louvain : " 
        compt_com = 0
        for clu in clusters_list:
            if len(clu) >= 6:
                compt_com += 1
        fichier.write(str(compt_com))
        fichier.write(";")
        
        graph_list = graph.decompose()
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
        compt_com_max_cc = 0
        for cl in clusters_list:
            if len(cl) >= 6:
                compt_com_max_cc += 1
        fichier.write(str(compt_com_max_cc))
        fichier.write(";" )
    
        #fichier.write("diametre du graphe : ")
        fichier.write(str(graph.diameter()))
        fichier.write(";")
        
        #fichier.write("nombre de noeuds isoles : ")
        fichier.write(str(cmpt))
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
        return
        
    if "louvain" in args.option:
        colours = [""]*len(graph.vs)
        clusters_list = graph.community_multilevel()
        i = 0
        for cluster in clusters_list:
            for vertex in cluster:
                colours[vertex] = rainbow[i]
            i += 1
        graph.vs['color'] = colours
        layout = graph.layout_fruchterman_reingold(repulserad = len(graph.vs)**2.5)
        print "nombre de communautes de Louvain : " + str(len(clusters_list))
        plot(graph, layout=layout)
    
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

# -*- coding: utf-8 -*-

import sys
import csv
sys.path.append('./Jsons')
sys.path.append('./GALLERY')
sys.path.append('./Graphs')
import os.path
from igraph import *
import argparse
import main_jsons
import main_graphs


# python indicators.py DATA/export_sample/011171e509d303ecf1710551179e5c1a6e299f0e

rainbow = ["blue", "green", "red", "purple", "yellow", "grey", "black", "pink", "orange", "brown", "white", "cyan", "magenta"]

def print_info_commenters(folder, ego):
    list_of_friends = main_jsons.list_of_friends(folder, ego)
    info_commenters = main_jsons.calculate_info_commenters(folder, ego)
    info_likers = main_jsons.calculate_info_likers(folder, ego)
    info_likers_of_comment = main_jsons.calculate_info_likers_of_comment(folder, ego)
    csv_file = open('GALLERY/'+folder+'/'+ego+'/'+'list_of_commenters_likers.csv', 'wb')
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow(['id', 'nombre de commentaires', 'nombre de statuts commentes', 'nombre de likes de statuts', 'nombre de likes de commentaires']) 
    
    sorted_info = []
    for friend in list_of_friends:
        if friend in info_commenters:
            info_commenter = info_commenters[friend]
        else:
            info_commenter = {'nb_of_comments' : 0, 'nb_of_statuses' : 0}
        if friend in info_likers:
            info_liker = info_likers[friend]
        else:
            info_liker = 0
        if friend in info_likers_of_comment:
            info_liker_of_comment = info_likers_of_comment[friend]
        else:
            info_liker_of_comment = 0
        sorted_info.append((friend, info_commenter['nb_of_comments'], info_commenter['nb_of_statuses'], info_liker, info_liker_of_comment))
        
    sorted_info.sort(key=lambda tup: 4*tup[1]+3*tup[3]+2*tup[4]+tup[1], reverse = True) 
    
    for info in sorted_info:
        writer.writerow(info) 
        

def print_info_statuses(folder, ego):
    dict_of_commenter_per_status =  main_jsons.calculate_dict_of_commenters_per_status(folder, ego)
    dict_of_likers_per_status = main_jsons.calculate_dict_of_likers_per_status(folder, ego)
    dict_of_likers_of_comments_per_status = main_jsons.calculate_dict_of_likers_of_comments_per_status(folder, ego)
    
    csv_file = open('GALLERY/'+folder+'/'+ego+'/'+'list_of_statuses.csv', 'wb')
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow(['id', 'nombre de commentaires', 'nombre de commentateurs', 'nombre de commentaires d\'ego', 'nombre de likes', 'nombre de likes de commentaires']) 
    sorted_info = []
    for status in dict_of_commenter_per_status:
        sum_comments = 0
        nb_ego = 0
        list_of_commenters_of_status = dict_of_commenter_per_status[status]
        for commenter in list_of_commenters_of_status:
            sum_comments += list_of_commenters_of_status[commenter]
        if 0 in list_of_commenters_of_status:
            nb_ego = list_of_commenters_of_status[0]
        sorted_info.append((status, sum_comments, len(list_of_commenters_of_status), nb_ego, len(dict_of_likers_per_status[status]), len(dict_of_likers_of_comments_per_status[status])))
    
    sorted_info.sort(key=lambda tup: 2*tup[1]+tup[4], reverse = True) 
    
    for info in sorted_info:
        writer.writerow(info)
        

def print_info_communities(folder, ego):
    retour 'zou'
    

def main():
    parser = argparse.ArgumentParser(description="truc")
    parser.add_argument('path', help="dossier où se trouvent les fichiers jsons de ego")
    parser.add_argument('--option', '-o', nargs='+')
    args = parser.parse_args()

    ego = os.path.basename(os.path.dirname(args.path + '/'))
    # NB : basename n'interprète pas le slash de fin comme unix, d'où le trick
    
    fichier = open("Resultats/indicators.csv","a")
    
    fichier.write("\n")
   
    triplet = methods_graph.create_graph(args.path)
    graph = triplet[0]
    
    #fichier.write("id ego : ")
    fichier.write(ego)
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
            
        print ego + " ok"
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

print_info_commenters('csa', '0baf8b741f10e7684c2c810319728802f44b524d')
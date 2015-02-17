# -*- coding: utf-8 -*-

import os
import csv

def main(folder, ego, graph):    
    if not os.path.isfile('GALLERY/'+folder+'/'+ego+'/Graphs/friends.gml'):
        return
    
    if not os.path.isdir('GALLERY/'+folder+'/'+ego+'/CSV'):
        os.mkdir('GALLERY/'+folder+'/'+ego+'/CSV')
    
    en_tete = []
    infos = []
    
    #nombre d'amis
    en_tete.append(u'nombre d\'amis')
    infos.append(len(graph.vs))
    
    #nombre de liens 
    en_tete.append(u'nombre de liens')
    infos.append(len(graph.es))
    
    #sommets isolés
    cmpt_sommets_isoles = 0
    for v in graph.vs:
        if v.degree() == 0:
            cmpt_sommets_isoles += 1
    en_tete.append(u'sommets isolés')
    infos.append(cmpt_sommets_isoles)
                
    #Louvain            
    clusters_list = graph.community_multilevel()
    compt_com = 0
    for clu in clusters_list:
        if len(clu) >= 6:
            compt_com += 1
    en_tete.append(u'nombre de communautés de Louvain')
    infos.append(compt_com)
    
    #Modularité
    en_tete.append(u'modularité')
    infos.append(round(clusters_list.modularity,2))
    
    #max CC
    graph_list = graph.decompose()
    max_nb = 0
    max_index = 0
    i = 0
    for g in graph_list:
        if len(g.vs) > max_nb:
            max_index = i
            max_nb = len(g.vs)
        i += 1
    en_tete.append(u'taille de la plus grande composante connexe')
    infos.append(max_nb)
    
    #Louvain max CC
    graph_max_cc = graph_list[max_index]
    clusters_list = graph_max_cc.community_multilevel()
    
    compt_com_max_cc = 0
    for cl in clusters_list:
        if len(cl) >= 6:
            compt_com_max_cc += 1
    en_tete.append(u'nombre de communautés de la plus grande CC')
    infos.append(compt_com_max_cc)

    #Diametre
    en_tete.append(u'diamètre')
    infos.append(graph.diameter())
        
    #Coefficient de clustering
    en_tete.append(u'coefficient de clustering')
    infos.append(round(graph.transitivity_undirected(),2))
    
    #Densité
    en_tete.append(u'densité')
    infos.append(round(graph.density(),2))
    
    
    fichier = csv.writer(open('GALLERY/'+folder+'/'+ego+'/CSV/indicators_classics.csv','wb'), delimiter = ';')
    fichier.writerow([x.encode('utf-8') for x in en_tete])
    new_info = []
    for i in infos:
        if isinstance(i, str):
            new_info.append(unicode(i.decode('utf-8')).encode('utf-8'))
        elif isinstance(i, unicode):
            new_info.append(i.encode('utf-8'))
        else:
            new_info.append(i)
    fichier.writerow(new_info)
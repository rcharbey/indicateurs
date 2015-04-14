# -*- coding: utf-8 -*-

import sys
import csv
sys.path.append('./Jsons')
sys.path.append('./GALLERY')
sys.path.append('./Graphs')
import os.path
import os
from igraph import *
import argparse
import main_jsons
import main_graphs
import time
import indicators_classic

def print_info_commenters_likers(folder, ego, clusters_list):
    list_of_friends = main_jsons.list_of_friends(folder, ego)
    info_commenters = main_jsons.calculate_info_commenters(folder, ego)
    info_likers = main_jsons.calculate_info_likers(folder, ego)
    info_likers_of_comment = main_jsons.calculate_info_likers_of_comment(folder, ego)
    csv_file = open('GALLERY/'+folder+'/'+ego+'/'+'CSV/list_of_commenters_likers.csv', 'wb')
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow(['id/nom', 'nombre de commentaires', 'nombre de statuts commentés', 'nombre de likes de statuts', 'nombre de likes de commentaires', 'cluster']) 
    
    sorted_info = []
    for friend in list_of_friends:
        cluster_of_this_friend = 0
        for cluster in clusters_list:
            cluster_of_this_friend += 1
            if friend in cluster:
                break
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
        friend_info = main_jsons.find_friend(folder, ego, friend)
        if 'name' in friend_info:
            friend = friend_info['name']
        infos_list = ((friend, 
                            info_commenter['nb_of_comments'], 
                            info_commenter['nb_of_statuses'], 
                            info_liker, 
                            info_liker_of_comment,
                            cluster_of_this_friend))
        
        sorted_info.append([unicode(s).encode("utf-8") for s in infos_list])
        
    sorted_info.sort(key=lambda tup: 4*tup[1]+3*tup[3]+2*tup[4]+tup[1], reverse = True) 
    
    for info in sorted_info:
        writer.writerow(info) 
        
    csv_file.close()
        
def print_info_statuses(folder, ego, clusters_list):
    dict_of_commenter_per_status =  main_jsons.calculate_dict_of_commenters_per_status(folder, ego)
    dict_of_likers_per_status = main_jsons.calculate_dict_of_likers_per_status(folder, ego)
    dict_of_likers_of_comments_per_status = main_jsons.calculate_dict_of_likers_of_comments_per_status(folder, ego)
    
    csv_file = open('GALLERY_STATUSES/'+folder+'/'+ego+'_statuses.csv', 'wb')
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow(['id',
                     'auteur', 
                     'destinataire', 
                     'nombre de commentaires', 
                     'nombre de commentateurs', 
                     'nombre de commentaires d\'ego', 
                     'nombre de likes', 
                     'nombre de likes de commentaires', 
                     'texte', 
                     'lien', 
                     'type', 
                     'date', 
                     'liste des commentateurs', 
                     'liste des likers',
                     'cluster qui a le plus intéragis'])
    sorted_info = []
    for status in dict_of_commenter_per_status:
        sum_comments = 0
        nb_ego = 0
        list_of_commenters_of_status = dict_of_commenter_per_status[status]
        for commenter in list_of_commenters_of_status:
            sum_comments += list_of_commenters_of_status[commenter]
        if 0 in list_of_commenters_of_status:
            nb_ego = list_of_commenters_of_status[0]
        status_info = main_jsons.find_status(folder, ego, status)
        if not 'from' in status_info:
            status_info['from'] = ''
        else:
            if not 'name' in status_info['from']:
                status_info['from']['name'] = status_info['from']['id']
        if not 'to' in status_info:
            status_info['to'] = ''
        else:
            temp = ''
            for dest in status_info['to']:
                if not 'name' in dest:
                    temp += dest['id'] + ' '
                else:
                    temp += dest['name'] + ' '
            status_info['to'] = temp
        if 'link' in status_info:
            if 'message' in status_info['link']:
                status_info['message'] = status_info['link']['message']
            else:
                status_info['message'] = ''
        else:
            status_info['message'] = ''
        if not 'type' in status_info:
            status_info['type'] = ''
        else:
            temp = ''
            for type in status_info['type']:
                temp += type + ' '
            status_info['type'] = temp
        if not 'link' in status_info:
            status_info['link'] = ' '
        else:
            if not 'link' in status_info['link']:
                status_info['link'] = ' '
            else:
                status_info['link'] = status_info['link']['link']
        if 'time' in status_info:
            date_object = time.localtime(status_info['time']/1000)
            date = str(date_object.tm_mday) + ' ' + str(date_object.tm_mon) + ' ' + str(date_object.tm_year) 
        elif 'created' in status_info:
            date_object = time.localtime(status_info['created']/1000)
            date = str(date_object.tm_mday) + ' ' + str(date_object.tm_mon) + ' ' + str(date_object.tm_year) 
        else:
            date = ''
        #liste des commentateurs
        print_commenters = u''
        for commenter in list_of_commenters_of_status:
            if commenter != 0 and commenter != None:
                print_commenters += commenter + ' : ' + str(list_of_commenters_of_status[commenter]) + ' - '
        #liste des likers
        list_of_likers_of_status = dict_of_likers_per_status[status]
        print_likers = u''
        for liker in list_of_likers_of_status:
            if liker == 0:
                liker = ego.decode('utf-8')
            print_likers += liker + ' - '
        #cluster qui a le plus intéragis
        max_cluster = 0
        id_max_cluster = 0
        current_cluster = 0
        for cluster in clusters_list:
            current_cluster += 1
            temp = 0
            for person in cluster:
                if person in list_of_commenters_of_status:
                    temp += list_of_commenters_of_status[person]
                if person in list_of_likers_of_status:
                    temp += 1
            if temp > max_cluster:
                max_cluster = temp
                id_max_cluster = current_cluster
        infos_list = (status, 
                    status_info['from']['name'], 
                    status_info['to'], 
                    sum_comments, 
                    len(list_of_commenters_of_status), 
                    nb_ego, 
                    len(dict_of_likers_per_status[status]), 
                    len(dict_of_likers_of_comments_per_status[status]), 
                    status_info['message'], 
                    status_info['link'], 
                    status_info['type'], 
                    date,
                    print_commenters[0:len(print_commenters)-2],
                    print_likers[0:len(print_likers)-2],
                    id_max_cluster)
        sorted_info.append([unicode(s).encode("utf-8") for s in infos_list])
    
    sorted_info.sort(key=lambda tup: 2*tup[3]+tup[6], reverse = True) 
    
    for info in sorted_info:
        writer.writerow(info)
        
    csv_file.close()
        
def print_info_communities(folder, ego, graph):
    clusters_list_temp = graph.community_multilevel()
    clusters_list = []
    for cluster in clusters_list_temp:
        temp = []
        for index in cluster:
            temp.append(graph.vs[index]['name'].decode('utf-8'))
        clusters_list.append(temp)
        
    info_commenters = main_jsons.calculate_info_commenters(folder, ego)
    info_likers = main_jsons.calculate_info_likers(folder, ego)
    info_likers_of_comment = main_jsons.calculate_info_likers_of_comment(folder, ego)

    info_per_cluster = {}
    for cluster in clusters_list:
        info_per_cluster[str(cluster)] = {'nb_comments' : 0, 'nb_likes' : 0, 'nb_likes_of_comments' : 0}
    for cluster in clusters_list:
        info_current = info_per_cluster[str(cluster)]
        for name in cluster:
            if name in info_commenters:
                info_current['nb_comments'] += info_commenters[name]['nb_of_comments']
            if name in info_likers:
                info_current['nb_likes'] += info_likers[name]
            if name in info_likers_of_comment:
                info_current['nb_likes_of_comments'] += info_likers_of_comment[name]
    index_cluster = 0
    sorted_info = []
    for cluster in clusters_list:
        index_cluster += 1
        info_current = info_per_cluster[str(cluster)]
        sorted_info.append((cluster, 
                            info_current['nb_comments'], 
                            info_current['nb_likes'], 
                            info_current['nb_likes_of_comments'],
                            index_cluster))
    sorted_info.sort(key=lambda tup: 3*tup[1]+2*tup[2]+tup[1], reverse = True)
    csv_file = open('GALLERY/'+folder+'/'+ego+'/CSV/list_of_clusters.csv', 'wb')
    writer = csv.writer(csv_file, delimiter = ';')
    for info in sorted_info:
        temp = [info[4]]
        for name in info[0]:
            friend_info = main_jsons.find_friend(folder, ego, name)
            if 'name' in friend_info:
                temp.append(friend_info['name'])
            else:
                temp.append(friend_info['id'])
        writer.writerow([unicode(elem).encode('utf-8') for elem in temp])
        writer.writerow(['nombre de commentaires', 
                         'nombre de likes', 
                         'nombre de likes de commentaires'])
        to_write = []
        writer.writerow(info[1:len(info)-1])
    csv_file.close()
    return clusters_list
        
def print_info_pages(folder, ego):
    csv_file = open('GALLERY/'+folder+'/'+ego+'/CSV/list_of_liked_pages.csv', 'wb')
    writer = csv.writer(csv_file, delimiter = ';')
    list_of_liked_pages = main_jsons.list_of_liked_pages(folder, ego)
    writer.writerow(('nom', 'categorie'))
    for info in list_of_liked_pages:
        writer.writerow((info['name'].encode('ascii', 'ignore'), info['category'].encode('ascii', 'ignore')))
    csv_file.close()

def print_info_qualify(folder, ego):
    csv_file = open('GALLERY/'+folder+'/'+ego+'/CSV/list_of_qualified.csv', 'wb')
    tab_duration = ['toujours (enfance, études)', 'longtemps (+5 ans)', 'quelques temps (1-5 ans)', 'Récemment (-1 an)']
    tab_frequency = ['tous les jours ou presque',
                     'au moins une fois par semaine',
                     'au moins une fois par mois',
                     'au moins une fois tous les trois mois',
                     'au moins une fois tous les six mois',
                     'au moins une fois par an',
                     'moins d\'une fois par an']
        
    writer = csv.writer(csv_file, delimiter = ';')
    writer.writerow(('nom',
                    'durée', 
                    'fréquence des rencontres', 
                    'fréquence des communications', 
                    'proximité affective',  
                    'conaissance', 
                    'famille', 
                    'colègue', 
                    'ami', 
                    'autre info'))                     
    list_of_qualified = main_jsons.list_of_qualified(folder, ego)
    for qualified_data in list_of_qualified:
        qualified = qualified_data['data']
        info = (main_jsons.find_friend(folder, ego, qualified_data['user_id'])['name'],
                tab_duration[int(qualified['since'])-1],
                tab_frequency[int(qualified['close'])-1],
                tab_frequency[int(qualified['begin'])-1],
                qualified['affect'],
                qualified['acquaintance'],
                qualified['family'],
                qualified['coworker'],
                qualified['friend'],
                qualified['other'])
        new_info = []
        for i in info:
            if isinstance(i, str):
                new_info.append(unicode(i.decode('utf-8')).encode('utf-8'))
            elif isinstance(i, unicode):
                new_info.append(i.encode('utf-8'))
            else:
                new_info.append(i)
        writer.writerow(new_info)
    csv_file.close()
        

def main(folder_arg = None, ego_arg = None, options = None):
    if folder_arg != None and ego_arg != None:
        graph = main_graphs.import_graph(folder_arg, ego_arg, 'friends')
        print_info_qualify(folder_arg, ego_arg)
        clusters_list = print_info_communities(folder_arg, ego_arg, graph)
        print_info_statuses(folder_arg, ego_arg, clusters_list)
        print_info_commenters_likers(folder_arg, ego_arg, clusters_list)
        print_info_pages(folder_arg, ego_arg)
        return
    file_to_write_classic = 'GALLERY/General/indicators_classics.csv'
    if 'lightcom' in options:
        file_to_write_classic = 'GALLERY/General/indicators_classics_com.csv'
    if not os.path.isfile(file_to_write_classic):
        file = open(file_to_write_classic, 'wb')
        csv_writer = csv.writer(file, delimiter = ';')
        en_tete = []
        en_tete.append(u'id')
        en_tete.append(u'dossier')
        en_tete.append(u'nombre d\'amis')
        en_tete.append(u'nombre de liens')
        en_tete.append(u'sommets isolés')
        en_tete.append(u'nombre de communautés de Louvain')
        en_tete.append(u'modularité')
        en_tete.append(u'taille de la plus grande composante connexe')
        en_tete.append(u'nombre de communautés de la plus grande CC')
        en_tete.append(u'diamètre')
        en_tete.append(u'coefficient de clustering')
        en_tete.append(u'densité')
        en_tete.append(u'betweenness (Freeman)')
        en_tete.append(u'type')
        csv_writer.writerow([x.encode('utf-8') for x in en_tete])
        file.close
    file = open(file_to_write_classic, 'rb')
    csv_reader = csv.reader(file, delimiter = ';')
    ego_already_done = []
    for row in csv_reader:
        ego_already_done.append(row[0])
    file.close()
    list_folders = [f for f in os.listdir('DATA/') if os.path.isdir(os.path.join('DATA', f))]
    for folder in list_folders:
        if 'all_2014' in folder or 'entre' in folder:
            continue
        list_ego = [f for f in os.listdir('DATA/'+folder) if os.path.isdir(os.path.join('DATA/'+folder, f))]
        for ego in list_ego:
            print folder,
            print ' ',
            print ego,
            print ' : infos',
            if options != None:
                graph_format = ''
                if 'light' in options:
                    graph_format = 'edgelist'
                    if not os.path.isfile('GALLERY/'+folder+'/'+ego+'/Graphs/light_graph'):
                        print ' - pas de graphe'
                        continue
                    if os.stat('GALLERY/'+folder+'/'+ego+'/Graphs/light_graph').st_size == 0:
                        print ' - graphe vide'
                        continue
                    graph = main_graphs.import_graph(folder, ego, 'friends', graph_format)
                elif 'lightcom' in options:
                    graph_format = 'edgelist'
                    if not os.path.isfile('GALLERY/'+folder+'/'+ego+'/Graphs/light_graph_fc'):
                        print ' - pas de graphe'
                        continue
                    if os.stat('GALLERY/'+folder+'/'+ego+'/Graphs/light_graph_fc').st_size == 0:
                        print ' - graphe vide'
                        continue
                    graph = main_graphs.import_graph(folder, ego, 'friends', graph_format, True)
                    for v in graph.vs:
                        v['id'] = v.index
                    for v in graph.vs:
                        if v.degree() == 0:
                            graph.delete_vertices(v.index)
            else:
                graph_format = 'gml'
                if not os.path.isfile('GALLERY/'+folder+'/'+ego+'/Graphs/friends.gml'):
                    print ' - pas de graphe'
                    continue
                else:
                    graph = main_graphs.import_graph(folder, ego, 'friends')
            #print_info_qualify(folder, ego)
            #clusters_list = print_info_communities(folder, ego, graph)
            #print_info_statuses(folder, ego, clusters_list)
            #print_info_commenters_likers(folder, ego, clusters_list)
            #print_info_pages(folder, ego)
            if ego in ego_already_done:
                continue
            indicators_classic.main(folder, ego, graph.as_undirected(), graph_format)
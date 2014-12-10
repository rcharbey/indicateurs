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


def print_info_commenters_likers(folder, ego):
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
        friend_info = main_jsons.find_friend(folder, ego, friend)
        if 'name' in friend_info:
            friend = friend_info['name'].encode('ascii', 'ignore')
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
    writer.writerow(['id', 'auteur', 'destinataire', 'nombre de commentaires', 'nombre de commentateurs', 'nombre de commentaires d\'ego', 'nombre de likes', 'nombre de likes de commentaires', 'texte', 'lien', 'type'])
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
        if not 'story' in status_info:
            status_info['story'] = ''
        else:
            status_info['story'] = status_info['story'].encode('ascii', 'ignore')
            temp = ''
            for i in range(0, len(status_info['story'])):
                temp += status_info['story'][i]
                if status_info['story'][i] == ';':
                    temp += ','
            status_info['story'] = temp
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
            
        sorted_info.append((status, status_info['from']['name'].encode('ascii', 'ignore'), status_info['to'].encode('ascii', 'ignore'), sum_comments, len(list_of_commenters_of_status), nb_ego, len(dict_of_likers_per_status[status]), len(dict_of_likers_of_comments_per_status[status]), status_info['story'].encode('ascii', 'ignore'), status_info['link'].encode('ascii', 'ignore'), status_info['type'].encode('ascii', 'ignore')))
    
    sorted_info.sort(key=lambda tup: 2*tup[3]+tup[6], reverse = True) 
    
    for info in sorted_info:
        writer.writerow(info)
        

def print_info_communities(folder, ego):
    if not os.path.isfile('GALLERY/'+folder+'/'+ego+'/friends.gml'):
        return
    graph = main_graphs.import_graph(folder, ego, 'friends')
    clusters_list = graph.community_multilevel()
    i = 0
    csv_file = open('GALLERY/'+folder+'/'+ego+'/'+'list_of_commenters_likers.csv', 'rb')
    info_commenters_likers = csv.reader(csv_file, delimiter=';') 
    info_per_cluster = {}
    for cluster in clusters_list:
        info_per_cluster[str(cluster)] = {'nb_comments' : 0, 'nb_likes' : 0, 'nb_likes_of_comments' : 0}
    sorted_info = []
    for row in info_commenters_likers:
        for cluster in clusters_list:
            info_current = info_per_cluster[str(cluster)]
            for vertex in cluster:
                if graph.vs[vertex]['name'] == row[0]:
                    info_current['nb_comments'] += int(row[1])
                    info_current['nb_likes'] += int(row[3])
                    info_current['nb_likes_of_comments'] += int(row[4])
                    break
    for cluster in clusters_list:
        info_current = info_per_cluster[str(cluster)]
        sorted_info.append((cluster, info_current['nb_comments'], info_current['nb_likes'], info_current['nb_likes_of_comments']))
    sorted_info.sort(key=lambda tup: 3*tup[1]+2*tup[2]+tup[1], reverse = True)
    csv_file = open('GALLERY/'+folder+'/'+ego+'/'+'list_of_clusters.csv', 'wb')
    writer = csv.writer(csv_file, delimiter = ';')
    for cluster in sorted_info:
        temp = []
        for vertex in cluster[0]:
            friend_info = main_jsons.find_friend(folder, ego, graph.vs[vertex]['name'])
            if 'name' in friend_info:
                temp.append(friend_info['name'].encode('ascii', 'ignore'))
            else:
                temp.append(friend_info['id'])
        writer.writerow(temp)
        writer.writerow(['nombre de commentaires', 'nombre de likes', 'nombre de likes de commentaires'])
        to_write = []
        writer.writerow(cluster[1:len(cluster)])

def main(folder_arg = None, ego_arg = None):
    if folder_arg != None and ego_arg != None:
        print_info_statuses(folder_arg, ego_arg)
        print_info_commenters_likers(folder_arg, ego_arg)
        print_info_communities(folder_arg, ego_arg)
        return
    list_folders = [f for f in os.listdir('DATA/') if os.path.isdir(os.path.join('GALLERY', f))]
    for folder in list_folders:
	list_ego = [f for f in os.listdir('DATA/'+folder) if os.path.isdir(os.path.join('GALLERY/'+folder, f))]
        for ego in list_ego:
            print folder,
            print ' ',
            print ego,
            print ' : infos'
            print_info_statuses(folder, ego)
            print_info_commenters_likers(folder, ego)
            print_info_communities(folder, ego)


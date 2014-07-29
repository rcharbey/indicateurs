import sys
import json
from igraph import *
import math

#Affichage du graphes amis/commentaires

def create_graph(folder, name):
    path = "./data/"+folder+"/"+name+"/friends.jsons"
    f = open(path, 'r')
    dict_of_edges = {}
    index_to_vertex = {}
    index_to_graph_in = {}
    vertex_to_index = {}
    nb_of_vertices = 0
    for line in f:
        jr = json.loads(line)
        if not "mutual" in jr:
            continue
        if not jr["id"] in vertex_to_index:
            vertex_to_index[jr["id"]] = nb_of_vertices
            index_to_vertex[nb_of_vertices] = jr["id"]
            index_to_graph_in[nb_of_vertices] = 0
            nb_of_vertices += 1
        for neighbor in jr["mutual"]:
            if not neighbor["id"] in vertex_to_index:
                vertex_to_index[neighbor["id"]] = nb_of_vertices
                index_to_vertex[nb_of_vertices] = neighbor["id"]
                index_to_graph_in[nb_of_vertices] = 0
                nb_of_vertices += 1
            if vertex_to_index[jr["id"]] < vertex_to_index[neighbor["id"]]:
                dict_of_edges[(vertex_to_index[jr["id"]], vertex_to_index[neighbor["id"]])] = [0,0]      
    f.close()
    path = "./data/"+folder+"/"+name+"/statuses.jsons"
    f = open(path, 'r')
    nb_comments_per_alter = []
    nb_comments = 0
    for line in f:
        nb_comments += 1
        jr = json.loads(line)
        if jr["from"]["id"] != name:
            continue
        if "comments" in jr:
            list_current_com = []
            for v in vertex_to_index:
                nb_comments_per_alter.append(0)
            for comment in jr["comments"]:
                commenter = comment["from"]["id"]
                if commenter != name :
                    if not commenter in vertex_to_index:
                        nb_comments_per_alter.append(0)
                        vertex_to_index[commenter] = nb_of_vertices
                        index_to_vertex[nb_of_vertices] = commenter
                        index_to_graph_in[nb_of_vertices] = 1
                        nb_of_vertices += 1
                    else:
                        nb_comments_per_alter[vertex_to_index[commenter]] += 1
                        if index_to_graph_in[vertex_to_index[commenter]] == 0:
                            index_to_graph_in[vertex_to_index[commenter]] = 3
            for comment in jr["comments"]:
                if not comment["from"]["id"] == name : 
                    for comment_second in jr["comments"]:
                        if not comment_second["from"]["id"] == name:
                            id_comment = vertex_to_index[comment["from"]["id"]]
                            id_second = vertex_to_index[comment_second["from"]["id"]]
                            if id_comment < id_second:
                                if (id_comment, id_second) not in dict_of_edges:
                                    dict_of_edges[(id_comment, id_second)] = [1,1]
                                else:
                                    if dict_of_edges[(id_comment, id_second)][0] == 0:
                                        dict_of_edges[(id_comment, id_second)][0] = 3
                                    dict_of_edges[(id_comment, id_second)][1] += 1
        #if "likes" in jr:
            #for like in jr["likes"]:
                #if not like["id"] == name:
                    #if not like["id"] in vertex_to_index:
                        #nb_comments_per_alter.append(0)
                        #vertex_to_index[like["id"]] = nb_of_vertices
                        #index_to_vertex[nb_of_vertices] = like["id"]
                        #index_to_graph_in[nb_of_vertices] = 2
                        #nb_of_vertices += 1
                    #else:
                        #if index_to_graph_in[vertex_to_index[like["id"]]] == 0:
                            #index_to_graph_in[vertex_to_index[like["id"]]] = 4
                        #elif index_to_graph_in[vertex_to_index[like["id"]]] == 1:
                            #index_to_graph_in[vertex_to_index[like["id"]]] = 5
                        #elif index_to_graph_in[vertex_to_index[like["id"]]] == 3:
                            #index_to_graph_in[vertex_to_index[like["id"]]] = 6
            #for like in jr["likes"]:
                #if not like["id"] == name:
                    #for like_second in jr["likes"]:
                        #if not like_second["id"] == name:
                            #id_like = vertex_to_index[like["id"]]
                            #id_second = vertex_to_index[like_second["id"]]
                            #if id_like < id_second:
                                #if (id_like, id_second) not in dict_of_edges:
                                    #dict_of_edges[(id_like, id_second)] = [2,1]
                                #else:
                                    #if dict_of_edges[(id_like, id_second)][0] == 0:
                                        #dict_of_edges[(id_like, id_second)][0] = 4
                                    #elif dict_of_edges[(id_like, id_second)][0] == 1:
                                        #dict_of_edges[(id_like, id_second)][0] = 5
                                    #elif dict_of_edges[(id_like, id_second)][0] == 3:
                                        #dict_of_edges[(id_like, id_second)][0] = 6                                       
    f.close()
    graph = Graph(dict_of_edges.keys())
    return (graph, index_to_graph_in, dict_of_edges, index_to_vertex)
    
    
triple = create_graph(sys.argv[1], sys.argv[2])
graph = triple[0]
index_to_graph_in = triple[1]
dict_of_edges = triple[2]
index_to_vertex = triple[3]

layout = graph.layout_fruchterman_reingold(repulserad = len(graph.vs)**2.5)

color_dict_vertices = ["lightblue", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "violet", "limegreen", "rgba(0,0,0,0)", "black"]
color_dict_edges = ["darkblue", "rgba(0,0,0,0)", "rgba(0,0,0,0)", "darkviolet", "darkgreen", "rgba(0,0,0,0)", "black"]

plot(graph,layout=layout, vertex_color = [color_dict_vertices[index_to_graph_in[graph_in]] for graph_in in index_to_graph_in], 
     edge_color = [color_dict_edges[dict_of_edges[(e)][0]] for e in dict_of_edges], vertex_size = 10)
     
color_dict_vertices = ["rgba(0,0,0,0)", "lightsalmon", "rgba(0,0,0,0)", "violet", "rgba(0,0,0,0)", "darkorange", "black"]
color_dict_edges = ["rgba(0,0,0,0)", "darkred", "rgba(0,0,0,0)", "darkviolet", "rgba(0,0,0,0)", "orangered", "black"]

for e in graph.es:
    e["width"] = 1+math.log(1+dict_of_edges[e.tuple][1])
     
plot(graph,layout=layout, vertex_color = [color_dict_vertices[index_to_graph_in[graph_in]] for graph_in in index_to_graph_in], 
edge_color = [color_dict_edges[dict_of_edges[(e)][0]] for e in dict_of_edges], vertex_size = 10)

#color_dict_vertices = ["rgba(0,0,0,0)", "rgba(0,0,0,0)", "khaki", "rgba(0,0,0,0)", "limegreen", "darkorange", "black"]
#color_dict_edges = ["rgba(0,0,0,0)", "rgba(0,0,0,0)", "gold", "rgba(0,0,0,0)", "darkgreen", "orangered", "black"]

#for e in graph.es:
    #e["width"] = 1
    
#plot(graph,layout=layout, vertex_color = [color_dict_vertices[index_to_graph_in[graph_in]] for graph_in in index_to_graph_in], 
#edge_color = [color_dict_edges[dict_of_edges[(e)][0]] for e in dict_of_edges], vertex_size = 10)
        
        
#Super families Milo
#David.o.fourquet@gmail.com

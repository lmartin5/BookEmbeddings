"""GraphManager.py
@author lmartin5

This file contains the functions to use the MobiusGraph class to find a
one-page book embedding. You can either search all permutations for an 
embedding, or only search a few.
"""

import sys
import itertools
from MobiusGraph import MobiusGraph
from KleinGraph import KleinGraph
import Permutations

def find_mobius_embedding_with_permutation(perm, edgeSet):
    genA = MobiusGraph(perm, edgeSet)
    genA.place_free_edges()
    graphs = [genA]

    while len(graphs) > 0:
        new_graphs = []
        for graph in graphs:
            if graph.is_graph_placed():
                return graph
            if not graph.is_possible_to_embedd():
                continue
            
            next_edge = graph.remainingEdges[0]
            avail_edges = graph.get_available_edges(next_edge)

            for edge in avail_edges:
                new_graph = graph.copy()
                new_graph.place_edge(edge[0][0], edge[0][1], edge[1])
                new_graphs.append(new_graph)
        graphs = new_graphs

    return -1

def find_mobius_embedding(edgeSet, perms=None, vertices=None, file_prefix="flip_perms_"):
    if perms == None:
        if vertices == None: 
            print("When perms are not specified, the number of vertices must also be given.")
            sys.exit()
        perms = Permutations.get_perms_from_file(vertices, file_prefix)
        perms = Permutations.strings_to_perms(perms)
    
    counter = 0
    for perm in perms:
        print(counter)
        newEdgeSet = edgeSet.copy()
        graph = find_mobius_embedding_with_permutation(perm, newEdgeSet)
        counter += 1
        if graph == -1:
            continue
        else:
            return graph

    return graph

def create_complete_graph_edge_set(numVertices):
    edgeSet = []
    verts = list(range(1, numVertices + 1))
    for element in itertools.product(verts, verts):
        if element[0] < element[1]:
            edgeSet.append(element)

    return edgeSet

def find_klein_embedding_with_permutation(perm, edgeSet):
    genA = KleinGraph(perm, edgeSet)
    genA.place_free_edges()
    graphs = [genA]

    while len(graphs) > 0:
        new_graphs = []
        for graph in graphs:
            if graph.is_graph_placed():
                return graph
            if not graph.is_possible_to_embedd():
                continue
            
            next_edge = graph.remainingEdges[0]
            avail_edges = graph.get_available_edges(next_edge)

            for edge in avail_edges:
                new_graph = graph.copy()
                new_graph.place_edge(edge[0][0], edge[0][1], edge[1])
                new_graphs.append(new_graph)
        graphs = new_graphs

    return -1
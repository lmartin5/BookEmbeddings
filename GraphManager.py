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
from TorusGraph import TorusGraph
import Permutations

from multiprocessing import Pool, cpu_count
from functools import partial

def find_mobius_embedding_with_permutation(perm, edgeSet):
    edgeSet = edgeSet.copy()
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
    num_perms = len(perms)
    backspaces = ""
    progress_message = backspaces + "Graphs Completed: " + str(counter) + " / " + str(num_perms)
    print(progress_message, end="", flush=True)
    backspaces = len(progress_message) * "\b"

    final_graph = -1
    with Pool(cpu_count() - 2) as pool:
        for graph in pool.imap_unordered(partial(find_mobius_embedding_with_permutation, edgeSet=edgeSet), perms):
            counter += 1
            progress_message = backspaces + "Graphs Completed: " + str(counter) + " / " + str(num_perms)
            print(progress_message, end="", flush=True)
            backspaces = len(progress_message) * "\b"

            if graph == -1:
                continue
            else:
                final_graph = graph
                break

    return final_graph

def create_complete_graph_edge_set(numVertices):
    edgeSet = []
    verts = list(range(1, numVertices + 1))
    for element in itertools.product(verts, verts):
        if element[0] < element[1]:
            edgeSet.append(element)

    return edgeSet

def create_complete_bipartite_graph_edge_set(numVertsA, numVertsB):
    edgeSet = []
    setA = list(range(1, numVertsA + 1))
    setB = list(range(numVertsA + 1, numVertsA + numVertsB + 1))
    for element in itertools.product(setA, setB):
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

def find_klein_embedding(edgeSet, perms=None, vertices=None, file_prefix="flip_perms_"):
    if perms == None:
        if vertices == None: 
            print("When perms are not specified, the number of vertices must also be given.")
            print("find_klein_embedding(edgeSet, perms=None, vertices=None, file_prefix=\"flip_perms_\")")
            sys.exit()
        perms = Permutations.get_perms_from_file(vertices, file_prefix)
        perms = Permutations.strings_to_perms(perms)
    
    counter = 0
    num_perms = len(perms)
    backspaces = ""
    for perm in perms:
        progress_message = backspaces + "Graphs Completed: " + str(counter) + " / " + str(num_perms)
        print(progress_message, end="", flush=True)
        backspaces = len(progress_message) * "\b"

        newEdgeSet = edgeSet.copy()
        graph = find_klein_embedding_with_permutation(perm, newEdgeSet)
        counter += 1
        if graph == -1:
            continue
        else:
            print()
            return graph

    print()
    return graph

def find_torus_embedding_with_permutation(perm, edgeSet):
    genA = TorusGraph(perm, edgeSet)
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

def find_torus_embedding(edgeSet, perms=None, vertices=None, file_prefix="flip_perms_"):
    if perms == None:
        if vertices == None: 
            print("When perms are not specified, the number of vertices must also be given.")
            print("find_klein_embedding(edgeSet, perms=None, vertices=None, file_prefix=\"flip_perms_\")")
            sys.exit()
        perms = Permutations.get_perms_from_file(vertices, file_prefix)
        perms = Permutations.strings_to_perms(perms)
    
    counter = 0
    num_perms = len(perms)
    backspaces = ""
    for perm in perms:
        progress_message = backspaces + "Graphs Completed: " + str(counter) + " / " + str(num_perms)
        print(progress_message, end="", flush=True)
        backspaces = len(progress_message) * "\b"

        newEdgeSet = edgeSet.copy()
        graph = find_torus_embedding_with_permutation(perm, newEdgeSet)
        counter += 1
        if graph == -1:
            continue
        else:
            print()
            return graph

    print()
    return graph
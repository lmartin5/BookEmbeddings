"""GraphManager.py
@author lmartin5

This file contains example runs of how the GraphManager class can be
used to search for one-page Mobius book embeddings of a graph. It also contains examples of 
looking for an embedding for one permutation.
"""

from MobiusGraph import MobiusGraph
import Permutations
import GraphManager

def main():
    # Permutations.generate_permutations_to_file(6)
    # perms = Permutations.get_perms_from_file(6)
    # perms = Permutations.remove_flip_elements(perms)
    # Permutations.store_permutations(perms, 6, "flip_perms_")
    # perms = Permutations.get_perms_from_file(6, "flip_perms_")
    # perms = Permutations.strings_to_perms(perms)
    
    # Permutations.generate_permutations_to_file(7)
    # perms = Permutations.get_perms_from_file(7)
    # perms = Permutations.remove_flip_elements(perms)
    # Permutations.store_permutations(perms, 7, "flip_perms_")
    # perms = Permutations.get_perms_from_file(7, "flip_perms_")
    # perms = Permutations.strings_to_perms(perms)
    
    # K6 is embeddable in a Mobius Book
    # spine = [1, 6, 4, 3, 5, 2]
    # edges = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2, 5), (2, 6), (3, 4), (3,5), (3,6), (4, 5), (4, 6), (5, 6)]
    # k6_embedding = GraphManager.find_mobius_embedding(edges, vertices=6)
    # print(k6_embedding)

    # K7 is not embeddable in a Mobius Book
    # perms = Permutations.get_perms_from_file(7, "flip_perms_")
    # perms = Permutations.strings_to_perms(perms)
    # spine = [1, 2, 3, 4, 5, 6, 7]
    # edges = GraphManager.create_complete_graph_edge_set(7)
    # graph = GraphManager.find_mobius_embedding_with_permutation(spine, edges)
    # print(graph)

    '''
    permutations = [1, 2, 3, 4, 5, 6, 7, 14, 12, 10, 8, 13, 11, 9]
    edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (1, 7), (1, 8), (2, 9), (3, 10),
             (4, 11), (5, 12), (6, 13), (7, 14), (8, 10), (9, 11), (10, 12), (11, 13), (12, 14), (8, 13),
             (9, 14)]
    # graph = MobiusGraph(permutations, edges)
    # graph.place_free_edges() # fix, not storing all free edges
    graph = GraphManager.find_mobius_embedding_with_permutation(permutations, edges)
    print(graph)
    '''

    '''
    num_vertices = 11
    perms = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            [5, 2, 3, 4, 1, 6, 7, 8, 9, 10, 11],
            [1, 5, 3, 4, 2, 6, 7, 8, 9, 10, 11],
            [1, 2, 5, 4, 3, 6, 7, 8, 9, 10, 11],
            [1, 2, 3, 5, 4, 6, 7, 8, 9, 10, 11],
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            [1, 2, 3, 4, 6, 5, 7, 8, 9, 10, 11],
            [1, 2, 3, 4, 7, 6, 5, 8, 9, 10, 11],
            [1, 2, 3, 4, 8, 6, 7, 5, 9, 10, 11],
            [1, 2, 3, 4, 9, 6, 7, 8, 5, 10, 11],
            [1, 2, 3, 4, 10, 6, 7, 8, 9, 5, 11],
            [1, 2, 3, 4, 6, 11, 7, 8, 9, 10, 5],
            [1, 4, 3, 2, 6, 5, 7, 8, 9, 10, 11],
            [1, 4, 10, 2, 6, 5, 7, 8, 9, 3, 11],
            [1, 4, 10, 2, 11, 5, 7, 8, 9, 3, 6]]
    edges = [(1,4),(1,5),(1,6),(2,4),(2,5),(2,6),(3,4),(3,5),(3,6),(5,9),(5,10),(5,11),(7,9),(7,10),(7,11),(8,9),(8,10),(8,11)]
    graph = GraphManager.find_mobius_embedding(num_vertices, edges, perms)
    print(graph)
    '''

    '''
    num_vertices = 8
    edges = []
    for edge in range(0, num_vertices):
        conn_verts = [edge, (edge + 1) % num_vertices]
        edges.append((min(conn_verts) + 1, max(conn_verts) + 1))
        conn_verts = [edge, (edge + 4) % num_vertices]
        edges.append((min(conn_verts) + 1, max(conn_verts) + 1))
    print(edges)
    edges = [(1, 2), (1, 5), (2, 3), (2, 6), (3, 4), (3, 7), (4, 5), (4, 8), (5, 6), (6, 7), (7, 8), (1, 8)]
    graph = GraphManager.find_mobius_embedding(num_vertices, edges)
    print(graph)
    print(edges)
    '''

    '''
    edges= []
    for edge in range(0, num_vertices):
        conn_verts = [edge, (edge + 1) % num_vertices]
        edges.append((min(conn_verts) + 1, max(conn_verts) + 1))
        conn_verts = [edge, (edge + num_vertices) % (num_vertices * 2)]
        edges.append((min(conn_verts) + 1, max(conn_verts) + 1))
        conn_verts = [edge, (edge + 3) % (num_vertices)]
        edges.append((min(conn_verts) + 1 + num_vertices, max(conn_verts) + 1 + num_vertices))
    # print(edges)
    # graph = GraphManager.find_mobius_embedding(num_vertices*2, edges)
    # print(graph)
    # spine = [1, 2, 3, 4, 5, 6, 7, 14, 12, 10, 8, 13, 11, 9]
    # spine = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    # print(edges)
    # graph = GraphManager.find_mobius_embedding_with_permutation(spine, edges)
    # print(graph)
    '''

    '''
    num_vertices = 8
    edges = [(1, 2)]
    for edge in range(0, num_vertices):
        conn_verts = [edge, (edge + 1) % num_vertices]
        edges.append((min(conn_verts) + 1, max(conn_verts) + 1))
        conn_verts = [edge, (edge + 4) % num_vertices]
        edges.append((min(conn_verts) + 1, max(conn_verts) + 1))
    print(edges)
    edges = [(1, 2), (1, 5), (2, 3), (2, 6), (3, 4), (3, 7), (4, 5), (4, 8), (5, 6), (6, 7), (7, 8), (1, 8)]
    graph = GraphManager.find_mobius_embedding(num_vertices, edges)
    print(graph)
    print(edges)
    '''

    perms = Permutations.get_perms_from_file(7, "flip_perms_")
    perms = Permutations.strings_to_perms(perms)
    spine = [1, 2, 3, 4, 5, 6, 7]
    edges = GraphManager.create_complete_graph_edge_set(7)
    
    from KleinGraph import KleinGraph
    genA = KleinGraph(spine, edges)
    genA.place_free_edges()
    print(genA)

    # while len(graphs) > 0:
    #     new_graphs = []
    #     for graph in graphs:
    #         if graph.is_graph_placed():
    #             return graph
    #         if not graph.is_possible_to_embedd():
    #             continue
            
    #         next_edge = graph.remainingEdges[0]
    #         avail_edges = graph.get_available_edges(next_edge)

    #         for edge in avail_edges:
    #             new_graph = graph.copy()
    #             new_graph.place_edge(edge[0][0], edge[0][1], edge[1])
    #             new_graphs.append(new_graph)
    #     graphs = new_graphs
    
    
    # graph = GraphManager.find_klein_embedding_with_permutation(spine, edges)
    # print(graph)




main()

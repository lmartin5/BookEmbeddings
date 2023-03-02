"""main.py
@author lmartin5

This file contains example runs of how the GraphManager class can be
used to search for one-page Mobius book embeddings of a graph. It also contains examples of 
looking for an embedding for one permutation.
"""

from KleinGraph import KleinGraph
from MobiusGraph import MobiusGraph
from BookEmbedding import BookEmbedding
import Permutations
import GraphManager
from copy import deepcopy
from multiprocessing import freeze_support

def main():
    # # mobius ladder
    # edges = [(1, 3), (3, 5), (5, 7), (7, 9), (2, 9), (2, 4), (4, 6), (6, 8), (8, 10), (1, 10),
    #           (1,2), (3, 4), (5, 6), (7, 8), (9, 10)]

    # # klein ladder
    # edges = [(1, 3), (3, 5), (5, 7), (7, 9), (2, 9), (2, 4), (4, 6), (6, 8), (8, 10), (1, 10),
    #         (1,2), (3, 4), (5, 6), (7, 8), (9, 10),
    #         (1,4), (3,6), (5,8), (7,10), (2,3), (4,5), (6,7), (8,9)]


    # 3n graph for klein embedding with reveresed orientations
    # edges = [(1,2), (2, 3), (3,4), (4, 5), (5, 6), (6, 7), (7, 8), 
    #     (1,3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8), 
    #     (1, 4), (2, 5), (3, 6), (4, 7), (5, 8), (1, 6), (2, 7), (3, 7), (1, 7), (2, 8), (1, 8)]

    # Permutations.generate_permutations_to_file(6)
    # perms = Permutations.get_perms_from_file(6)
    # perms = Permutations.remove_flip_elements(perms)
    # Permutations.store_permutations(perms, 6, "flip_perms_")
    perms = Permutations.get_perms_from_file(7, "flip_perms_")
    perms = Permutations.strings_to_perms(perms)

    edges = GraphManager.create_complete_graph_edge_set(7)
    graph = GraphManager.find_klein_b_embedding_threaded(edges, perms)
    print(graph)

if __name__=="__main__":
    freeze_support()
    main()

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
    #     (1,3), (2, 6), (3, 5), (4, 6), (5, 8), (6, 8), 
    #     (1, 4), (2, 7), (3, 6), (4, 7), (1, 5), (1, 6), (2, 8), (3, 7), (1, 7), (1,8), (3, 8)]

    # 3n graph for klein embedding with cylinder orientations
    # edges = [(1,2), (2, 3), (3,4), (4, 5), (5, 6), (6, 7), (7, 8), 
    #     (1,3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8), 
    #     (1, 4), (2, 5), (3, 6), (4, 7), (5, 8), (1, 6), (2, 7), (3, 7), (1, 7), (2, 8), (1, 8)]

    # Permutations.generate_permutations_to_file(10)
    # perms = Permutations.get_perms_from_file(10)
    # perms = Permutations.remove_dihedral_elements(perms)
    # Permutations.store_permutations(perms, 10, "dihedral_perms_")
    perms = Permutations.get_perms_from_file(8, "dihedral_perms_")
    perms = Permutations.strings_to_perms(perms)

    # 8 vertex klein ladder
    edges = [(1,2), (1,3), (1,4), (1,6), (1,7), (1,8), 
             (2,3), (2,4), (2,6), (2,7), (2,8),
             (3,4), (3,5), (3,6), (3,8), 
             (4,5), (4,6), (4,7), 
             (5,6), (5,7), (5,8), 
             (6,7), (6,8), (7,8)]
    
    # 10 vertex klein ladder
    # edges = [(1,2), (1,3), (1,4), (1,6), (1,9), (1,10), 
    #          (2,3), (2,4), (2,8), (2,9), (2,10),
    #          (3,4), (3,5), (3,6), (3,8), 
    #          (4,5), (4,6), (4,9), 
    #          (5,6), (5,7), (5,8), (5,10),
    #          (6,7), (6,8), (7,8), (7, 9), (7, 10),
    #          (8,9), (8, 10), (9, 10)]
    
    # graph = GraphManager.find_klein_b_embedding_with_permutation([1, 2, 3, 4, 5, 6, 7, 8], edges)
    graph = GraphManager.find_torus_embedding_threaded(edges, perms)
    print(graph)

if __name__=="__main__":
    freeze_support()
    main()

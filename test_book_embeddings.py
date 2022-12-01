"""test_book_embeddings.py
@author lmartin5
"""

import GraphManager

k_6 = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2, 5), (2, 6),
       (3, 4), (3, 5), (3, 6), (4, 5), (4, 6), (5, 6)]
k_8 = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (2, 3), (2, 4), (2, 5), (2, 6),
       (2, 7), (2, 8), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (4, 5), (4, 6), (4, 7), (4, 8),
       (5, 6), (5, 7), (5, 8), (6, 7), (6, 8), (7, 8)]
k_2_3 = [(1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)]
k_4_4 = [(1, 5), (1, 6), (1, 7), (1, 8), (2, 5), (2, 6), (2, 7), (2, 8),
         (3, 5), (3, 6), (3, 7), (3, 8), (4, 5), (4, 6), (4, 7), (4, 8)]


# note: order is received value, expected/solution
"""
First Set: Testing Graph Creation Functions from GraphManager.py
"""
def test_complete_graph():
    """Test function
    """
    received_k_6 = GraphManager.create_complete_graph_edge_set(6)
    assert_correct_edge_set(received_k_6, k_6)

    received_k_8 = GraphManager.create_complete_graph_edge_set(8)
    assert_correct_edge_set(received_k_8, k_8)

def test_complete_bipartite_graph():
    """Test function
    """
    received_k_2_3 = GraphManager.create_complete_bipartite_graph_edge_set(2, 3)
    assert_correct_edge_set(received_k_2_3, k_2_3)

    received_k_4_4 = GraphManager.create_complete_bipartite_graph_edge_set(4, 4)
    assert_correct_edge_set(received_k_4_4, k_4_4)

def assert_correct_edge_set(edge_set, solution_edge_set):
    """Test function
    Recursively defined to check tree is the same
    """
    assert len(edge_set) == len(solution_edge_set)
    for edge in solution_edge_set:
        assert edge in edge_set
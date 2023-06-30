"""BookEmbedding.py
@author lmartin5

This file contains the BookEmbedding class. It represents an n-page book embedding of a graph. 
It is used in GraphManger to see what the book thickness of a graph is, and gives the n-page book 
embedding once it finds it.
"""

import copy

class BookEmbedding():

    def __init__(self, perm, edgeSet, numPages=1):
        self.verts = len(perm)
        self.spine = perm
        self.addedEdges = []
        self.remainingEdges = edgeSet
        self.availableEdges = []
        self.numPages = numPages
        self.generate_all_possible_edges()

    def is_possible_to_embedd(self):
        possible = True
        for edge in self.remainingEdges:
            edge_avail = False
            for page_number in range(1, self.numPages + 1):
                if self.is_edge_available((edge, page_number)):
                    edge_avail = True
                    break
            if edge_avail == False:
                possible = False
                break
        return possible

    def is_graph_placed(self):
        if len(self.remainingEdges) == 0:
            return True
        else:
            return False

    def __str__(self):
        pretty_print = "Book Embedding of Graph\n"
        pretty_print += str(self.spine)
        pretty_print += "\nNumber of Vertices: " + str(self.verts)
        pretty_print += "\nGraph Embedded: " + str(self.is_graph_placed())
        pretty_print += "\nEmbedding Possibility Remaining: " + str(self.is_possible_to_embedd())
        pretty_print += "\nEdges Added: " + str(len(self.addedEdges))
        for edge in self.addedEdges:
            pretty_print += "\n\t" + str(edge)
        pretty_print += "\nRemaining Edges to Add: " + str(len(self.remainingEdges))
        for edge in self.remainingEdges:
            pretty_print += "\n\t" + str(edge)
        return pretty_print

    def place_free_edges(self):
        for k in range(0, self.verts - 1):
            i = self.spine[k]
            j = self.spine[k+1]
            if j < i:
                temp = i
                i = j
                j = temp

            if (i, j) in self.remainingEdges:
                self.addedEdges.append(((i, j), 1))
                self.remainingEdges.remove((i, j))
                self.remove_edge_from_available((i, j))

        i = self.spine[0]
        j = self.spine[-1]
        if j < i:
            temp = i
            i = j
            j = temp
        if (i, j) in self.remainingEdges:
            self.addedEdges.append(((i, j), 1))
            self.remainingEdges.remove((i, j))
            self.remove_edge_from_available((i,j))

    def generate_all_possible_edges(self):
        for pageNumber in range(1, self.numPages + 1):
            for vert in range(1, self.verts):
                for other in range(vert + 1, self.verts + 1): 
                    self.availableEdges.append(((vert, other), pageNumber))

    def remove_edge_from_available(self, removed_edge):
        new_edge_copy = self.availableEdges.copy()
        for edge in self.availableEdges:
            if edge[0] == removed_edge:
                new_edge_copy.remove(edge)
        self.availableEdges = new_edge_copy

    def remove_typed_edge(self, remove_edge):
        new_edge_copy = self.availableEdges.copy()
        removed_edge = remove_edge[0]
        edge_type = remove_edge[1]

        if removed_edge[0] > removed_edge[1]:
            print("WARNING: First vertex given larger than second")

        for edge in self.availableEdges:
            if edge[0] == removed_edge and edge[1] == edge_type:
                new_edge_copy.remove(edge)
        self.availableEdges = new_edge_copy

    def is_edge_available(self, edge):
        for avail_edge in self.availableEdges:
            if edge[0] == avail_edge[0] and edge[1] == avail_edge[1]:
                return True
        return False

    def place_edge(self, a, b, page_number):
        if page_number not in list(range(1, self.numPages + 1)):
            print("invalid page number")
            return -2
        edge = ((a, b), page_number)
        if not self.is_edge_available(edge):
            print("edge is not available")
            return -1

        self.addedEdges.append(edge)
        if edge[0] in self.remainingEdges:
            self.remainingEdges.remove(edge[0])
        self.remove_edge_from_available(edge[0])

        self.add_blocked_edges(edge)

    def add_blocked_edges(self, placed_edge):
        edge = placed_edge[0]
        page_number = placed_edge[1]

        smaller = self.spine.index(edge[0])
        larger = self.spine.index(edge[1])
        if smaller > larger:
            temp = smaller
            smaller = larger
            larger = temp

        if larger == smaller + 1:
            return

        blocked_vertices = [vert for vert in range(smaller + 1, larger)]
        for i in range(len(blocked_vertices)):
            blocked_vertices[i] = self.spine[blocked_vertices[i]]
        
        ignored_vertices = [self.spine[smaller], self.spine[larger]] + blocked_vertices
        blocked_top_vertices = [i for i in self.spine if i not in ignored_vertices]

        for block in blocked_vertices:
            for vert in blocked_top_vertices:
                if vert < block:
                    self.remove_typed_edge(((vert, block), page_number))
                else:
                    self.remove_typed_edge(((block, vert), page_number))

    def get_available_edges(self, edge):
        edges = []
        for avail_edge in self.availableEdges:
            if avail_edge[0] == edge:
                edges.append(avail_edge)
        return edges

    def copy(self):
        graph2 = copy.deepcopy(self)
        return graph2

            

    
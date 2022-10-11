"""KleinGraph.py
@author lmartin5

This file contains the KleinGraph class. It represents a one-page Klein bottle
 book embedding of a graph. It is used in GraphManger to see if a graph
is one page Klein book embeddable and gives the embedding if it is.
"""

import copy

class KleinGraph():

    def __init__(self, perm, edgeSet):
        self.verts = len(perm)
        self.top_spine = perm
        self.bottom_spine = perm[::-1]
        self.addedEdges = []
        self.remainingEdges = edgeSet
        self.availableEdges = []
        self.edge_types = ["top", "bottom", "topToBottom", "bottomToTop", "topWrap", "bottomWrap", "ttbLeft", "ttbRight", "bttLeft", "bttRight"]

        self.generate_all_possible_edges()

    def is_possible_to_embedd(self):
        possible = True
        for edge in self.remainingEdges:
            edge_avail = False
            for edge_type in self.edge_types:
                if self.is_edge_available((edge, edge_type)):
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
        pretty_print = str(self.top_spine)
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
            i = self.top_spine[k]
            j = self.top_spine[k+1]
            if j < i:
                temp = i
                i = j
                j = temp

            if (i, j) in self.remainingEdges:
                self.addedEdges.append(((i, j), "top"))
                self.remainingEdges.remove((i, j))
                self.remove_edge_from_available((i, j))

        i = self.top_spine[0]
        j = self.top_spine[self.verts - 1]
        if j < i:
            temp = i
            i = j
            j = temp
        if (i, j) in self.remainingEdges:
            self.addedEdges.append(((i, j), "topWrap"))
            self.remainingEdges.remove((i, j))
            self.remove_edge_from_available((i,j))

    def generate_all_possible_edges(self):
        for vert in range(1, self.verts):
            for other in range(vert + 1, self.verts + 1):
                self.availableEdges.append(((vert, other), "top"))
                self.availableEdges.append(((vert, other), "bottom"))
                self.availableEdges.append(((vert, other), "topToBottom"))
                self.availableEdges.append(((vert, other), "bottomToTop"))
                self.availableEdges.append(((vert, other), "topWrap"))
                self.availableEdges.append(((vert, other), "bottomWrap"))
                self.availableEdges.append(((vert, other), "ttbLeft"))
                self.availableEdges.append(((vert, other), "ttbRight"))
                self.availableEdges.append(((vert, other), "bttLeft"))
                self.availableEdges.append(((vert, other), "bttRight"))

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

    def place_edge(self, a, b, edge_type):
        if edge_type not in self.edge_types:
            print("invalid edge type")
            return -2
        edge = ((a, b), edge_type)
        if not self.is_edge_available(edge):
            print("edge is not available")
            return -1

        self.addedEdges.append(edge)
        if edge[0] in self.remainingEdges:
            self.remainingEdges.remove(edge[0])
        self.remove_edge_from_available(edge[0])

        if edge_type == "top":
            self.add_blocked_edges_top(edge)
        if edge_type == "bottom":
            self.add_blocked_edges_bottom(edge)
        if edge_type == "topToBottom":
            self.add_blocked_edges_top_to_bottom(edge)
        if edge_type == "bottomToTop":
            self.add_blocked_edges_bottom_to_top(edge)

    def add_blocked_edges_top(self, placed_edge):
        edge = placed_edge[0]

        smaller = self.top_spine.index(edge[0])
        larger = self.top_spine.index(edge[1])
        if smaller > larger:
            temp = smaller
            smaller = larger
            larger = temp
        if larger == smaller + 1:
            return

        blocked_vertices = [vert for vert in range(smaller + 1, larger)]
        for i in range(len(blocked_vertices)):
            blocked_vertices[i] = self.top_spine[blocked_vertices[i]]
        
        ignored_vertices = [self.top_spine[smaller], self.top_spine[larger]] + blocked_vertices
        blocked_top_vertices = [i for i in self.top_spine if i not in ignored_vertices]

        for block in blocked_vertices:
            for vert in blocked_top_vertices:
                if vert < block:
                    self.remove_typed_edge(((vert, block),"top"))
                else:
                    self.remove_typed_edge(((block, vert),"top"))

        for block in blocked_vertices:
            for vert in self.bottom_spine:
                if vert < block:
                    self.remove_typed_edge(((vert, block),"bottomToTop"))
                else:
                    self.remove_typed_edge(((block, vert),"topToBottom"))

    def add_blocked_edges_bottom(self, placed_edge):
        edge = placed_edge[0]

        smaller = self.bottom_spine.index(edge[0])
        larger = self.bottom_spine.index(edge[1])
        if smaller > larger:
            temp = smaller
            smaller = larger
            larger = temp
        if larger == smaller + 1:
            return

        blocked_vertices = [vert for vert in range(smaller + 1, larger)]
        for i in range(len(blocked_vertices)):
            blocked_vertices[i] = self.bottom_spine[blocked_vertices[i]]
        
        ignored_vertices = [self.bottom_spine[smaller], self.bottom_spine[larger]] + blocked_vertices
        blocked_bottom_vertices = [i for i in self.bottom_spine if i not in ignored_vertices]

        for block in blocked_vertices:
            for vert in blocked_bottom_vertices:
                if vert < block:
                    self.remove_typed_edge(((vert, block),"bottom"))
                else:
                    self.remove_typed_edge(((block, vert),"bottom"))

        for block in blocked_vertices:
            for vert in self.bottom_spine:
                if vert < block:
                    self.remove_typed_edge(((vert, block),"topToBottom"))
                else:
                    self.remove_typed_edge(((block, vert),"bottomToTop"))

    def add_blocked_edges_top_to_bottom(self, placed_edge):
        edge = placed_edge[0]
        smaller = self.top_spine.index(edge[0])
        larger = self.bottom_spine.index(edge[1])
        
        top_left_blocked = [self.top_spine[i] for i in range(0, smaller)]
        bottom_left_blocked = [self.bottom_spine[i] for i in range(0, larger)]
        top_right_blocked = [self.top_spine[i] for i in range(smaller + 1, self.verts)]
        bottom_right_blocked = [self.bottom_spine[i] for i in range(larger + 1, self.verts)]

        for top_left in top_left_blocked:
            for top_right in top_right_blocked:
                if top_left < top_right:
                    self.remove_typed_edge(((top_left, top_right), "top"))
                else:
                    self.remove_typed_edge(((top_right, top_left), "top"))

        for bottom_left in bottom_left_blocked:
            for bottom_right in bottom_right_blocked:
                if bottom_left < bottom_right:
                    self.remove_typed_edge(((bottom_left, bottom_right), "bottom"))
                else:
                    self.remove_typed_edge(((bottom_right, bottom_left), "bottom"))

        for top_left in top_left_blocked:
            for bottom_right in bottom_right_blocked:
                if top_left < bottom_right:
                    self.remove_typed_edge(((top_left, bottom_right), "topToBottom"))
                else:
                    self.remove_typed_edge(((bottom_right, top_left), "bottomToTop"))

        for bottom_left in bottom_left_blocked:
            for top_right in top_right_blocked:
                if bottom_left < top_right:
                    self.remove_typed_edge(((bottom_left, top_right), "bottomToTop"))
                else:
                    self.remove_typed_edge(((top_right, bottom_left), "topToBottom"))

    def add_blocked_edges_bottom_to_top(self, placed_edge):
        edge = placed_edge[0]
        smaller = self.bottom_spine.index(edge[0])
        larger = self.top_spine.index(edge[1])
        
        top_left_blocked = [self.top_spine[i] for i in range(0, larger)]
        bottom_left_blocked = [self.bottom_spine[i] for i in range(0, smaller)]
        top_right_blocked = [self.top_spine[i] for i in range(larger + 1, self.verts)]
        bottom_right_blocked = [self.bottom_spine[i] for i in range(smaller + 1, self.verts)]

        for top_left in top_left_blocked:
            for top_right in top_right_blocked:
                if top_left < top_right:
                    self.remove_typed_edge(((top_left, top_right), "top"))
                else:
                    self.remove_typed_edge(((top_right, top_left), "top"))

        for bottom_left in bottom_left_blocked:
            for bottom_right in bottom_right_blocked:
                if bottom_left < bottom_right:
                    self.remove_typed_edge(((bottom_left, bottom_right), "bottom"))
                else:
                    self.remove_typed_edge(((bottom_right, bottom_left), "bottom"))

        for top_left in top_left_blocked:
            for bottom_right in bottom_right_blocked:
                if top_left < bottom_right:
                    self.remove_typed_edge(((top_left, bottom_right), "topToBottom"))
                else:
                    self.remove_typed_edge(((bottom_right, top_left), "bottomToTop"))

        for bottom_left in bottom_left_blocked:
            for top_right in top_right_blocked:
                if bottom_left < top_right:
                    self.remove_typed_edge(((bottom_left, top_right), "bottomToTop"))
                else:
                    self.remove_typed_edge(((top_right, bottom_left), "topToBottom"))

    def get_available_edges(self, edge):
        edges = []
        for avail_edge in self.availableEdges:
            if avail_edge[0] == edge:
                edges.append(avail_edge)
        return edges

    def copy(self):
        graph2 = copy.deepcopy(self)
        return graph2

            

    
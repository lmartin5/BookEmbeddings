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
                for edgeType in self.edge_types:
                    self.availableEdges.append(((vert, other), edgeType))

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
        if edge_type == "topWrap":
            self.add_blocked_edges_top_wrap(edge)
        if edge_type == "bottomWrap":
            self.add_blocked_edges_bottom_wrap(edge)
        if edge_type == "ttbLeft":
            print("ttbLeft edge")
        if edge_type == "ttbRight":
            print("ttbRight edge")
        if edge_type == "bttLeft":
            print("bttLeft edge")
        if edge_type == "bttRight":
            print("bttRight edge")

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
            # removing top edges
            for vert in blocked_top_vertices:
                if vert < block:
                    self.remove_typed_edge(((vert, block),"top"))
                else:
                    self.remove_typed_edge(((block, vert),"top"))
            
            # removing bottom to top, top to bottom, and top wrap edges
            for vert in self.bottom_spine:
                if vert < block:
                    self.remove_typed_edge(((vert, block),"topWrap"))
                    self.remove_typed_edge(((vert, block),"bottomToTop"))
                    self.remove_typed_edge(((vert, block),"bttRight"))
                    self.remove_typed_edge(((vert, block),"bttLeft"))
                else:
                    self.remove_typed_edge(((block, vert),"topWrap"))
                    self.remove_typed_edge(((block, vert),"topToBottom"))
                    self.remove_typed_edge(((block, vert),"ttbRight"))
                    self.remove_typed_edge(((block, vert),"ttbLeft"))


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
            # removing bottom edges
            for vert in blocked_bottom_vertices:
                if vert < block:
                    self.remove_typed_edge(((vert, block),"bottom"))
                else:
                    self.remove_typed_edge(((block, vert),"bottom"))

            # removing bottom to top, top to bottom, and wrap edges
            for vert in self.bottom_spine:
                if vert < block:
                    self.remove_typed_edge(((vert, block),"bottomWrap"))
                    self.remove_typed_edge(((vert, block),"topToBottom"))
                    self.remove_typed_edge(((vert, block),"ttbLeft"))
                    self.remove_typed_edge(((vert, block),"ttbRight"))
                else:
                    self.remove_typed_edge(((block, vert),"bottomWrap"))
                    self.remove_typed_edge(((block, vert),"bottomToTop"))
                    self.remove_typed_edge(((block, vert),"bttLeft"))
                    self.remove_typed_edge(((block, vert),"bttRight"))

    def add_blocked_edges_top_to_bottom(self, placed_edge):
        edge = placed_edge[0]
        smaller = self.top_spine.index(edge[0])
        larger = self.bottom_spine.index(edge[1])
        
        top_left_blocked = [self.top_spine[i] for i in range(0, smaller)]
        bottom_left_blocked = [self.bottom_spine[i] for i in range(0, larger)]
        top_right_blocked = [self.top_spine[i] for i in range(smaller + 1, self.verts)]
        bottom_right_blocked = [self.bottom_spine[i] for i in range(larger + 1, self.verts)]

        # removing regular top edges
        for top_left in top_left_blocked:
            for top_right in top_right_blocked:
                if top_left < top_right:
                    self.remove_typed_edge(((top_left, top_right), "top"))
                else:
                    self.remove_typed_edge(((top_right, top_left), "top"))
        # removing top wrap edges
        for top_left in top_left_blocked:
            top_left_copy = top_left_blocked.copy()
            top_left_copy.remove(top_left)
            for top_left_2 in top_left_copy:
                if top_left < top_left_2:
                    self.remove_typed_edge(((top_left, top_left_2), "topWrap"))
                else:
                    self.remove_typed_edge(((top_left_2, top_left), "topWrap"))
        for top_right in top_right_blocked:
            top_right_copy = top_right_blocked.copy()
            top_right_copy.remove(top_right)
            for top_right_2 in top_right_copy:
                if top_right < top_right_2:
                    self.remove_typed_edge(((top_right, top_right_2), "topWrap"))
                else:
                    self.remove_typed_edge(((top_right_2, top_right), "topWrap"))

        # removing regular bottom edges
        for bottom_left in bottom_left_blocked:
            for bottom_right in bottom_right_blocked:
                if bottom_left < bottom_right:
                    self.remove_typed_edge(((bottom_left, bottom_right), "bottom"))
                else:
                    self.remove_typed_edge(((bottom_right, bottom_left), "bottom"))
        # removing bottom wrap edges
        for bottom_left in bottom_left_blocked:
            bottom_left_copy = bottom_left_blocked.copy()
            bottom_left_copy.remove(bottom_left)
            for bottom_left_2 in bottom_left_copy:
                if bottom_left < bottom_left_2:
                    self.remove_typed_edge(((bottom_left, bottom_left_2), "bottomWrap"))
                else:
                    self.remove_typed_edge(((bottom_left_2, bottom_left), "bottomWrap"))
        for bottom_right in bottom_right_blocked:
            bottom_right_copy = bottom_right_blocked.copy()
            bottom_right_copy.remove(bottom_right)
            for bottom_right_2 in bottom_right_copy:
                if bottom_right < bottom_right_2:
                    self.remove_typed_edge(((bottom_right, bottom_right_2), "bottomWrap"))
                else:
                    self.remove_typed_edge(((bottom_right_2, bottom_right), "bottomWrap"))

        # removing top to bottom and bottom to top edges
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

        # removing wrapping top to bottom and bottom to top edges
        for top_left in top_left_blocked:
            for vert in self.bottom_spine:
                if top_left < vert:
                    self.remove_typed_edge(((top_left, vert), "ttbRight"))
                else:
                    self.remove_typed_edge(((vert, top_left), "bttLeft"))
        for bottom_left in bottom_left_blocked:
            for vert in self.top_spine:
                if bottom_left < vert:
                    self.remove_typed_edge(((bottom_left, vert), "bttRight"))
                else:
                    self.remove_typed_edge(((vert, bottom_left), "ttbLeft"))
        for top_right in top_right_blocked:
            for vert in self.bottom_spine:
                if top_right < vert:
                    self.remove_typed_edge(((top_right, vert), "ttbLeft"))
                else:
                    self.remove_typed_edge(((vert, top_right), "bttRight"))
        for bottom_right in bottom_right_blocked:
            for vert in self.top_spine:
                if bottom_right < vert:
                    self.remove_typed_edge(((bottom_right, vert), "bttLeft"))
                else:
                    self.remove_typed_edge(((vert, bottom_right), "ttbRight"))

    def add_blocked_edges_bottom_to_top(self, placed_edge):
        edge = placed_edge[0]
        smaller = self.bottom_spine.index(edge[0])
        larger = self.top_spine.index(edge[1])
        
        top_left_blocked = [self.top_spine[i] for i in range(0, larger)]
        bottom_left_blocked = [self.bottom_spine[i] for i in range(0, smaller)]
        top_right_blocked = [self.top_spine[i] for i in range(larger + 1, self.verts)]
        bottom_right_blocked = [self.bottom_spine[i] for i in range(smaller + 1, self.verts)]

        # removing regular top edges
        for top_left in top_left_blocked:
            for top_right in top_right_blocked:
                if top_left < top_right:
                    self.remove_typed_edge(((top_left, top_right), "top"))
                else:
                    self.remove_typed_edge(((top_right, top_left), "top"))
        # removing top wrap edges
        for top_left in top_left_blocked:
            top_left_copy = top_left_blocked.copy()
            top_left_copy.remove(top_left)
            for top_left_2 in top_left_copy:
                if top_left < top_left_2:
                    self.remove_typed_edge(((top_left, top_left_2), "topWrap"))
                else:
                    self.remove_typed_edge(((top_left_2, top_left), "topWrap"))
        for top_right in top_right_blocked:
            top_right_copy = top_right_blocked.copy()
            top_right_copy.remove(top_right)
            for top_right_2 in top_right_copy:
                if top_right < top_right_2:
                    self.remove_typed_edge(((top_right, top_right_2), "topWrap"))
                else:
                    self.remove_typed_edge(((top_right_2, top_right), "topWrap"))

        # removing regular bottom edges
        for bottom_left in bottom_left_blocked:
            for bottom_right in bottom_right_blocked:
                if bottom_left < bottom_right:
                    self.remove_typed_edge(((bottom_left, bottom_right), "bottom"))
                else:
                    self.remove_typed_edge(((bottom_right, bottom_left), "bottom"))
        # removing bottom wrap edges
        for bottom_left in bottom_left_blocked:
            bottom_left_copy = bottom_left_blocked.copy()
            bottom_left_copy.remove(bottom_left)
            for bottom_left_2 in bottom_left_copy:
                if bottom_left < bottom_left_2:
                    self.remove_typed_edge(((bottom_left, bottom_left_2), "bottomWrap"))
                else:
                    self.remove_typed_edge(((bottom_left_2, bottom_left), "bottomWrap"))
        for bottom_right in bottom_right_blocked:
            bottom_right_copy = bottom_right_blocked.copy()
            bottom_right_copy.remove(bottom_right)
            for bottom_right_2 in bottom_right_copy:
                if bottom_right < bottom_right_2:
                    self.remove_typed_edge(((bottom_right, bottom_right_2), "bottomWrap"))
                else:
                    self.remove_typed_edge(((bottom_right_2, bottom_right), "bottomWrap"))

        # removing top to bottom and bottom to top edges
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

        # removing wrapping top to bottom and bottom to top edges
        for top_left in top_left_blocked:
            for vert in self.bottom_spine:
                if top_left < vert:
                    self.remove_typed_edge(((top_left, vert), "ttbRight"))
                else:
                    self.remove_typed_edge(((vert, top_left), "bttLeft"))
        for bottom_left in bottom_left_blocked:
            for vert in self.top_spine:
                if bottom_left < vert:
                    self.remove_typed_edge(((bottom_left, vert), "bttRight"))
                else:
                    self.remove_typed_edge(((vert, bottom_left), "ttbLeft"))
        for top_right in top_right_blocked:
            for vert in self.bottom_spine:
                if top_right < vert:
                    self.remove_typed_edge(((top_right, vert), "ttbLeft"))
                else:
                    self.remove_typed_edge(((vert, top_right), "bttRight"))
        for bottom_right in bottom_right_blocked:
            for vert in self.top_spine:
                if bottom_right < vert:
                    self.remove_typed_edge(((bottom_right, vert), "bttLeft"))
                else:
                    self.remove_typed_edge(((vert, bottom_right), "ttbRight"))

    def add_blocked_edges_top_wrap(self, placed_edge):
        edge = placed_edge[0]

        smaller = self.top_spine.index(edge[0])
        larger = self.top_spine.index(edge[1])
        if smaller > larger:
            temp = smaller
            smaller = larger
            larger = temp
        if smaller == 0 and larger == self.verts - 1:
            print("Attempting to place a free edge")
            return

        left_blocked_vertices = [vert for vert in range(0, smaller)]
        right_blocked_vertices = [vert for vert in range(larger + 1, self.verts)]
        for i in range(len(left_blocked_vertices)):
            left_blocked_vertices[i] = self.top_spine[left_blocked_vertices[i]]
        for i in range(len(right_blocked_vertices)):
            right_blocked_vertices[i] = self.top_spine[right_blocked_vertices[i]]
        
        blocked_vertices = [self.top_spine[smaller], self.top_spine[larger]] + left_blocked_vertices + right_blocked_vertices
        unblocked_vertices = [i for i in self.top_spine if i not in blocked_vertices]

        for block in left_blocked_vertices:
            # removing top edges
            for vert in unblocked_vertices + right_blocked_vertices + [self.top_spine[larger]]:
                if vert < block:
                    self.remove_typed_edge(((vert, block),"top"))
                else:
                    self.remove_typed_edge(((block, vert),"top"))
            # removing wrapping to unblocked middle verts
            for vert in [self.top_spine[smaller]] + unblocked_vertices:
                if vert < block:
                    self.remove_typed_edge(((vert, block),"topWrap"))
                else:
                    self.remove_typed_edge(((block, vert),"topWrap"))
            # removing wrapping to other left blocked verts
            left_blocked_copy = left_blocked_vertices.copy()
            left_blocked_copy.remove(block)
            for left_2 in left_blocked_copy:
                if block < left_2:
                    self.remove_typed_edge(((block, left_2),"topWrap"))
                else:
                    self.remove_typed_edge(((left_2, block),"topWrap"))
            # removing bottom to top and top to bottom edges
            for vert in self.bottom_spine:
                if vert < block:
                    self.remove_typed_edge(((vert, block),"bottomToTop"))
                    self.remove_typed_edge(((vert, block),"bttRight"))
                    self.remove_typed_edge(((vert, block),"bttLeft"))
                else:
                    self.remove_typed_edge(((block, vert),"topToBottom"))
                    self.remove_typed_edge(((block, vert),"ttbRight"))
                    self.remove_typed_edge(((block, vert),"ttbLeft"))

        for block in right_blocked_vertices:
            # removing top edges
            for vert in unblocked_vertices + left_blocked_vertices + [self.top_spine[smaller]]:
                if vert < block:
                    self.remove_typed_edge(((vert, block),"top"))
                else:
                    self.remove_typed_edge(((block, vert),"top"))
            # removing wrapping to unblocked middle verts
            for vert in [self.top_spine[larger]] + unblocked_vertices:
                if vert < block:
                    self.remove_typed_edge(((vert, block),"topWrap"))
                else:
                    self.remove_typed_edge(((block, vert),"topWrap"))
            # removing wrapping to other right blocked verts
            right_blocked_copy = right_blocked_vertices.copy()
            right_blocked_copy.remove(block)
            for right_2 in right_blocked_copy:
                if block < right_2:
                    self.remove_typed_edge(((block, right_2),"topWrap"))
                else:
                    self.remove_typed_edge(((right_2, block),"topWrap"))
            # removing bottom to top and top to bottom edges
            for vert in self.bottom_spine:
                if vert < block:
                    self.remove_typed_edge(((vert, block),"bottomToTop"))
                    self.remove_typed_edge(((vert, block),"bttRight"))
                    self.remove_typed_edge(((vert, block),"bttLeft"))
                else:
                    self.remove_typed_edge(((block, vert),"topToBottom"))
                    self.remove_typed_edge(((block, vert),"ttbRight"))
                    self.remove_typed_edge(((block, vert),"ttbLeft"))

    def add_blocked_edges_bottom_wrap(self, placed_edge):
        edge = placed_edge[0]

        smaller = self.bottom_spine.index(edge[0])
        larger = self.bottom_spine.index(edge[1])
        if smaller > larger:
            temp = smaller
            smaller = larger
            larger = temp
        if smaller == 0 and larger == self.verts - 1:
            print("Attempting to place a free edge")
            return

        left_blocked_vertices = [vert for vert in range(0, smaller)]
        right_blocked_vertices = [vert for vert in range(larger + 1, self.verts)]
        for i in range(len(left_blocked_vertices)):
            left_blocked_vertices[i] = self.bottom_spine[left_blocked_vertices[i]]
        for i in range(len(right_blocked_vertices)):
            right_blocked_vertices[i] = self.bottom_spine[right_blocked_vertices[i]]
        
        blocked_vertices = [self.bottom_spine[smaller], self.bottom_spine[larger]] + left_blocked_vertices + right_blocked_vertices
        unblocked_vertices = [i for i in self.bottom_spine if i not in blocked_vertices]

        for block in left_blocked_vertices:
            # removing bottom edges
            for vert in unblocked_vertices + right_blocked_vertices + [self.bottom_spine[larger]]:
                if vert < block:
                    self.remove_typed_edge(((vert, block),"bottom"))
                else:
                    self.remove_typed_edge(((block, vert),"bottom"))
            # removing wrapping to unblocked middle verts
            for vert in [self.bottom_spine[smaller]] + unblocked_vertices:
                if vert < block:
                    self.remove_typed_edge(((vert, block),"bottomWrap"))
                else:
                    self.remove_typed_edge(((block, vert),"bottomWrap"))
            # removing wrapping to other left blocked verts
            left_blocked_copy = left_blocked_vertices.copy()
            left_blocked_copy.remove(block)
            for left_2 in left_blocked_copy:
                if block < left_2:
                    self.remove_typed_edge(((block, left_2),"bottomWrap"))
                else:
                    self.remove_typed_edge(((left_2, block),"bottomWrap"))
            # removing top to bottom and top to bottom edges
            for vert in self.top_spine:
                if vert < block:
                    self.remove_typed_edge(((vert, block),"topToBottom"))
                    self.remove_typed_edge(((vert, block),"ttbRight"))
                    self.remove_typed_edge(((vert, block),"ttbLeft"))
                else:
                    self.remove_typed_edge(((block, vert),"bottomToTop"))
                    self.remove_typed_edge(((block, vert),"bttRight"))
                    self.remove_typed_edge(((block, vert),"bttLeft"))

        for block in right_blocked_vertices:
            # removing bottom edges
            for vert in unblocked_vertices + left_blocked_vertices + [self.bottom_spine[smaller]]:
                if vert < block:
                    self.remove_typed_edge(((vert, block),"bottom"))
                else:
                    self.remove_typed_edge(((block, vert),"bottom"))
            # removing wrapping to unblocked middle verts
            for vert in [self.bottom_spine[larger]] + unblocked_vertices:
                if vert < block:
                    self.remove_typed_edge(((vert, block),"bottomWrap"))
                else:
                    self.remove_typed_edge(((block, vert),"bottomWrap"))
            # removing wrapping to other right blocked verts
            right_blocked_copy = right_blocked_vertices.copy()
            right_blocked_copy.remove(block)
            for right_2 in right_blocked_copy:
                if block < right_2:
                    self.remove_typed_edge(((block, right_2),"bottomWrap"))
                else:
                    self.remove_typed_edge(((right_2, block),"bottomWrap"))
            # removing bottom to top and top to bottom edges
            for vert in self.bottom_spine:
                if vert < block:
                    self.remove_typed_edge(((vert, block),"bottomToTop"))
                    self.remove_typed_edge(((vert, block),"bttRight"))
                    self.remove_typed_edge(((vert, block),"bttLeft"))
                else:
                    self.remove_typed_edge(((block, vert),"topToBottom"))
                    self.remove_typed_edge(((block, vert),"ttbRight"))
                    self.remove_typed_edge(((block, vert),"ttbLeft"))

    def get_available_edges(self, edge):
        edges = []
        for avail_edge in self.availableEdges:
            if avail_edge[0] == edge:
                edges.append(avail_edge)
        return edges

    def copy(self):
        graph2 = copy.deepcopy(self)
        return graph2

            
import Permutations
import GraphManager

perms = Permutations.get_perms_from_file(7, "flip_perms_")
perms = Permutations.strings_to_perms(perms)
spine = [1, 2, 3, 4, 5, 6, 7]

edges = GraphManager.create_complete_graph_edge_set(7)
# edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (1, 7), (3,5), (2, 5), (2, 4), (3, 6)]

graph = KleinGraph(spine, edges)
graph.place_free_edges()
print(graph)
# print(graph.availableEdges)
# print(graph.remainingEdges)
graph.place_edge(3, 5, "top")
graph.place_edge(2, 6, "topWrap")
graph.place_edge(2, 4, "topToBottom")
graph.place_edge(4, 6, "bottomToTop")
graph.place_edge(1, 5, "bottomWrap")
graph.place_edge(1, 3, "bottom")
print(graph)
ed = graph.availableEdges
for e in ed:
    print(e)
print(graph.remainingEdges)
print(graph.get_available_edges((1,6)))
print(graph.get_available_edges((5,7)))
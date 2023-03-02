"""KleinGraph.py
@author lmartin5

This file contains the KleinGraph class. It represents a one-page Klein bottle
 book embedding of a graph. It is used in GraphManger to see if a graph
is one page Klein book embeddable and gives the embedding if it is.
"""

import copy

class KleinGraphB():

    def __init__(self, perm, edgeSet):
        self.verts = len(perm)
        self.top_spine = perm
        self.bottom_spine = perm.copy()
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
        if (i < j) and (i, j) in self.remainingEdges:
            self.addedEdges.append(((i, j), "ttbLeft"))
            self.remainingEdges.remove((i, j))
            self.remove_edge_from_available((i,j))
        elif (j < i) and (j, i) in self.remainingEdges:
            self.addedEdges.append(((j, i), "bttRight"))
            self.remainingEdges.remove((j, i))
            self.remove_edge_from_available((j,i))

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
            self.add_blocked_edges_ttb_left(edge)
        if edge_type == "ttbRight":
            self.add_blocked_edges_ttb_right(edge)
        if edge_type == "bttLeft":
            self.add_blocked_edges_btt_left(edge)
        if edge_type == "bttRight":
            self.add_blocked_edges_btt_right(edge)

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

        left_blocked_vertices = [self.top_spine[vert] for vert in range(0, smaller)]
        right_blocked_vertices = [self.top_spine[vert] for vert in range(larger + 1, self.verts)]
        
        blocked_vertices = [self.top_spine[smaller], self.top_spine[larger]] + left_blocked_vertices + right_blocked_vertices
        unblocked_vertices = [i for i in self.top_spine if i not in blocked_vertices]

        for vert_a in unblocked_vertices:
            unblocked_copy = unblocked_vertices.copy()
            unblocked_copy.remove(vert_a)
            for vert_b in unblocked_copy:
                if vert_a < vert_b:
                    self.remove_typed_edge(((vert_a, vert_b),"topWrap"))
                else:
                    self.remove_typed_edge(((vert_b, vert_a),"topWrap"))

        for vert_a in self.bottom_spine:
            bottom_spine_copy = self.bottom_spine.copy()
            bottom_spine_copy.remove(vert_a)
            for vert_b in bottom_spine_copy:
                if vert_a < vert_b:
                    self.remove_typed_edge(((vert_a, vert_b),"bottomWrap"))
                else:
                    self.remove_typed_edge(((vert_b, vert_a),"bottomWrap"))
            for vert_b in unblocked_vertices + [self.top_spine[larger]] + right_blocked_vertices:
                if vert_a < vert_b:
                    self.remove_typed_edge(((vert_a, vert_b),"bttRight"))
                else:
                    self.remove_typed_edge(((vert_b, vert_a),"ttbLeft"))
            for vert_b in unblocked_vertices + [self.top_spine[smaller]] + left_blocked_vertices:
                if vert_a < vert_b:
                    self.remove_typed_edge(((vert_a, vert_b),"bttLeft"))
                else:
                    self.remove_typed_edge(((vert_b, vert_a),"ttbRight"))
            for vert_b in left_blocked_vertices + right_blocked_vertices:
                if vert_a < vert_b:
                    self.remove_typed_edge(((vert_a, vert_b),"bottomToTop"))
                else:
                    self.remove_typed_edge(((vert_b, vert_a),"topToBottom"))

        for vert_a in left_blocked_vertices:
            left_blocked_copy = left_blocked_vertices.copy()
            left_blocked_copy.remove(vert_a)

            for vert_b in unblocked_vertices + [self.top_spine[larger]] + right_blocked_vertices:
                if vert_a < vert_b:
                    self.remove_typed_edge(((vert_a, vert_b),"top"))
                else:
                    self.remove_typed_edge(((vert_b, vert_a),"top"))
            for vert_b in left_blocked_copy + right_blocked_vertices:
                if vert_a < vert_b:
                    self.remove_typed_edge(((vert_a, vert_b),"topWrap"))
                else:
                    self.remove_typed_edge(((vert_b, vert_a),"topWrap"))

        for vert_a in right_blocked_vertices:
            right_blocked_copy = right_blocked_vertices.copy()
            right_blocked_copy.remove(vert_a)

            for vert_b in unblocked_vertices + [self.top_spine[smaller]] + left_blocked_vertices:
                if vert_a < vert_b:
                    self.remove_typed_edge(((vert_a, vert_b),"top"))
                else:
                    self.remove_typed_edge(((vert_b, vert_a),"top"))
            for vert_b in right_blocked_copy + left_blocked_vertices:
                if vert_a < vert_b:
                    self.remove_typed_edge(((vert_a, vert_b),"topWrap"))
                else:
                    self.remove_typed_edge(((vert_b, vert_a),"topWrap"))


    def add_blocked_edges_bottom_wrap(self, placed_edge):
        edge = placed_edge[0]

        smaller = self.bottom_spine.index(edge[0])
        larger = self.bottom_spine.index(edge[1])
        if smaller > larger:
            temp = smaller
            smaller = larger
            larger = temp

        left_blocked_vertices = [self.bottom_spine[vert] for vert in range(0, smaller)]
        right_blocked_vertices = [self.bottom_spine[vert] for vert in range(larger + 1, self.verts)]
        
        blocked_vertices = [self.bottom_spine[smaller], self.top_spine[larger]] + left_blocked_vertices + right_blocked_vertices
        unblocked_vertices = [i for i in self.bottom_spine if i not in blocked_vertices]

        for vert_a in unblocked_vertices:
            unblocked_copy = unblocked_vertices.copy()
            unblocked_copy.remove(vert_a)
            for vert_b in unblocked_copy:
                if vert_a < vert_b:
                    self.remove_typed_edge(((vert_a, vert_b),"bottomWrap"))
                else:
                    self.remove_typed_edge(((vert_b, vert_a),"bottomWrap"))

        for vert_a in self.top_spine:
            top_spine_copy = self.top_spine.copy()
            top_spine_copy.remove(vert_a)
            for vert_b in top_spine_copy:
                if vert_a < vert_b:
                    self.remove_typed_edge(((vert_a, vert_b),"topWrap"))
                else:
                    self.remove_typed_edge(((vert_b, vert_a),"topWrap"))
            for vert_b in unblocked_vertices + [self.bottom_spine[larger]] + right_blocked_vertices:
                if vert_a < vert_b:
                    self.remove_typed_edge(((vert_a, vert_b),"ttbRight"))
                else:
                    self.remove_typed_edge(((vert_b, vert_a),"bttLeft"))
            for vert_b in unblocked_vertices + [self.bottom_spine[smaller]] + left_blocked_vertices:
                if vert_a < vert_b:
                    self.remove_typed_edge(((vert_a, vert_b),"ttbLeft"))
                else:
                    self.remove_typed_edge(((vert_b, vert_a),"bttRight"))
            for vert_b in left_blocked_vertices + right_blocked_vertices:
                if vert_a < vert_b:
                    self.remove_typed_edge(((vert_a, vert_b),"topToBottom"))
                else:
                    self.remove_typed_edge(((vert_b, vert_a),"bottomToTop"))

        for vert_a in left_blocked_vertices:
            left_blocked_copy = left_blocked_vertices.copy()
            left_blocked_copy.remove(vert_a)

            for vert_b in unblocked_vertices + [self.bottom_spine[larger]] + right_blocked_vertices:
                if vert_a < vert_b:
                    self.remove_typed_edge(((vert_a, vert_b),"bottom"))
                else:
                    self.remove_typed_edge(((vert_b, vert_a),"bottom"))
            for vert_b in left_blocked_copy + right_blocked_vertices:
                if vert_a < vert_b:
                    self.remove_typed_edge(((vert_a, vert_b),"bottomWrap"))
                else:
                    self.remove_typed_edge(((vert_b, vert_a),"bottomWrap"))

        for vert_a in right_blocked_vertices:
            right_blocked_copy = right_blocked_vertices.copy()
            right_blocked_copy.remove(vert_a)

            for vert_b in unblocked_vertices + [self.bottom_spine[smaller]] + left_blocked_vertices:
                if vert_a < vert_b:
                    self.remove_typed_edge(((vert_a, vert_b),"bottom"))
                else:
                    self.remove_typed_edge(((vert_b, vert_a),"bottom"))
            for vert_b in right_blocked_copy + left_blocked_vertices:
                if vert_a < vert_b:
                    self.remove_typed_edge(((vert_a, vert_b),"bottomWrap"))
                else:
                    self.remove_typed_edge(((vert_b, vert_a),"bottomWrap"))

    def add_blocked_edges_ttb_left(self, placed_edge):
        edge = placed_edge[0]
        smaller = self.top_spine.index(edge[0])
        larger = self.bottom_spine.index(edge[1])
        
        top_left_blocked = [self.top_spine[i] for i in range(0, smaller)]
        bottom_right_blocked = [self.bottom_spine[i] for i in range(larger + 1, self.verts)]

        for top_left in top_left_blocked:
            for vert in self.top_spine:
                if top_left < vert:
                    self.remove_typed_edge(((top_left, vert), "topWrap"))
                else:
                    self.remove_typed_edge(((vert, top_left), "topWrap"))
            for vert in [self.top_spine[i] for i in range(smaller + 1, self.verts)]:
                if top_left < vert:
                    self.remove_typed_edge(((top_left, vert), "top"))
                else:
                    self.remove_typed_edge(((vert, top_left), "top"))
            for vert in self.bottom_spine:
                if top_left < vert:
                    self.remove_typed_edge(((top_left, vert), "topToBottom"))
                    self.remove_typed_edge(((top_left, vert), "ttbRight"))
                else:
                    self.remove_typed_edge(((vert, top_left), "bottomToTop"))
                    self.remove_typed_edge(((vert, top_left), "bttLeft"))
            # wrapping prevents this
            for vert in [self.bottom_spine[i] for i in range(0, larger)]:
                if top_left < vert:
                    self.remove_typed_edge(((top_left, vert), "ttbLeft"))
                else:
                    self.remove_typed_edge(((vert, top_left), "bttRight"))

        for bottom_right in bottom_right_blocked:
            for vert in self.bottom_spine:
                if bottom_right < vert:
                    self.remove_typed_edge(((bottom_right, vert), "bottomWrap"))
                else:
                    self.remove_typed_edge(((vert, bottom_right), "bottomWrap"))
            for vert in [self.bottom_spine[i] for i in range(0, larger)]:
                if bottom_right < vert:
                    self.remove_typed_edge(((bottom_right, vert), "bottom"))
                else:
                    self.remove_typed_edge(((vert, bottom_right), "bottom"))
            for vert in self.top_spine:
                if bottom_right < vert:
                    self.remove_typed_edge(((bottom_right, vert), "bottomToTop"))
                    self.remove_typed_edge(((bottom_right, vert), "bttLeft"))
                else:
                    self.remove_typed_edge(((vert, bottom_right), "topToBottom"))
                    self.remove_typed_edge(((vert, bottom_right), "ttbRight"))
            # wrapping prevents this
            for vert in [self.top_spine[i] for i in range(smaller + 1, self.verts)]:
                if bottom_right < vert:
                    self.remove_typed_edge(((bottom_right, vert), "bttRight"))
                else:
                    self.remove_typed_edge(((vert, bottom_right), "ttbLeft"))


    def add_blocked_edges_ttb_right(self, placed_edge):
        edge = placed_edge[0]
        smaller = self.top_spine.index(edge[0])
        larger = self.bottom_spine.index(edge[1])
        
        top_right_blocked = [self.top_spine[i] for i in range(smaller + 1, self.verts)]
        bottom_left_blocked = [self.bottom_spine[i] for i in range(0, larger)]


        for top_right in top_right_blocked:
            for vert in self.top_spine:
                if top_right < vert:
                    self.remove_typed_edge(((top_right, vert), "topWrap"))
                else:
                    self.remove_typed_edge(((vert, top_right), "topWrap"))
            for vert in [self.top_spine[i] for i in range(0, smaller)]:
                if top_right < vert:
                    self.remove_typed_edge(((top_right, vert), "top"))
                else:
                    self.remove_typed_edge(((vert, top_right), "top"))
            for vert in self.bottom_spine:
                if top_right < vert:
                    self.remove_typed_edge(((top_right, vert), "topToBottom"))
                    self.remove_typed_edge(((top_right, vert), "ttbLeft"))
                else:
                    self.remove_typed_edge(((vert, top_right), "bottomToTop"))
                    self.remove_typed_edge(((vert, top_right), "bttRight"))
            # wrapping prevents this
            for vert in [self.bottom_spine[i] for i in range(larger + 1, self.verts)]:
                if top_right < vert:
                    self.remove_typed_edge(((top_right, vert), "ttbRight"))
                else:
                    self.remove_typed_edge(((vert, top_right), "bttLeft"))

        for bottom_left in bottom_left_blocked:
            for vert in self.bottom_spine:
                if bottom_left < vert:
                    self.remove_typed_edge(((bottom_left, vert), "bottomWrap"))
                else:
                    self.remove_typed_edge(((vert, bottom_left), "bottomWrap"))
            for vert in [self.bottom_spine[i] for i in range(larger + 1, self.verts)]:
                if bottom_left < vert:
                    self.remove_typed_edge(((bottom_left, vert), "bottom"))
                else:
                    self.remove_typed_edge(((vert, bottom_left), "bottom"))
            for vert in self.top_spine:
                if bottom_left < vert:
                    self.remove_typed_edge(((bottom_left, vert), "bottomToTop"))
                    self.remove_typed_edge(((bottom_left, vert), "bttRight"))
                else:
                    self.remove_typed_edge(((vert, bottom_left), "topToBottom"))
                    self.remove_typed_edge(((vert, bottom_left), "ttbLeft"))
            # wrapping prevents this
            for vert in [self.top_spine[i] for i in range(0, smaller)]:
                if bottom_left < vert:
                    self.remove_typed_edge(((bottom_left, vert), "bttLeft"))
                else:
                    self.remove_typed_edge(((vert, bottom_left), "ttbRight"))

    def add_blocked_edges_btt_left(self, placed_edge):
        edge = placed_edge[0]
        smaller = self.bottom_spine.index(edge[0])
        larger = self.top_spine.index(edge[1])
        
        top_right_blocked = [self.top_spine[i] for i in range(larger + 1, self.verts)]
        bottom_left_blocked = [self.bottom_spine[i] for i in range(0, smaller)]

        for top_right in top_right_blocked:
            for vert in self.top_spine:
                if top_right < vert:
                    self.remove_typed_edge(((top_right, vert), "topWrap"))
                else:
                    self.remove_typed_edge(((vert, top_right), "topWrap"))
            for vert in [self.top_spine[i] for i in range(0, larger)]:
                if top_right < vert:
                    self.remove_typed_edge(((top_right, vert), "top"))
                else:
                    self.remove_typed_edge(((vert, top_right), "top"))
            for vert in self.bottom_spine:
                if top_right < vert:
                    self.remove_typed_edge(((top_right, vert), "topToBottom"))
                    self.remove_typed_edge(((top_right, vert), "ttbLeft"))
                else:
                    self.remove_typed_edge(((vert, top_right), "bottomToTop"))
                    self.remove_typed_edge(((vert, top_right), "bttRight"))
            # wrapping prevents this
            for vert in [self.bottom_spine[i] for i in range(smaller + 1, self.verts)]:
                if top_right < vert:
                    self.remove_typed_edge(((top_right, vert), "ttbRight"))
                else:
                    self.remove_typed_edge(((vert, top_right), "bttLeft"))

        for bottom_left in bottom_left_blocked:
            for vert in self.bottom_spine:
                if bottom_left < vert:
                    self.remove_typed_edge(((bottom_left, vert), "bottomWrap"))
                else:
                    self.remove_typed_edge(((vert, bottom_left), "bottomWrap"))
            for vert in [self.bottom_spine[i] for i in range(smaller + 1, self.verts)]:
                if bottom_left < vert:
                    self.remove_typed_edge(((bottom_left, vert), "bottom"))
                else:
                    self.remove_typed_edge(((vert, bottom_left), "bottom"))
            for vert in self.top_spine:
                if bottom_left < vert:
                    self.remove_typed_edge(((bottom_left, vert), "bottomToTop"))
                    self.remove_typed_edge(((bottom_left, vert), "bttRight"))
                else:
                    self.remove_typed_edge(((vert, bottom_left), "topToBottom"))
                    self.remove_typed_edge(((vert, bottom_left), "ttbLeft"))
            # wrapping prevents this
            for vert in [self.top_spine[i] for i in range(0, larger)]:
                if bottom_left < vert:
                    self.remove_typed_edge(((bottom_left, vert), "bttLeft"))
                else:
                    self.remove_typed_edge(((vert, bottom_left), "ttbRight"))

    def add_blocked_edges_btt_right(self, placed_edge):
        edge = placed_edge[0]
        smaller = self.bottom_spine.index(edge[0])
        larger = self.top_spine.index(edge[1])
        
        top_left_blocked = [self.top_spine[i] for i in range(0, larger)]
        bottom_right_blocked = [self.bottom_spine[i] for i in range(smaller + 1, self.verts)]

        for top_left in top_left_blocked:
            for vert in self.top_spine:
                if top_left < vert:
                    self.remove_typed_edge(((top_left, vert), "topWrap"))
                else:
                    self.remove_typed_edge(((vert, top_left), "topWrap"))
            for vert in [self.top_spine[i] for i in range(larger + 1, self.verts)]:
                if top_left < vert:
                    self.remove_typed_edge(((top_left, vert), "top"))
                else:
                    self.remove_typed_edge(((vert, top_left), "top"))
            for vert in self.bottom_spine:
                if top_left < vert:
                    self.remove_typed_edge(((top_left, vert), "topToBottom"))
                    self.remove_typed_edge(((top_left, vert), "ttbRight"))
                else:
                    self.remove_typed_edge(((vert, top_left), "bottomToTop"))
                    self.remove_typed_edge(((vert, top_left), "bttLeft"))
            # wrapping prevents this
            for vert in [self.bottom_spine[i] for i in range(0, smaller)]:
                if top_left < vert:
                    self.remove_typed_edge(((top_left, vert), "ttbLeft"))
                else:
                    self.remove_typed_edge(((vert, top_left), "bttRight"))

        for bottom_right in bottom_right_blocked:
            for vert in self.bottom_spine:
                if bottom_right < vert:
                    self.remove_typed_edge(((bottom_right, vert), "bottomWrap"))
                else:
                    self.remove_typed_edge(((vert, bottom_right), "bottomWrap"))
            for vert in [self.bottom_spine[i] for i in range(0, smaller)]:
                if bottom_right < vert:
                    self.remove_typed_edge(((bottom_right, vert), "bottom"))
                else:
                    self.remove_typed_edge(((vert, bottom_right), "bottom"))
            for vert in self.top_spine:
                if bottom_right < vert:
                    self.remove_typed_edge(((bottom_right, vert), "bottomToTop"))
                    self.remove_typed_edge(((bottom_right, vert), "bttLeft"))
                else:
                    self.remove_typed_edge(((vert, bottom_right), "topToBottom"))
                    self.remove_typed_edge(((vert, bottom_right), "ttbRight"))
            # wrapping prevents this
            for vert in [self.top_spine[i] for i in range(larger + 1, self.verts)]:
                if bottom_right < vert:
                    self.remove_typed_edge(((bottom_right, vert), "bttRight"))
                else:
                    self.remove_typed_edge(((vert, bottom_right), "ttbLeft"))


    def get_available_edges(self, edge):
        edges = []
        for avail_edge in self.availableEdges:
            if avail_edge[0] == edge:
                edges.append(avail_edge)
        return edges

    def copy(self):
        graph2 = copy.deepcopy(self)
        return graph2
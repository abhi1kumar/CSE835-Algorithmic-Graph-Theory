'''
pg, version 33
This version should work with python version 3.3
Note that in numpy Array and Matrix are different.
Last update 12/10/2020
'''
import os
import numpy
from numpy import zeros
from numpy import matrix
import copy
from numpy import linalg as la
import itertools
import random
import sys
import matplotlib.cbook as cb
import matplotlib.pylab as pylab
import matplotlib.pyplot as pyplot
from matplotlib.collections import LineCollection
import networkx as nx
import math
import time

import plotting_params as params
from common_operations import *

class Graph(object):
    def __init__(self, graph = {}):
        self.g = graph
    #
    def default(self):
        self.g = {}
    #
    def save(self, name):
        output = open(name + '.pg', 'w')
        output.write(str(self.g))
        output.close()
    #
    def display(self, Laptop = 1):
        if Laptop == 1:
            self.save('C:\PythonGraph\GmpxTmp\GraphTmp')
            import os
            os.system('C:\GMPxFile\GMPx.exe C:\PythonGraph\GmpxTmp\GraphTmp.pg')
        else:
            self.save('D:\PythonGraph\GmpxTmp\GraphTmp')
            import os
            os.system('D:\Gmpx\GDGA_1\Builds\Debug\GMPx.exe D:\PythonGraph\GmpxTmp\GraphTmp.pg')
    #
    def vertices(self):
        '''
        Returns the vertex set as a sorted list.
        Output example: [0, 2, 3, 6, 7]
        '''
        return sorted(self.g.keys())
    #
    def order(self):
        '''
        Returns the number of vertices
        '''
        return len(self.vertices())
    #
    def edges(self):
        '''
        Returns the edge set of the graph.
        Sample output: [(1, 9), (1, 3), (1, 5), (1, 17), (3, 19)]
        '''
        E = []
        for i in self.g.keys():
            for j in self.g[i].keys():
                E.append((i, j))
        for (x, y) in E:
            if (y, x) in E:
                #if y == x:
                #    continue
                E.remove((y, x))
        return E
    #
    def weights(self):
        '''
        Returns the edge set of the graph with edge weights.
        Sample output: [(1, 9, 1), (1, 3, 1), (1, 5, 1), (1, 17, 1), (3, 19, 1)]
        '''
        E = []
        for i in self.g.keys():
            for j in self.g[i].keys():
                E.append((i, j, self.edge_weight(i, j)))
        for (x, y, z) in E:
            if (y, x, z) in E:
                E.remove((y, x, z))
        return E
    #
    def size(self):
        '''
        Returns the number of edges
        '''
        return len(self.edges())
    #
    def adjacent(self, i, j):
        # Returns 1 if i and j are adjacent, o otherwise
        if ((i, j) in self.edges()) or ((j, i) in self.edges()):
            return 1
        else:
            return 0
    #
    def neighbors(self, v):
        '''
        Returns a list of vertices adjacent with v.
        Sample output: [1, 11, 13, 25]
        '''
        return sorted(self.g[v].keys())
    #

    def neighborlist(self, L):
        '''
        It returns the list of vertices adjacent to vertices in L
        '''
        N = []
        for i in L:
            N = N + self.neighbors(i)
        sN = set(N)
        K = list(sN - set(L))
        K.sort()
        return K
    #
    def adjacency_list(self):
        '''
        returns adjacencey list.
        Sample output [[1, 5, 6], [0, 2], [1, 3, 6], [2, 4, 6], [3, 5], [0, 4], [0, 2, 3]]
        '''
        L = []
        for i in self.vertices():
            L.append(sorted(self.g[i].keys()))
        return L
    #
    def edge_weight(self, u, v):
        '''
        Returns the weight of edge {u, v}.
        '''
        if u in self.g.keys():
            if v in self.g[u].keys():
                return self.g[u][v]
    #
    def add_edgeOld(self, i, j, w):
        '''
        Adds the edge {i, j} with weight w.
        '''
        if i == j:
            return
        if not i in self.g:
            self.g[i] = {}
        if not j in self.g:
            self.g[j] = {}
        self.g[i][j] = w
        self.g[j][i] = w
    #
    def add_edge(self, i, j, w=1):
        '''
        Adds the edge {i, j} with weight w.
        '''
        if i == j or (i,j) in self.edges():
            return
        if i not in self.vertices() or j not in self.vertices():
            return
        self.g[i][j] = w
        self.g[j][i] = w    
    #
    def add_edges(self, edge_list = []):
        '''
        Adds edges with weight 1 to the graph.
        Input should be of form [(x, y), (x, z), ...]
        '''
        for (x, y) in edge_list:
            if (x, y) not in self.edges():
                self.add_edge(x, y, 1)
    #
    def remove_edge(self, edge):
        '''
        Removes the edge (u, v) if it exists
        '''
        i, j = edge[0], edge[1]
        if (i, j) or (j, i) in self.edges():
            i, j = edge[0], edge[1]
            del self.g[i][j]
            del self.g[j][i]
    #
    def change_edge_weight(self, edge, w):
        if edge in self.edges():
            i, j = edge[0], edge[1]
            self.g[i][j] = w
            self.g[j][i] = w
    #
    def add_vertices(self, k):
        '''
        Adds k vertices, continuing with highest current label.
        '''
        if self.order() == 0:
            for i in range(k):
                self.g[i]={}
            return self.vertices()
        else:
            new_vertices = []
            for i in range(max(self.vertices()) + 1, max(self.vertices()) + 1 + k):
                new_vertices.append(i)
                self.g[i] = {}
        return new_vertices
    #
    def add_vertices_list(self, vertex_list):
        '''
        Add vertices in the input list, if they are not already in the graph.
        '''
        for i in vertex_list:
            if not i in self.g:
                self.g[i] = {}
    #
    def remove_vertex(self, i):
        '''
        Remove vertex i if it exists.
        '''
        if i in self.g: 
            del self.g[i]
            for j in self.g.keys():
                if i in self.g[j].keys():
                    del self.g[j][i]
    #
    def remove_vertices(self, vertex_list):
        '''
        Removes the vertices given in the input list.
        '''
        for i in vertex_list:
            if i in self.g: 
                del self.g[i]
                for j in self.g.keys():
                    if i in self.g[j].keys():
                        del self.g[j][i]
    #
    def degree_sequence(self):
        '''
        Returns degree sequence as a sorted list; highest degree first.
        Sample output: [4, 4, 4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        '''
        DS = []
        for i in self.g.keys():
            y = self.g[i].keys()
            DS.append(len(y))
        return sorted(DS, reverse = True)
    #
    def degree_sequence_dict(self):
        '''
        Returns degree sequence as a dictionary, where key is vertex and value is degree.
        Sample output: {1: 3, 3: 3, 7: 3, 9: 4, 11: 4, 13: 3, 15: 4,}
        '''
        DS = {}
        for i in self.g.keys():
            y = self.g[i].keys()
            DS[i] = len(y)
        return DS
        
    def degree_Sequence_op(self):
        d = self.degree_sequence_dict()
        k = []
        for i in d:
            k.append((d[i], i))
        k.sort(reverse = True)
        return k
    #
    def leaves(self):
        '''
        Returns the leaf vertices as a list.
        '''
        L = []
        d = self.degree_sequence_dict()
        for i in d.keys():
            if d[i] == 1:
                L.append(i)
        return L
    #
    def prufer_seq(self):
        '''
        If self is a tree it returns its prufer sequence
        '''
        if not(self.size() == self.order() -1 and self.connectedness() == 1):
            return "Graph is not a tree."
        p = []
        import copy
        h = copy.deepcopy(self)
        while h.order() > 2:
            lv = h.leaves()
            l = min(lv)
            k = h.neighbors(l)
            p.append(k[0])
            h.remove_vertex(l)
        return p 
    #        
    def max_degree(self):
        # Returns max degree.
        if self.order() == 0:
            return None
        return max(self.degree_sequence())
    #
    def min_degree(self):
        # Returns minimum degree.
        if self.order() == 0:
            return None
        return min(self.degree_sequence())
    #
    def adjacency_matrix(self):
        '''
        Returns adjacency matrix of the graph as a two dimentional array.
        Note that the index of the vertex in the vertex set V gives its position in the array.
        '''
        n = self.order()
        V = self.vertices()
        from numpy import zeros
        A = zeros((n, n))
        for (x, y) in self.edges():
            i = V.index(x)
            j = V.index(y)
            A[i, j] = 1
            A[j, i] = 1
        return A
    #
    def adjacency_matrix_power(self, n = 1):
        '''
        Returns adjacency matrix of the graph to the power n.
        '''
        from numpy import matrix
        A = self.adjacency_matrix()
        A = matrix(A)
        return A ** n
    #
    def diameter(self):
        '''
        Returns the diameter of the graph, by first computing all pairs 
        distances and then finding the max.
        '''
        if self.connectedness():
            c = self.adjacency_matrix()
            n = c.shape[0]
            # use the following number as +infinity
            m = 999999999
            for i in range(n):
                for j in range(n):
                    if (i != j) and (c[i, j] == 0):
                        c[i, j] = m
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        #print(c[j, k], c[j, i] + c[i, k])
                        c[j, k] = min(c[j, k], c[j, i] + c[i, k])
            d = c.max()
            return d
        else:
            return 'Diameter is infinity'

    #
    def _component(self):
        '''
        Returns the vertex set of a component as a list. It selects a vertex and finds all
        vertices reachable from it via a path.
        '''
        p, c, V = [], [], self.vertices()
        if len(V) == 0:
            print('Input is an empty graph.')
            return None
        if len(V) == 1:
            return V
        else:
            v = V[0]
            R = self.reachable_set(v)
            return R
    #
    def components(self):
        '''
        Returns a list, consisting of vertex list of each component.
        It uses _component as a subroutine.
        Sample output: [[1, 3, 7, 9, 11], [13], [15, 17, 21, 23, 25, 27, 29, 31]]
        '''
        import copy
        h = copy.deepcopy(self)
        n = h.order()
        c = []
        while n:
            r = h._component()
            n = n - len(r)
            #print(r)
            c.append(r)
            h.remove_vertices(r)
        return c
    #
    def dfs(self, s):
        '''
        Depth First Search
        '''
        n = self.order()
        #order verices are discovered
        k = [0]* n
        #vertex from which a vertex is discovered
        f = [0]*n
        #neighbors of vertices discovered so far
        C = [[] for i in range(n)]
        #forward edges
        forwardArcs = []
        k[s] = 1
        f[s] = -1
        print("starting vertex is ", s)
        
        while True:
            # s is the center of search
            N = self.neighbors(s)
            #neighbors not covered yet
            uN = list(set(N) - set(C[s]))
            #print(uN)
            if uN == []:
                s = f[s]
                if s == -1:
                    break
                else:
                    print('backtracked to ', s)
                    continue
            v = random.choice(uN)
            C[s].append(v)
            if k[v] == 0:
                k[v] = 1
                print('discovered vertex ', v)
                f[v] = s
                forwardArcs.append((s,v))
                s = v
            else:
                print('seen vertex ', v)
        print("done")       
        
    #
    def edgeIndex(self):
        '''
        Assumes self is a tree. It returns the 
        edge index of each edge, sorted
        '''
        edgeIndex = []
        for edge in self.edges():
            self.remove_edge(edge)
            k = self.components()
            #print(edge, k)
            edgeIndex.append((len(k[0])*len(k[1]), edge))
            self.add_edge(edge[0], edge[1], 1)
        edgeIndex.sort()
        return edgeIndex
    #
    def edgeIndexDistance(self):
        '''
        Assumes self is a tree. For each edge, it returns the sum
        of the distance which uses that edge, sorted.
        '''
        edgeIndexDis = []
        dis = self.distance_matrix()
        for edge in self.edges():
            s= 0
            self.remove_edge(edge)
            k = self.components()
            #print(edge, k)
            for vertex in k[0]:
                for node in k[1]:
                    s = s + dis[vertex, node]
            edgeIndexDis.append((s, edge))
            self.add_edge(edge[0], edge[1], 1)
        edgeIndexDis.sort()
        return edgeIndexDis
        
    #
    def vertex_induced(self, s = []):
        '''
        Return subgraph induced by vertex list s.
        It return the graph data structure.
        Exampel output: {3: {7: 1}, 7: {3: 1}, 21: {29: 1}, 29: {21: 1}}
        '''
        import copy
        h = copy.deepcopy(self)
        V = h.vertices()
        Vs = set(V)
        Ss = set(s)
        Rs = Vs - Ss
        Rm = [x for x in Rs]
        h.remove_vertices(Rm)
        return h
    #
    def biparticity(self):
        '''
        Returns 1 if self is bipartite, along with its bipartitions.
        Sample output: (1, [1, 3, 5], [0, 6, 4])
        It returns (0, [], []) otherwise.
        '''
        if not self.connectedness():
            return 'Graph is not connected, run this on each component'
        Even, Odd, V = [], [], self.vertices()
        import copy
        self_copy = copy.deepcopy(self)
        for edge in self_copy.edges():
            self_copy.change_edge_weight(edge, 1)
        path = self_copy.dijkstra(V[0])
        for i in path.keys():
            if path[i][0] % 2 == 0:
                Even.append(i)
            else:
                Odd.append(i)
        #print(Even)
        #print(Odd)
        for i in Even:
            if set(self.g[i].keys()) & set(Even):
                return 0, [], []
        for i in Odd:
            if set(self.g[i].keys()) & set(Odd):
                return 0, [], []
        return 1, Even, Odd
    #
    def eulerTrail(self):
        '''
        Tests if self contains an Euler open/closed trail.
        '''
        if not self.connectedness():
            return 'Graph is not connected.'
        d = self.degree_sequence()
        od = []
        for x in d:
            if x % 2 != 0:
                od.append(x)
        if len(od) > 2:
            return 0
        else:
            return 1
    #
    def eulerian(self):
        '''
        Tests if self contains an Euler closed trail.
        '''
        if not self.connectedness():
            return 'Graph is not connected.'
        d = self.degree_sequence()
        od = []
        for x in d:
            if x % 2 != 0:
                od.append(x)
        if len(od) > 0:
            return 0
        else:
            return 1    
    def girth(self):
        '''
        Returns the girth of the graph.
        Sample output: (girth, vertex_list)
        '''
        import copy
        self_copy = copy.deepcopy(self)
        for edge in self_copy.edges():
            self_copy.change_edge_weight(edge, 1)
        E = self_copy.edges()
        C = []
        for (x, y) in E:
            self_copy.remove_edge((x, y))
            D = self_copy.dijkstra_sd(x, y)
            #print(e[0], e[1], D, '\n')
            C.append(D)
            self_copy.add_edge(x, y, 1)
        C.sort()
        return C[0][0] + 1, C[0][1]
    #
    def girth_weighted(self):
        '''
        Returns the girth of the graph.
        Sample output: (girth, vertex_list)
        '''
        E = self.edges()
        C = []
        for (x, y) in E:
            w = self.edge_weight(x, y)
            self.remove_edge((x, y))
            D1 = self.dijkstra_sd(x, y)
            D = (D1[0] + w, D1[1])
            #print(e[0], e[1], D, '\n')
            C.append(D)
            self.add_edge(x, y, w)
            #print(C, '\n')
        C.sort()
        return C[0][0] + 1, C[0][1]
    #
    def spanning_trees_count(self):
        '''
        Computes the number of spanning trees, based on degree-matrix, determinant computation
        '''
        c = self.adjacency_matrix()
        n = c.shape[0]
        for i in range(n):
            c[i, i] = c[i].sum()
        #Removing the 1st row and column
        t = c[1 :, 1 :]
        #print(c, '\n')
        #print(t, '\n')
        m = t.shape[0]
        for i in range(m):
                for j in range(m):
                        if (t[i, j] == 1) and (i != j):
                                t[i, j] = -1
        s = int(round(la.det(t)))
        return s
#
    def connectedness(self):
        '''
        Returns 1 if self is connected, 0 otherwise.
        '''
        if self.spanning_trees_count() != 0:
            return 1
        else:
            return 0
    #
    def spanning_trees_all(self):
        # Returns all the spanning trees of self
        import copy
        st = []
        n = self.order()
        q = self.size()
        L = all_sub(q)
        LL = []
        for item in L:
            if item.count('1') == n - 1:
                LL.append(item)
        for item in LL:
            self_copy = copy.deepcopy(self)
            sc_edges = self_copy.edges()
            for i in range(len(item)):
                if item[i] == '0':
                    self_copy.remove_edge(sc_edges[i])
            if self_copy.connectedness() == 1:
                st.append(self_copy.g)
        return st
    #

    def spanning_trees_all_new(self):
        # Returns all the spanning trees of self
        import copy
        import itertools
        st = []
        n = self.order()
        q = self.size()
        e = self.edges()
        for nontreeEdges in  itertools.combinations(e, q -n+1):
            self_copy = copy.deepcopy(self)
            for edge in nontreeEdges:
                self_copy.remove_edge(edge)
            if self_copy.connectedness() == 1:
                st.append(self_copy.g)
        return st
    #    
    def spanning_tree_random(self):
        n = self.order()
        e = self.edges()
        while True:
            t = random.sample(e, n-1)
            chords = list(set(self.edges()) - set(t))
            self_copy = copy.deepcopy(self)
            for i in chords:
                self_copy.remove_edge(i)
            if self_copy.connectedness():
                return self_copy
            
        
    def _independence_number_set(self, ind = []):
        '''
        This is a recursive algorithm for finding a maximum independent set and independence number of the graph.
        Sample output: (5, [2, 6, 10, 28, 9])
        '''
        if self.order() == 0:
            return 0, []
        if self.max_degree() == 0:
            return self.order(), self.vertices()
        else:
            d = self.degree_sequence_dict()
            for i in d.keys():
                if d[i] != 0:
                    break
            import copy
            h2 = copy.deepcopy(self)
            n_i = self.neighbors(i)
            self.remove_vertices(n_i + [i])
            h2.remove_vertex(i)
            r1 = self._independence_number_set()
            r2 = h2._independence_number_set()
            if r1[0] + 1 > r2[0]:
                return r1[0] + 1, r1[1] + [i]
            else:
                return r2[0], r2[1]
    #
    def max_independent_set(self):
        '''
        Calls the __independence_number_set routine by first copying the input graph and work on the copy
        '''
        import copy
        self_copy = copy.deepcopy(self)
        return self_copy._independence_number_set()
    #
    def complement(self):
        '''
        Returns the complement of the graph.
        '''
        V = self.vertices()
        gc = Graph({})
        gc.add_vertices_list(V)
        for i in V:
            for j in V:
                if i != j and j not in self.g[i]:
                    gc.add_edge(i, j, 1)
        return gc
    #
    def matching(self):
        '''
        Returns a maximum cardinality matching
        '''
        import copy
        self_copy = copy.deepcopy(self)
        return self_copy._matching()
    #
    def _matching(self, match = []):
        '''
        This is a recursive algorithm for maximum cardinality matching.
        It considers the following two situations: an edge x in a maximum matching and 
        when that edge is not in a maximum matching. For the first situation, it removes the end
        vertices of x and make a recursive call. In the other situation, it just remove edge x
        and makes a recursive call. Sampel output [3, [(1, 2), (3, 4), (5, 6)]]
        '''
        if self.order() == 0:
            return 0, []
        if self.max_degree() == 0:
            return 0, []
        if len(self.edges()) == 1:
            return 1, self.edges()
        else:
            e = self.edges()
            x = e[0]
            import copy
            h = copy.deepcopy(self)
            self.remove_edge(x)
            h.remove_vertices([x[0], x[1]])
            m_with_x = h._matching()
            m_without_x = self._matching()
            if m_with_x[0] + 1 > m_without_x[0]:
                return m_with_x[0] + 1, m_with_x[1] + [x]
            else:
                return m_without_x[0], m_without_x[1]
    #
    def max_clique_set(self):
        self_c = self.complement()
        ind = self_c.max_independent_set()
        return ind
    #
    def coloring_heuristic(self):
        '''
        Returns an upper bound for the chromatic number as well as the color sets.
        Sample output: (4, [[8, 10, 16, 17, 18, 9, 6, 3], [14, 15, 19, 7, 2], [0, 5, 11, 12, 1], [4, 13]])
        '''
        import copy
        self_copy = copy.deepcopy(self)
        cn = 0
        cs = []
        while self_copy.order():
            x = self_copy.max_independent_set()
            cn = cn + 1
            cs.append(x[1])
            self_copy.remove_vertices(x[1])
        return cn, cs
    #///////////////////////////////////////////////////////////////////////
    #
    #            Paths section
    #
    #///////////////////////////////////////////////////////////////////////
    def path(self, start, end, path = []):
        '''
        Returns, if exists, the vertices along a path from start to end.
        '''
        path = path + [start]
        if start == end:
            return path
        if start not in self.vertices():
            return None
        for vertex in self.neighbors(start):
            if vertex not in path:
                newpath = self.path(vertex, end, path)
                if newpath: 
                    return newpath
        return None
    #
    def path_all(self, start, end, path = []):
        '''
        Retruns all the paths (that is, their vertices as a list) from start to end
        '''
        path = path + [start]
        if start == end:
                return [path]
        if start not in self.vertices():
                return []
        paths = []
        for vertex in self.neighbors(start):
            if vertex not in path:
                newpaths = self.path_all(vertex, end, path)
                #print('This is paths: ', paths, '\n')
                for newpath in newpaths:
                    #print('this is newpath: ', newpath, '\n')
                    paths.append(newpath)
        return paths
    #
    def path_min_size(self, start, end):
        '''
        Returns a least size path from start to end
        '''
        import copy
        self_copy = copy.deepcopy(self)
        for edge in self_copy.edges():
            self_copy.change_edge_weight(edge, 1)
        path = self_copy.dijkstra_sd(start,end)
        return path
    #
    def _path_min_size(self, start, end, path = []):
        '''
        Returns a shortest path (no weight case). It is a brute force algorithm and thus costly
        '''
        path = path + [start]
        if start == end:
                return path
        if start not in self.vertices:
                return None
        shortest = None
        for vertex in self.neighbors(start):
            if vertex not in path:
                newpath = self.path_min_size(vertex, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest
    #
    def path_max_size(self, start, end, path = []):
        '''
        It returns a longest path from start to end. Again, it is a brute force algorithm.
        '''
        paths = self.path_all(start, end)
        #print(paths)
        maxpath = []
        for i in paths:
            if len(i) > len(maxpath):
                maxpath = i
        return maxpath
    #
    def reachable_set(self, i):
        '''
        It returns the list of vertices reachable from i
        '''
        sp, sc, sn, r = [], [i], [], [i]
        for n in range(self.order()):
            #print(sp, sc, sn, r, '\n')
            for vertex in sc:
                sn = sn + self.neighbors(vertex)
            sn_set = set(sn) - set(sc) - set(sp)
            sn = [x for x in sn_set]
            if sn == []:
                break
            sp = sc
            sc = sn
            r = r + sn
            r.sort()
        return r
    #/////////////////////////////////////////////////////////
    #
    #            Distance section
    #
    #/////////////////////////////////////////////////////////
    def max_weight_edge(self):
        '''
        Returns an edge whose weight is maximum.
        Sample output: {2: {11: 45}}
        '''
        # use the following number as -infinity
        he = -999999999
        for i in self.g.keys():
            if self.g[i].values():
                #k.append(max(self.g[i].values()))
                if he < max(self.g[i].values()):
                    he = max(self.g[i].values())
                    ev1 = i
                    for (x, y) in (self.g[i].items()):
                        if y == he:
                            ev2 = x
                #print(ev1, ev2, he)
        return {ev1 : {ev2 : he}}
    #
    def min_weight_edge(self):
        '''
        Returns an edge whose weight is minimum
        Sample output: {2: {11: 45}}
        '''
        # use the following number as +infinity
        le = 999999999
        for i in self.g.keys():
            if self.g[i].values():
                if le > min(self.g[i].values()):
                        le = min(self.g[i].values())
                        ev1 = i
                        for (x, y) in (self.g[i].items()):
                            if y == le:
                                ev2 = x
                #print(ev1, ev2, le)
        return {ev1 : {ev2 : le}}
    #
    def weight_matrix(self):
        '''
        Returns weight matrix of the graph as a two dimentional array. Note that the index of the vertex in 
        the vertex set V gives its position in the array. It is assumed that no edge weight is zero.
        '''
        n = self.order()
        V = self.vertices()
        from numpy import zeros
        W = zeros((n, n))
        for (x, y) in self.edges():
            i = V.index(x)
            j = V.index(y)
            W[i, j] = self.g[x][y]
            W[j, i] = self.g[y][x]
        for i in range(n):
            for j in range(n):
                if (i != j) and (W[i, j] == 0):
                # use 999999999 as + infinity
                    W[i, j] = 999999999
        return W
    #
    def dijkstra(self, source):
        '''
        Finds distance from source to every other vertex.
        Sample output: {destination:(distance, path)}
        '''
        #print(eval(self.min_weight_edge()))
        if list(list(self.min_weight_edge().values())[0].values())[0] < 0:
            return 'It does not work when there is an edge with negative weight in the graph.'
        V = self.vertices()
        for (x, y) in self.edges():
            if self.edge_weight(x, y) < 0:
                return ' It does not work with negative edge weights.'
        label, path = {}, {}
        for v in V:
            label[v] = 999999999
            path[v] = []
        label[source] = 0
        path[source] = [source]
        S = set([source])
        SC = set(V) - S
        while SC:
            S_list = [s for s in S]
            SC_list = [s for s in SC]
            for v in SC_list:
                if self.adjacent(source, v):
                    if label[v] > label[source] + self.edge_weight(source, v):
                        label[v] = label[source] + self.edge_weight(source, v)
                        path[v] = path[source] + [v]
            D = []
            for (v, d) in label.items():
                if v in SC_list:
                    D.append(d)
            x = min(D)
            for (v, d) in label.items():
                if v in SC_list:
                    if d == x:
                        newsource = v
                        break
            S.add(newsource)
            SC = set(V) - S
            source = newsource
            #raw_input()
        paths = {}
        for v in V:
            paths[v] = (label[v], path[v])
        return paths
    #
    def dijkstra_sd(self, source, destination):
        '''
        Finds distance from source to destination.
        Sample output: {destination:(distance, path)}
        '''
        if list(list(self.min_weight_edge().values())[0].values())[0] < 0:
            return 'It does not work when there is an edge with negative weight in the graph.'
        V = self.vertices()
        for (x, y) in self.edges():
            if self.edge_weight(x, y) < 0:
                return ' It does not work with negative edge weights.'
        label, path = {}, {}
        for v in V:
            label[v] = 999999999
            path[v] = []
        label[source] = 0
        path[source] = [source]
        S = set([source])
        SC = set(V) - S
        while destination in SC:
            S_list = [s for s in S]
            SC_list = [s for s in SC]
            for v in SC_list:
                if self.adjacent(source, v):
                    if label[v] > label[source] + self.edge_weight(source, v):
                        label[v] = label[source] + self.edge_weight(source, v)
                        path[v] = path[source] + [v]
            D = []
            for (v, d) in label.items():
                if v in SC_list:
                    D.append(d)
            x = min(D)
            for (v, d) in label.items():
                if v in SC_list:
                    if d == x:
                        newsource = v
                        break
            S.add(newsource)
            SC = set(V) - S
            source = newsource
            #raw_input()
        paths = {}
        for v in V:
            paths[v] = (label[v], path[v])
        return paths[destination]
        #return label[destination], path[destination]
    #
    def dpt(self, source):
        '''
        Return a distance presevating tree with respect to the source
        '''
        h = self.dijkstra(source)
        #print(h)
        t = Graph({})
        t.add_vertices_list(self.vertices())
        paths = []
        for i in range(len(h)):
            paths.append(h[i][1])
            #print(paths)
        for i in paths:
            if len(i) > 1:
                for j in range(len(i) - 1):
                    t.add_edge(i[j], i[j + 1], self.edge_weight(i[j], i[j + 1]))
        return t
    #
    def dpTree(self, v):
        '''
        It returns vertices and level in a distance-preserving tree with respect to v
        '''
        levelVertices = [(0,v)]
        L = [v]
        i = 1
        while set(L) != set(self.vertices()):
            S = self.neighborlist(L)
            for j in S:
                levelVertices.append((i, j))
            i = i+1
            L = L + S
            #print(L, flush=True)
        return levelVertices   
        
    #
    def dpTreeGraph(self, v):
        '''
        It returns a distance-preserving tree with respect to v with all weights 1. Does not take edge weight into account.
        If you want to preserve edge weights as well, use dpt()
        '''
        T = Graph({})
        T.add_vertices_list(self.vertices())
        levelVertices = [(0,v)]
        L = [v]
        i = 1
        while set(L) != set(self.vertices()):
            S = self.neighborlist(L)
            for j in S:
                levelVertices.append((i, j))
            i = i+1
            for u in S:
                for v in L:
                    if (u,v) not in T.edges() or (v,u) not in T.edges():
                        if (u,v) in self.edges() or (v,u) in self.edges():
                            T.add_edge(u,v,1)
                    #print(T.edges())
            L = L + S
            #print(L, flush=True)
        return T
    #
    def parity(self):
        '''
        Decides if self is parity
        '''
        if not self.connectedness():
            return 0
        W = self.distance_matrix()
        n = W.shape[0]
        for u in range(n):
            for v in range(u + 1, n):
                for w in range(v + 1, n):
                    for x in range(w + 1, n):
                        d1 = W[u, v] + W[w, x]
                        d2 = W[u, w] + W[v, x]
                        d3 = W[u, x] + W[v, w]
                        if d1 != d2 and d1 != d3 and d2 != d3 and not (d1 % 2 == d2 % 2 and d1 % 2 == d3 % 2):
                            return 0
        return 1
    #
    def distance_hereditary(self, print_nodes= False):
        '''
        Decides if self is distance hereditary
        '''
        if not self.connectedness():
            return 0
        W = self.distance_matrix()
        n = W.shape[0]
        for u in range(n):
            for v in range(u + 1, n):
                for w in range(v + 1, n):
                    for x in range(w + 1, n):
                        d1 = W[u, v] + W[w, x]
                        d2 = W[u, w] + W[v, x]
                        d3 = W[u, x] + W[v,w]
                        if d1 != d2 and d1 != d3 and d2 != d3:
                            if print_nodes:
                                print("u={} v={} w={} x={} D(u,v)={} D(w,x)={} D(u,w)={} D(v,x)={} D(u,x)={} D(v,w)={}".format(u, v, w, x, W[u, v], W[w, x], W[u, w], W[v, x], W[u, x], W[v,w]))
                            return 0
        return 1
    #
    def distance_preserving(self, verbose = False):
        if self.distance_hereditary():
            return 1
        n = self.order()
        g_dist = self.distance_matrix()
        dp_subgraph = [0] * n
        for k in range(n, 0, -1):
            for v in itertools.combinations(self.vertices(), k):
                h = self.vertex_induced(v)
                h_dist = h.distance_matrix()
                if numpy.all(g_dist[v, :][:, v] == h_dist):
                    dp_subgraph[k - 1] = 1
                    break
        if sum(dp_subgraph) == n:
            return 1
        if verbose:
            print(dp_subgraph, ',', self.induced_cycle())
        return 0
    #
    def isometricSubBF(self, x, y):
        '''
        It checks for isometric subgraphs of order from x to y inclusive, x > y
        '''
        if self.distance_hereditary():
            return 1
        n = self.order()
        g_dist = self.distance_matrix()
        dp_subgraph = [0] * n
        for k in range(x, y+1, -1):
            for v in itertools.combinations(self.vertices(), k):
                print(len(v))
                h = self.vertex_induced(v)
                h_dist = h.distance_matrix()
                if numpy.all(g_dist[v, :][:, v] == h_dist):
                    dp_subgraph[k - 1] = 1
                    break
        #print(dp_subgraph)
        if sum(dp_subgraph) == x - y + 1:
            return 1, dp_subgraph
        else:
            return v, dp_subgraph
    #
            
    def isometricSpecific(self, D):
        '''
        It checks if self with vertices remove in D gives an isometric subgraph
        '''
        g_dist = self.distance_matrix()
        vSelf = self.vertices()
        v = list(set(vSelf)- set(D))

        h = self.vertex_induced(v)
        h_dist = h.distance_matrix()
        if numpy.all(g_dist[v, :][:, v] == h_dist):
            return 1
        else:
            return 0

    def distance_preserving_np(self, k, trial=1000):
        import time
        st = time.clock()
        g_dist = self.distance_matrix()
        for i in range(trial):
            v = random.sample(self.vertices(), k)
            v.sort()
            h = self.vertex_induced(v)
            h_dist = h.distance_matrix()
            #print(v)
            #print(g_dist[v, :][:, v])
            #print(h_dist)
            if numpy.all(g_dist[v, :][:, v] == h_dist):
                return(v, time.clock() - st)
        return 0

    def isometricSubgraph(self, k, trial=500):
        '''
        Attempting to find an isometric subgraph of 
        order k by doing random selection and testing.
        '''
        g_dist = self.distance_matrix()
        for i in range(trial):
            v = random.sample(self.vertices(), k)
            v.sort()
            h = self.vertex_induced(v)
            if h.connectedness() == 0:
                continue
            h_dist = h.distance_matrix()
            if numpy.all(g_dist[v, :][:, v] == h_dist):
                return(1, v)
        return(0, v)

    def isoSubgraph(self, k):
        '''
        Attempting to find an isometrci subgraph of 
        order k by prouning leaves of some distance
        preserving tree.
        '''
        g_dist = self.distance_matrix()
        for i in self.vertices():
            tree = self.dpTree(i)
            V = []
            for j in tree:
                V.append(j[1])
            V = V[:k]
            V.sort()
            h = self.vertex_induced(V)
            h_dist = h.distance_matrix()
            if numpy.all(g_dist[V, :][:, V] == h_dist):
                return(1, V)
        return(0, V)
        
#
    def isoSubgraph2(self, k):
        '''
        Attempting to find an isometrci subgraph of 
        order k by prouning leaves of some distance
        preserving tree. Here we select vertices in order of 
        their degree, with highest degree first.
        '''
        g_dist = self.distance_matrix()
        
        for i in self.degree_Sequence_op():
            tree = self.dpTree(i[1])
            V = []
            for j in tree:
                V.append(j[1])
            V = V[:k]
            V.sort()
            h = self.vertex_induced(V)
            h_dist = h.distance_matrix()
            if numpy.all(g_dist[V, :][:, V] == h_dist):
                return(1, V)
        return(0, V)
        
#
    def isDP(self):
        st = time.clock()
        maxDegree = self.max_degree()
        order = self.order()
        #print('Order is ', order, 'maxdegree is ', maxDegree)
        for i in range(order -1, maxDegree+1, -1):
            h = self.isoSubgraph(i)
            #print(h[1])
            if h[0] == 0:
                print('G may not have an isometric subgraph of order ', len(h[1]))
                print('It took ', time.clock() - st, ' seconds.')
                return
        print('G is distance preserving.')
        print('It took ', time.clock() - st, ' seconds.')
        return
        
#
    def isDP2(self):
        st = time.clock()
        maxDegree = self.max_degree()
        order = self.order()
        #print('Order is ', order, 'maxdegree is ', maxDegree)
        for i in range(order -1, maxDegree+1, -1):
            h = self.isoSubgraph2(i)
            #print(h[1])
            if h[0] == 0:
                print('G may not have an isometric subgraph of order ', len(h[1]))
                print('It took ', time.clock() - st, ' seconds.')
                return
        print('G is distance preserving.')
        print('It took ', time.clock() - st, ' seconds.')
        return       
    #
    def perfect(self):
        h = self.complement()
        for k in range(5, self.order() + 1, 2):
            if self.induced_cycle(k) or h.induced_cycle(k):
                return 0
        return 1
    #
    def induced_cycle(self, k = False):
        import itertools
        i = 0
        if k:
            for v in itertools.combinations(self.vertices(), k):
                h = self.vertex_induced(v)
                if h.connectedness() and h.degree_sequence() == [2] * k:
                    i = i + 1
        else:
            for k in range(self.order(), 0, -1):
                for v in itertools.combinations(self.vertices(), k):
                    h = self.vertex_induced(v)
                    if h.connectedness() and h.degree_sequence() == [2] * k:
                        return k
        return i
    #
    def distance_matrix(self):
        # Returns the distance matrix

        W = self.weight_matrix()
        n = W.shape[0]
        #print "Here is W"
        #print W
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    #print(W[j, k], W[j, i] + W[i, k])
                    W[j, k] = min(W[j, k], W[j, i] + W[i, k])
            #print("Here is W")
        for i in range(n):
            if W[i, i] < 0:
                return 'There is a negative weight cycle.'
            else:
                W[i, i] = 0
        return W
    #
    def distance_list(self):
        # Returns the distance matrix as a sorted list

        W = self.distance_matrix()
        n = W.shape[0]
        L = []
        for i in range(n):
            for j in range(i + 1, n, 1):
                L.append(W[i, j])
        L.sort()
        return L
    #
    
    def wienerIndex(self):
        '''
        returns sum of distances in self.
        '''
        return sum(self.distance_list())
    #
    def weighted_diameter(self):
        '''
        Returns the diameter. It assumes that there is no negative weight cycle.
        '''
        if self.connectedness():
            W = self.distance_matrix()
            d = W.max()
            return d
        else:
            return 'Diameter is infinity'
    #
    def center(self):
        '''
        Returns a center vertex. It assumes that there is no negative weight cycle.
        '''
        if self.connectedness():
            W = self.distance_matrix()
            n = W.shape[0]
            L = []
            for i in range(n):
                L.append(W[i].max())
            r = min(L)
            vertex = L.index(r)
            return ('A center is vertex ', vertex, 'and the radius is ', r)
        else:
            return 'Graph is not connected'
    #       
    def centerTree(self):
        '''
        returns the center(s) of tree self
        '''
        g = copy.deepcopy(self)
        while g.order() > 2:
            k = g.leaves()
            g.remove_vertices(k)
        return g.vertices()
    #
    
    def hammming(self):
        '''
        It reurns a Hamming labelimg of tree self as a dictionary
        '''
        g = copy.deepcopy(self)
        rList = []
        hamLabel = {}
        while len(g.leaves()) > 1:
            leaves = g.leaves()
            v = random.choice(leaves)
            w = g.neighbors(v)[0]
            rList.append((v,w))
            g.remove_vertex(v)
            #hamLabel[v] = '0'
        u = g.vertices()[0]
        hamLabel[u] = '0'
        #print(rList, hamLabel)        
        while rList !=[]:
            d = rList.pop()
            #print(d, rList)
            x = d[0]
            y = d[1]
            g.add_edge(x,y,1)
            for key in hamLabel.keys():
                hamLabel[key] = hamLabel[key] + '0'
            hamLabel[x] = hamLabel[y][:-1] + '1'    
        return(hamLabel)
    # 
    def delay_cost(self):
        # Returns the delay cost 

        W = self.distance_matrix()
        #n = n = W.shape[0]
        return sum(sum(W))
    #
    def weight_sum(self):
        # Returns the sum of the weights
        sum = 0
        for edge in self.edges():
            i, j = edge[0], edge[1]
            sum = sum + self.edge_weight(i, j)
        return sum
    #
    def mst(self):
        # Returns a minimum spanning tree
        if not self.connectedness():
            return 'Graph is not connected'
        import copy
        h = copy.deepcopy(self)
        V = h.vertices()
        n = len(V)
        vt = {}
        for i in V:
            vt[i] = {}
        t = Graph(vt)
        while t.size() < n - 1:
            e = h.min_weight_edge()
            v1 = list(e.keys())[0]
            v2 = list(list(e.values())[0].keys())[0]
            w = e[v1][v2]
            #print('examining edge', (v1, v2), ' with weight', w, '\n')
            h.remove_edge((v1, v2))
            if not t.path(v1, v2):
                t.add_edge(v1, v2, w)
        return t.weight_sum(), t.g
    #
    def mst_all(self):
        # Returns all the minimum spanning trees of self
        k = self.mst()
        mstweight = k[0]
        #print(k[0])
        L = self.spanning_trees_all()
        mstL = []
        for graph in L:
            g = Graph(graph)
            #print(g.g, g.weight_sum())
            if g.weight_sum() == mstweight:
                mstL.append(g.g)
        return mstL
    #
    def iso(self):
        # Generate a new graph isomorphic to self.
        import copy
        h = copy.deepcopy(self)
        v = h.vertices()

        m = random.choice(range(len(v)))
        u = v[m] # selected vertex to remove
        nl = list(h.g[u].keys())
        #print(u, nl)
        h.remove_vertex(u)
        x = h.add_vertices(1)
        for y in nl:
            h.add_edge(x[0], y, 1)
        return h
    #
    # {0: {4: 6, 5: 7, 6: 1, 7: 7}, 1: {4: 5, 6: 3, 7: 1}, 2: {4: 8, 5: 4, 7: 4}, 3: {4: 8, 6: 8}, 4: {0: 6, 1: 5, 2: 8, 3: 8, 7: 7}, 5: {0: 7, 2: 4}, 6: {0: 1, 1: 3, 3: 8}, 7: {0: 7, 1: 1, 2: 4, 4: 7}}
    #
    def check_delay_Cost(self, delay):
        #Returns all spanning trees of self with delay cost <= delay
        import sys
        import copy
        #st = open('C:\PgOutput\SpanningTrees.txt','w')
        n = self.order()
        q = self.size()
        L = all_sub(q)
        LL = []
        LLL = []
        for item in L:
            if item.count('1') == n - 1:
                LL.append(item)
        for item in LL:
            self_copy = copy.deepcopy(self)
            sc_edges = self_copy.edges()
            for i in range(len(item)):
                if item[i] == '0':
                    self_copy.remove_edge(sc_edges[i])
            if self_copy.connectedness() == 1:
                dc = self_copy.delay_cost()
                if dc <= delay: 
                    #print(>> st, self_copy.g)
                    #print(>> st, '------------------------------------------------------------')
                    #print(self_copy.g)
                    #print(dc)
                    #print('::::::::::::')
                    LLL.append(self_copy.g)
        return LLL
    #
    def vertex_clusCoef(self):
        '''
        It finds the clustering coefficient of each vertex in v
        '''
        V = self.vertices()
        l = []
        for vertex in V:
            h = self.vertex_induced(self.neighbors(vertex))
            ns = len(self.neighbors(vertex))
            if ns == 0 :
                l.append((vertex, 0))
            elif ns == 1:
                l.append((vertex, 1))
            else:
                vce = h.size() / (ns * (ns - 1) / 2.)
                l.append((vertex, vce))
        return l
    #
    def clusCoef(self):
        '''
        Returns the clustering coefficient of self
        '''
        l = self.vertex_clusCoef()
        x = 0.
        for i in l:
            x = x + i[1]
        return x/len(l)
    #
    def density(self,k):
        '''
        Return the average density
        '''
        l = gen_sub(self.vertices(), k)
        #print(l)
        den = 0.
        for i in l:
            h = self.vertex_induced(i)
            den = den + h.size() / (len(i) * (len(i) - 1) / 2.)
        return den / len(l)    
    #
    def allsubgraphs_ds(self, k):
        '''
        It returns all the subgraphs of self whose degree sequence is k
        '''
        if self.size() < sum(k) / 2:
            print('No subgraphs with degree sequence k.')
            return
        e = self.edges()
        SubEgdes = gen_sub(e, sum(k) / 2)
        AllSubGraphs = []
        import copy
        for x in SubEgdes:
            h = copy.deepcopy(self)
            for edge in h.edges():
                if edge not in x:
                    h.remove_edge(edge)
            if h.degree_sequence() == k:
                AllSubGraphs.append(h.g)
        return AllSubGraphs
        
        
    #
    def edgeImpact(self):
        '''
        For each missing edge e in self, it returns a sorted list k
        of ordered pairs (s, e) where s is the amount by which
        the total distances are reduced.
        '''
        h = self.complement()
        w = self.distance_matrix()
        k = []
        for eachEdge in h.edges():
            self.add_edge(eachEdge[0], eachEdge[1], 1)
            x = self.distance_matrix()
            s = sum(sum(w-x))/2
            k.append((s, eachEdge))
            self.remove_edge(eachEdge)
        k.sort()
        return k

    #

    def edgeImpactSet(self, q):
        '''
        For each missing edge e in q, it returns a sorted list k
        of ordered pairs (s, e) where s is the amount by which
        the total distances are reduced.
        '''
        h = self.complement()
        w = self.distance_matrix()
        k = []
        for edgeList in itertools.combinations(h.edges(), q):        
            self.add_edges(edgeList)
            x = self.distance_matrix()
            s = sum(sum(w-x))/2
            k.append((s, edgeList))
            for edge in edgeList:
                self.remove_edge(edge)
        k.sort()
        return k
  #
    def edgeImpactSP(self):
        '''
        For each missing edge e in self, it returns a sorted list k
        of ordered pairs (s, e) where s is the amount by which
        the the number of spanning trees are increased.
        '''
        h = self.complement()
        w = self.spanning_trees_count()
        k = []
        for eachEdge in h.edges():
            self.add_edge(eachEdge[0], eachEdge[1], 1)
            x = self.spanning_trees_count()
            s = x-w
            k.append((s, eachEdge))
            self.remove_edge(eachEdge)
        k.sort()
        return k
    #
    def edgeImpactCount(self):
        '''
        For each missing edge e in self, it returns a sorted list k
        of ordered pairs (s, e) where s is the count by which
        the distances are reduced.
        '''
        h = self.complement()
        w = self.distance_matrix()
        k = []
        for eachEdge in h.edges():
            self.add_edge(eachEdge[0], eachEdge[1], 1)
            x = self.distance_matrix()
            y = w-x
            #print(y)
            s = numpy.count_nonzero(y)/2
            #print(s)
            k.append((s, eachEdge))
            self.remove_edge(eachEdge)
        k.sort()
        return k       
    #Adding edges of least impact    
    def evolUsingEdgeImpact(self, leastImpactEdge = True, wd = True):
        h = copy.deepcopy(self)
        seqEdge = []
        s = h.size()
        o = h.order()
        
        while s != o*(o-1)/2:
            k = h.edgeImpact()
            #print(k)
            if leastImpactEdge:
                edge2use = k.pop(0)[1]
            else:
                edge2use = k.pop()[1]
            
            theEdge = (edge2use[0], edge2use[1])
            #print(leastImpactEdge)
            seqEdge.append(theEdge)
            h.add_edge(theEdge[0], theEdge[1],1)
            s = h.size()
            o = h.order()
            if wd:
                h.draw()
            if h.distance_preserving() != 1:
                print('It is not dp.')
                print(seqEdge)
                break
        return seqEdge
        
    def evolUsingEdgeImpactCount(self, leastImpactEdge = True, wd = True):
        h = copy.deepcopy(self)
        seqEdge = []
        s = h.size()
        o = h.order()
        
        while s != o*(o-1)/2:
            k = h.edgeImpactCount()
            #print(k)
            if leastImpactEdge:
                edge2use = k.pop(0)[1]
            else:
                edge2use = k.pop()[1]
            
            theEdge = (edge2use[0], edge2use[1])
            #print(leastImpactEdge)
            seqEdge.append(theEdge)
            h.add_edge(theEdge[0], theEdge[1],1)
            s = h.size()
            o = h.order()
            if wd:
                h.draw()
            if h.distance_preserving() != 1:
                print('It is not dp.')
                print(seqEdge)
                break
        return seqEdge


    def evolUsingEdgeImpactSP(self, leastImpactEdge = True, wd = True):
        h = copy.deepcopy(self)
        seqEdge = []
        s = h.size()
        o = h.order()
        
        while s != o*(o-1)/2:
            k = h.edgeImpactSP()
            #print(k)
            if leastImpactEdge:
                edge2use = k.pop(0)[1]
            else:
                edge2use = k.pop()[1]
            
            theEdge = (edge2use[0], edge2use[1])
            #print(leastImpactEdge)
            seqEdge.append(theEdge)
            h.add_edge(theEdge[0], theEdge[1],1)
            s = h.size()
            o = h.order()
            if wd:
                h.draw()
        return seqEdge        
    '''
    import matplotlib.pyplot as plt
    plt.hist([1, 2, 1], bins=[0, 1, 2, 3])


    '''
        
            
    #/////////////////////////////////////////////////////////
    #
    #            Drawing section
    #
    #/////////////////////////////////////////////////////////
    def circular_layout(self, scale = 1):
        import numpy
        t = numpy.arange(0, 2.0 * numpy.pi, 2.0 * numpy.pi / self.order(), dtype = numpy.float32)
        pos = numpy.transpose(numpy.array([numpy.cos(t), numpy.sin(t)]))
        lim = 0 # max coordinate for all axes
        for i in range(pos.shape[1]):
            pos[:, i] -= pos[:, i].min()
            lim=max(pos[:, i].max(), lim)
        # rescale to (0, scale) in all directions, preserves aspect
        for i in range(pos.shape[1]):
            pos[:, i] *= scale / lim
        pos = dict(zip(self.g, pos))
        return pos
    #
    def random_layout(self, scale = 1):
        import numpy
        pos = numpy.asarray(numpy.random.random((self.order(), 2)), dtype = numpy.float32)
        lim = 0 # max coordinate for all axes
        for i in range(pos.shape[1]):
            pos[:, i] -= pos[:, i].min()
            lim=max(pos[:, i].max(), lim)
        # rescale to (0, scale) in all directions, preserves aspect
        for i in range(pos.shape[1]):
            pos[:, i] *= scale / lim
        pos = dict(zip(self.g, pos))
        return pos
    #
    def spring_layout(self, scale = 1):
        import numpy
        pos = None
        fixed = None
        iterations = 50
        weighted = True
        nfixed = dict(zip(self.g, range(self.order())))
        pos_arr = None
        A = self.distance_matrix()
        nnodes, _= A.shape
        A = numpy.asarray(A) # make sure we have an array instead of a matrix
        if not weighted: # use 0/1 adjacency instead of weights
            A = numpy.where(A == 0, A, A / A)
        # random initial positions
        pos = numpy.asarray(numpy.random.random((nnodes, 2)), dtype = A.dtype)
        # optimal distance between nodes
        k = numpy.sqrt(1.0 / nnodes) 
        # the initial 'temperature' is about .1 of domain area (=1x1)
        # this is the largest step allowed in the dynamics.
        t = 0.1
        # simple cooling scheme.
        # linearly step down by dt on each iteration so last iteration is size dt.
        dt = t / float(iterations + 1) 
        delta = numpy.zeros((pos.shape[0], pos.shape[0], pos.shape[1]), dtype = A.dtype)
        # the inscrutable (but fast) version
        # this is still O(V^2)
        # could use multilevel methods to speed this up significantly
        for iteration in range(iterations):
            # matrix of difference between points
            for i in range(pos.shape[1]):
                delta[:, :, i]= pos[:, i, None] - pos[:, i]
            # distance between points
            distance = numpy.sqrt((delta ** 2).sum(axis = -1))
            # enforce minimum distance of 0.01
            distance = numpy.where(distance < 0.01, 0.01, distance)
            # displacement 'force'
            displacement = numpy.transpose(numpy.transpose(delta) *\
                                            (k * k / distance ** 2 - A * distance / k)) \
                                            . sum(axis = 1)
            # update positions            
            length = numpy.sqrt((displacement ** 2).sum(axis = 1))
            length = numpy.where(length < 0.01, 0.1, length)
            delta_pos = numpy.transpose(numpy.transpose(displacement) * t / length)
            if fixed is not None:
                # don't change positions of fixed nodes
                delta_pos[fixed] = 0.0
            pos += delta_pos
            # cool temperature
            t -= dt
        lim = 0 # max coordinate for all axes
        for i in range(pos.shape[1]):
            pos[:, i] -= pos[:, i].min()
            lim=max(pos[:, i].max(), lim)
        # rescale to (0, scale) in all directions, preserves aspect
        for i in range(pos.shape[1]):
            pos[:, i] *= scale / lim
        pos = dict(zip(self.g, pos))
        return pos
    #
    def draw_matplotlib(self, layout = 'circular', path = None, scale = 1, vertex_size= 2500, vertex_color= params.color1, lw= params.lw, dpi= params.DPI, fs= params.fs, 
        radius_self_loop = 0.12, show_figure= False):
        try:
            import matplotlib.cbook as cb
            import matplotlib.pylab as pylab
            import matplotlib.pyplot as plt
            from matplotlib.collections import LineCollection
        except ImportError:
            print('matplotlib is required for draw_matplotlib()')
            return
        import numpy
        plt.figure(dpi= dpi)
        plt.clf()
        n = self.order()
        if layout == 'circular':
            pos = self.circular_layout(scale)
        elif layout == 'random':
            pos = self.random_layout(scale)
        elif layout == 'spring':
            pos = self.spring_layout(scale)
        else:
            pos = self.spring_layout(scale)
        # initialize graph
        cf = plt.gcf()
        cf.set_facecolor('w')
        ax = cf.add_axes((0, 0, 1, 1))
        ax.set_axis_off()
        # draw vertices
        nodelist = self.vertices()
        xy = numpy.asarray([pos[v] for v in nodelist])
        node_collection = ax.scatter(xy[:, 0], xy[:, 1],
                                        s = vertex_size, # vertex size
                                        c = vertex_color, # vertex color
                                        marker='o', # vertex shape
                                        cmap = None,
                                        vmin = None,
                                        vmax = None,
                                        alpha = 1.0,
                                        linewidths = lw)
        plt.axes(ax)
        plt.sci(node_collection)
        node_collection.set_zorder(2)
        # draw vertex labels
        labels = dict(zip(self.vertices(), self.vertices()))
        text_items={}
        for (n, label) in labels.items():
            (x, y) = pos[n]
            t = ax.text(x, y, label,
                        size = fs,
                        color = 'k', # font color
                        family = 'sans-serif', # font family
                        weight = 'normal', # font weight
                        horizontalalignment = 'center',
                        verticalalignment = 'center',
                        transform = ax.transData)
            text_items[n] = t
        # draw edges
        edge_color = 'k'
        edgelist = self.edges()
        edge_pos = []
        num_points = 720
        angle  = numpy.arange(num_points+1)*2*numpy.pi/num_points
        x_spiral = radius_self_loop * numpy.cos(angle)
        y_spiral = radius_self_loop * numpy.sin(angle)
        for e in edgelist:
            if e[0] == e[1]:
                # draw a spiral
                x = pos[e[0]][0] + radius_self_loop*0.7 + x_spiral
                y = pos[e[0]][1] + radius_self_loop*0.7 + y_spiral
                for ind in range(num_points):
                    edge_pos.append(([x[ind], y[ind]], [x[ind+1], y[ind+1]]))
            else:
                edge_pos.append((pos[e[0]], pos[e[1]]))
        edge_pos = numpy.asarray(edge_pos)       
        edge_colors = tuple(edge_color)
        edge_collection = LineCollection(edge_pos,
                                        colors = edge_colors,
                                        linewidths = lw,
                                        antialiaseds = (1,),
                                        linestyle = 'solid',     
                                        transOffset = ax.transData)
        edge_collection.set_zorder(1) # edges go behind nodes            
        ax.add_collection(edge_collection)
        # draw edge labels
        if self.weight_sum() != self.size():
            labels=dict(zip(self.edges(), [d for u, v, d in self.weights()]))
            text_items={}
            for ((n1, n2), label) in labels.items():
                (x1, y1) = pos[n1]
                (x2, y2) = pos[n2]
                (x, y) = ((x1 + x2) / 2, (y1 + y2) / 2)
                angle = numpy.arctan2(y2 - y1, x2 - x1) / (2.0 * numpy.pi) * 360 # degrees
                # make label orientation 'right-side-up'
                if angle > 90: 
                    angle -= 180
                if angle < -90: 
                    angle += 180
                # transform data coordinate angle to screen coordinate angle
                xy = numpy.array((x, y))
                trans_angle = ax.transData.transform_angles(numpy.array((angle,)),
                                                            xy.reshape((1, 2)))[0]
                # use default box of white with white border
                bbox = dict(boxstyle = 'round',
                            ec=(1.0, 1.0, 1.0),
                            fc=(1.0, 1.0, 1.0))
                t = ax.text(x, y, label,
                            size = fs, # font size
                            color = 'k', # font color
                            family = 'sans-serif', # font family
                            weight = 'normal', # font weight
                            horizontalalignment = 'center',
                            verticalalignment = 'center',
                            rotation = trans_angle,
                            transform = ax.transData,
                            bbox = bbox,
                            zorder = 1)
                text_items[(n1, n2)] = t
        # update view
        pad_view = 0.1
        minx = numpy.amin(numpy.ravel(edge_pos[:, :, 0]- pad_view))
        maxx = numpy.amax(numpy.ravel(edge_pos[:, :, 0]+ pad_view))
        miny = numpy.amin(numpy.ravel(edge_pos[:, :, 1]- pad_view))
        maxy = numpy.amax(numpy.ravel(edge_pos[:, :, 1]+ pad_view))
        plt.xlim((minx, maxx))
        plt.ylim((miny, maxy))
        # draw graph
        # pylab.draw_if_interactive()
        if path is not None:
            savefig(plt, path)
        if show_figure:
            plt.show()
    #
    def draw_tkz_graph(self, layout = 'spring', scale = 10):
        if layout == 'circular':
            pos = self.circular_layout(scale)
        elif layout == 'random':
            pos = self.random_layout(scale)
        elif layout == 'spring':
            pos = self.spring_layout(scale)
        else:
            layout = self.spring_layout(scale)
        print('\\begin{tikzpicture}')
        print('  \\GraphInit')
        if self.weight_sum() == self.size():
            print('  \\SetVertexNoLabel')
        print('  \\tikzstyle{VertexStyle} = [shape=circle,ball color=black!0, draw]')
        for i in self.vertices():
            (x, y) = pos[i]
            print('  \\Vertex[x=' + str(round(x, 2)) + ', y=' + str(round(y, 2)) + ']{' + str(i) + '}')
        if self.weight_sum() == self.size():
            for (i, j) in self.edges():
                print('  \\Edge(' + str(i) + ')(' + str(j) + ')')
        else:
            for (i, j) in self.edges():
                print('  \\Edge[label=$' + str(self.g[i][j]) + '$](' + str(i) + ')(' + str(j) + ')')
        print('\\end{tikzpicture}')



    def make_dh(self):
        '''
        It finds the least number of additional edges to make self distant-hereditary
        '''
        h = self.complement()
        E = h.edges()
        import itertools
        for i in range (1, h.size() + 1):
            print(i)
            for j in itertools.combinations(E,i):
                #print(j)
                self.add_edges(j)
                if self.distance_hereditary():
                    return j
                else:
                    for k in range(i):
                        self.remove_edge(j[k])
                                                

    def draw(self):
            '''
            It draws self using networkx circular drawing
            '''
            G = nx.Graph()
            for i in self.vertices():
                    G.add_node(i)
            for i in self.edges():
                G.add_edge(i[0],i[1])
            nx.draw_circular(G)

    def isometric_sub_find(self):
        n = self.order()
        g_dist = self.distance_matrix()
        dp_subgraph = [None] * n
        for k in range(n, 0, -1):
            for v in itertools.combinations(self.vertices(), k):
                h = self.vertex_induced(v)
                h_dist = h.distance_matrix()
                w = [i for i, j in enumerate(self.vertices()) if j in v]
                if numpy.all(g_dist[w, :][:, w] == h_dist):
                    dp_subgraph[k - 1] = v
                    break
        return dp_subgraph
        
    def line_graph(self):
        e = self.edges()
        g = Graph({})
        g.add_vertices(len(e))
        for u, v in itertools.combinations(range(len(e)), 2):
            if e[u][0] in e[v] or e[u][1] in e[v]:
                g.add_edge(u, v, 1)
        return g
 

                
#/////////////////////////////////////////////////////////
#
#            Graph Construction section
#
#/////////////////////////////////////////////////////////
def star(n,w=1):
    '''
    Creates an n-vertex star graph, with edge weight (all) w
    '''
    g = Graph({})
    g.add_vertices(n)
    for i in range(1,n):
        g.add_edge(0, i, w)
    return g
    
def cycle(n, w=1):
    '''
    Creates an n-vertex cycle graph, with edge weight (all) w
    '''
    g = Graph({})
    g.add_vertices(n)
    for i in range (0, n-1):
        g.add_edge(i, i+1, w)
    g.add_edge(n-1, 0, 1)
    return g

def line(n,w=1):
    '''
    Creates an n-vertex line graph, with edge weight (all) w
    '''
    g = Graph({})
    g.add_vertices(n)
    for i in range(0,n-1):
        g.add_edge(i, i+1, w)
    return g

def cube(n):
    #Creates an n-cube graph
    #print(n)
    g = Graph({})
    g.add_vertices(1 << n)
    for i in range(1 << n):
        v = 0
        for j in range(n):
            if (i >> j) % 2 == 1:
                g.add_edge(i, i - (1 << j), 1)
            else:
                g.add_edge(i, i + (1 << j), 1)
    return g
    
def tcube(n):
    #Creates a twisted n-cube graph
    #print(n)
    g = Graph({})
    g.add_vertices(1 << n)
    for i in range(1 << n):
        v = 0
        for j in range(n):
            if (i >> j) % 2 == 1:
                g.add_edge(i, i - (1 << j), 1)
            else:
                g.add_edge(i, i + (1 << j), 1)
    g.remove_edge((0,1))
    g.remove_edge((2,3))
    g.add_edge(1,2,1)
    g.add_edge(0,3,1)
    return g
#
def de_bruijn(n):
    g = Graph({})
    g.add_vertices(1 << n)
    for i in range(1 << n):
        v = 0
        for j in range(n - 1):
            if (i >> j) % 2 == 1:
                v = v + 2 ** (j + 1)
        if i != v:
            g.add_edge(i, v, 1)
        if i != v + 1:
            g.add_edge(i, v + 1, 1)
        v = 0
        for j in range(1, n):
            if (i >> j) % 2 == 1:
                v = v + 2 ** (j - 1)
        if i != v:
            g.add_edge(i, v, 1)
        if i != v + (1 << (n - 1)):
            g.add_edge(i, v + (1 << (n - 1)), 1)
    return g
#
def random_graph(n=10, edge_prob=0.5):
    '''
    Returns an n-order random graph 
    '''

    g = Graph({})
    g.add_vertices(n)
    for i in range(n):
        for j in range(i + 1, n):
            x = random.uniform(0, 1)
            if x <= edge_prob:
                g.add_edge(i, j, 1)
    return g

def random_social_graph(n=10, edge_prob=0.5):
    '''
    Returns an n-order random graph 
    '''

    g = Graph({})
    g.add_vertices(n)
    for i in range(n):
        for j in range(i + 1, n):
            x = random.uniform(0, 1)
            if x <= edge_prob:
                g.add_edge(i, j, random.choice([1,-1]))
    return g
#
def random_graph_eds01(w = []):
    '''
    Returns an n-order random graph with expected degree sequence w. Due to Chung and Lu
    '''

    m = sum(w) + 0.0
    n = len(w)
    g = Graph({})
    g.add_vertices(n)
    for i in range(n):
        for j in range(i + 1, n):
            x = random.uniform(0, 1)
            edge_prob = w[i] * w[j] / m
            if x <= edge_prob:
                g.add_edge(i, j, 1)
    return g
#    
def random_graph_eds02(w = []):
    '''
    Returns an n-order random graph with expected degree sequence w. Due to Xu Xinping and Liu Feng
    '''

    m = sum(w) + 0.0
    n = len(w)
    z = m / n
    g = Graph({})
    g.add_vertices(n)
    for i in range(n):
        for j in range(i + 1, n):
            x = random.uniform(0, 1)
            edge_prob = (w[i] + w[j] - z) / n
            if x <= edge_prob:
                g.add_edge(i, j, 1)
    return g
#
def random_graph_kim(ds = []):
    '''
    Generate a random  graph with a given degree sequence ds using Kim et al.'s algorithm
    '''
    while True:
        if not isgraphical(list(ds))[0]:
            return None
        s = list(zip(ds, range(len(ds))))
        n = len(s)
        g = Graph({})
        g.add_vertices(n)
        while len(s):
            s.sort(reverse = True)
            v = random.randrange(len(s))
            d = s[v][0]
            perm = list(range(len(s)))
            perm.remove(v)
            random.shuffle(perm)
            for i in range(d):
                s[v] = (s[v][0] - 1, s[v][1])
                while len(perm) >= d:
                    s[perm[i]] = (s[perm[i]][0] - 1, s[perm[i]][1])
                    for j in range(len(s)):
                        if s[v][0] == 0:
                            break
                        if s[j][1] != s[v][1] and j not in perm[:i + 1]:
                            s[v] = (s[v][0] - 1, s[v][1])
                            s[j] = (s[j][0] - 1, s[j][1])
                    graphical = isgraphical(list(j[0] for j in s))
                    for j in range(len(s)):
                        if s[v][0] == d - i - 1:
                            break
                        if s[j][1] != s[v][1] and j not in perm[:i + 1]:
                            s[v] = (s[v][0] + 1, s[v][1])
                            s[j] = (s[j][0] + 1, s[j][1])
                    if graphical[0]:
                        g.add_edge(s[v][1], s[perm[i]][1], 1)
                        break
                    s[perm[i]] = (s[perm[i]][0] + 1, s[perm[i]][1])
                    perm.pop(i)
            if len(perm) < d:
                return None
            s.pop(v)
        if g.connectedness() == 1:
            return g

    #

#
def power_law_list(max_deg, beta, order):
    n = 0.0
    for i in range(1, max_deg + 1):
        n = n + i ** (-beta)
    alpha = int(order / n)
    d = []
    for i in range(1, max_deg + 1):
        for j in range(int(alpha * (i ** (-beta))) + 1):
            d.append(min(j, max_deg))
    k = []
    for i in range(0, order):
        if d[i] == 0:
            k.append(1)
        else:
            k.append(d[i])
    k.sort(reverse = True)
    return k
# 
def random_graph_ws(n=20,k =4 ,p = 0.05):
    '''
    Generates a random small world graph by the Watts-Strogatz model 
    Values for k: n>>k>>ln(n)
    Values for p: in order to have the small world property p needs to be between 0.01 and 0.1
    '''
    if k>=n or k< numpy.log(n):
        print( 'k to small/large')
        return
    if k%2==1:
        print('only even k allowed')
        return

    g=Graph({})
    g.add_vertices(2)
    #creating 
    while(g.connectedness()==0):
        g = Graph({})
        g.add_vertices(n)
        for i in range(n):
            for t in range(1,(k//2)+1):
                j=(i+t)%n
                g.add_edge(i,j,1)
                j=(i-t)%n
                g.add_edge(i,j,1)
        for t in range(1,(k//2)+1):
            for i in range(n//2):             
                if random.random() < p:        
                    j = random.randint(0,n-1)
                    while j == i:
                        j = random.randint(0,n-1)
                    g.remove_edge((i,((i+t)%n)))
                    g.add_edge(i,j,1)

    return g
#    
def random_tree(n=20):
    '''
    Generate a random Prufer sequence and then its tree
    '''
    p = []
    for i in range (n - 2):
        p.append(random.randint(0, n - 1))
    #print(p)
    g = prufer_tree(p)
    return g
#
def random_prufer_seq(n=10):
    '''
    Generate a random Prufer sequence and then its tree
    '''
    p = []
    for i in range (n - 2):
        p.append(random.randint(0, n - 1))
    return p

def random_weighted_graph(n, edge_prob, low_edge_weight, high_edge_weight):
    '''
    Returns an n-order random graph with random weights
    '''
    g = Graph({})
    g.add_vertices(n)
    for i in range(n):
        for j in range(i + 1, n):
            x = random.uniform(0, 1)
            w = random.choice(range(low_edge_weight, high_edge_weight))
            if x <= edge_prob:
                g.add_edge(i, j, w)
    return g
#
def self_complementary_graph(k):
    '''
    Returns a self complementary graph on 4k vertices
    '''
    if k <= 0:
        return None
    if k == 1:
        g = Graph({})
        g.add_vertices(4)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 2, 1)
        g.add_edge(2, 3, 1)
        return g
    else:
        g = self_complementary_graph(k - 1)
        S = g.vertices()
        V = g.add_vertices(4)
        g.add_edge(V[0], V[1], 1)
        g.add_edge(V[1], V[2], 1)
        g.add_edge(V[2], V[3], 1)
        for i in S:
            g.add_edge(V[1], S[i], 1)
            g.add_edge(V[2], S[i], 1)
        return g
#
def petersen_graph():
    g = Graph({})
    g.add_vertices(10)
    g.add_edge(0, 1, 1)
    g.add_edge(1, 2, 1)
    g.add_edge(2, 3, 1)
    g.add_edge(3, 4, 1)
    g.add_edge(4, 0, 1)
    g.add_edge(5, 0, 1)
    g.add_edge(6, 1, 1)
    g.add_edge(7, 2, 1)
    g.add_edge(8, 3, 1)
    g.add_edge(9, 4, 1)
    g.add_edge(5, 7, 1)
    g.add_edge(5, 8, 1)
    g.add_edge(6, 8, 1)
    g.add_edge(6, 9, 1)
    g.add_edge(7, 9, 1)
    return g
    
def heawood_graph():
    g = Graph({0: {1: 1, 13: 1, 5: 1}, 1: {0: 1, 2: 1, 10: 1}, 2: {1: 1, 3: 1, 7: 1}, 
    3: {2: 1, 4: 1, 12: 1}, 4: {3: 1, 5: 1, 9: 1}, 5: {4: 1, 6: 1, 0: 1}, 
    6: {5: 1, 7: 1, 11: 1}, 7: {6: 1, 8: 1, 2: 1}, 8: {7: 1, 9: 1, 13: 1}, 
    9: {8: 1, 10: 1, 4: 1}, 10: {9: 1, 11: 1, 1: 1}, 11: {10: 1, 12: 1, 6: 1}, 
    12: {11: 1, 13: 1, 3: 1}, 13: {12: 1, 0: 1, 8: 1}})
    return g
#
def complete_graph(n):
    g = Graph({})
    g.add_vertices(n)
    h = g.complement()
    return h
    return g
#
def read_graph(file):
    input = open(file, 'r')
    s = eval(input.readlines()[0])
    inputgraph = Graph(s)
    return inputgraph
#
def read_Adj_Matrix(file = 'E:\COURSES\CSE835\CSE835_Fall_2006\samplegraph.txt'):
    input = open(file, 'r')
    l = input.readlines()
    n = len(l)
    g = Graph({})
    g.add_vertices(n)
    for i in range(n):
        m = l[i]
        s = ''
        for c in m:
            if c != ' ' and c != '\n':
                s = s + c
            j = i + 1
            for c in s[i + 1:]:
                if int(c) ==1:
                    g.add_edge(i, j, 1)
                j = j + 1
    return g
#
def sim_tree(k = 500000, n = 13, m = 20, p = 0.5):
    '''
    Generating random graphs to find twin graphs of different edge sizes. Note that a 
    negative test for deciding whether a graph is self-complementary is to see if its 
    diameter is >=4.
    '''
    import sys
    c = 0
    #st = open('C:\PgOutput\SimTree.txt', 'a')
    st = open('C:\Documents and Settings\Esfahanian\Desktop\CourseWare\CSE835_Fall_2007\SampleGraphs\SpouseGraph.txt','a')
    for j in range(k):
        for i in range(n,m + 1, 1):
            g = random_graph(i,p)
            tg = g.spanning_trees_count()
            h = g.complement()
            th = h.spanning_trees_count()
            if (tg == th) and (g.size() != h.size()):
                print('The Graph is: ', g.g)
                print('Its order is: ', g.order())
                print('Its degree Sequence is: ', g.degree_sequence())
                print('Its distance list is: ', g.distance_list())
                print('Its count of spanning trees is : ', tg)
                print('------------------------------------------------------------')
                c = c + 1
    print('The number of such graphs is ', c)
    st.close()

#
def all_sub(n):
    '''
    Returns all binary patterns of length n
    Example: pg.all_sub(3) will return ['000', '001', '010', '011', '100', '101', '110', '111']
    '''
    if n == 0:
        return []
    if n == 1:
        return ['0', '1']
    else:
        L = []
        for x in all_sub(n - 1):
            L.append('0' + x)
            L.append('1' + x)
    L.sort()
    return L
#
def all_nq_sub(n,q):
    '''
    Returns all binary patterns of length n with q bit set to 1
    Example: pg.all_nq_sub(5, 3) will return ['00111', '01011', '01101', '01110', '10011', '10101', '10110', '11001', '11010', '11100']
    '''
    if n == 0:
        return []
    if q > n:
        return []
    if q == 0:
        return ['0' * int(n)]
    if n == q:
        return ['1' * int(q)]
    L = []
    for x in all_nq_sub(n - 1, q - 1):
        L.append('1' + x)
    for x in all_nq_sub(n - 1, q):
        L.append('0' + x)
    L.sort()
    return L
#
def gen_sub(l = [], k = 0):
    '''
    Returns all k-element subsets of list l
    '''
    n = len(l)
    h = all_nq_sub(n, k)
    sub = []
    for s in h:
        subtemp = []
        for i in zip(s, l):
            if i[0] == '1':
                subtemp.append(i[1])
        sub.append(subtemp)
        sub.sort()
    return sub
#
def gen_graph(n):
    '''
    Generates all labeled graphs on n vertices
    '''
    gl= []
    m = n * (n - 1) / 2
    L = all_sub(m)
    k = 0
    start = 0
    g = Graph({})
    for l in L:
        g.add_vertices(n)
        while start < m:
            for i in range(start + 1, n, 1):
                #print(start, i, k)
                if l[k] == '1':
                    g.add_edge(start, i, 1)
                k = k + 1
            start = start + 1
        gl.append(g.g)
        start = 0
        k = 0
        g = Graph({})
    return gl
#
def gen_nq_graphs(n, q, c = 1):
    '''
    Generates all labeled graphs on n vertices with q edges. by default we only need connected graphs
    '''
    gl= []
    m = n * (n - 1) / 2
    L = all_nq_sub(m, q)
    k = 0
    start = 0
    g = Graph({})
    for l in L:
        g.add_vertices(n)
        while start < m:
            for i in range(start + 1, n, 1):
                #print(start, i, k)
                if l[k] == '1':
                    g.add_edge(start, i, 1)
                k = k + 1
            start = start + 1
        if c == 1:
            if g.connectedness():
                gl.append(g.g)
        else:
            gl.append(g.g)
        start = 0
        k = 0
        g = Graph({})
    return gl
#
def prufer(n):
    '''
    Returns a list containing prufer sequences of length n-2; assumes n>=3
    '''
    if n <=2:
        return []
    l = []
    x = list(range(n))
    for p in itertools.product(x, repeat=(n-2)):
        l.append(p)
    return l
#
def prufer_tree(p = []):
    '''
    Decodes a Prufer Sequence, that is, it returns a tree
    '''
    n = len(p) + 2
    V = list(range(n))
    g = Graph({})
    g.add_vertices(n)
    while len(V) > 2:
        for i in V:
            if i not in p:
                break
        g.add_edge(i, p[0], 1)
        V.remove(i)
        p.remove(p[0])
    g.add_edge(V[0], V[1], 1)
    return g
#
def labeled_trees_leaf_count(n):
    '''
    Returns a list l, where l[i] is the number of 
    n-vertex labeled trees having i leaves
    '''
    k = prufer(n)
    nl = 0
    leafDis = [0]*n
    for tree in k:
        nl = 0
        for j in range(n):
            if j not in tree:
                nl +=1
        #print tree, nl
        leafDis[nl] +=1
    return leafDis
#
def isthereSpouseGraph(n):
    import sys
    st = open('C:\PgOutput\IsThere.txt','a')
    for i in range (1, n + 1, 1):
        L = gen_graph(i)
        for x in L:
            g = Graph(x)
            tg = g.spanning_trees_count()
            h = g.complement()
            th = h.spanning_trees_count()
            if (tg == th) and (g.distance_list() != h.distance_list()):
                print('The Graph is: ', g.g)
                print('Its order is: ', g.order())
                print('Its degree Sequence is: ', g.degree_sequence())
                print('Its distance list is: ', g.distance_list())
                print('Its count of spanning trees is : ', tg)
                print('------------------------------------------------------------')
#
def rel(n = 11): #It plots the prob of an (n + 1) wheel being functional
    '''
    It plots the prob of an (n + 1) wheel being functional (connected), where
    p is the prob of a node being reliable.
    '''
    import pylab
    import numpy
    p = numpy.arange(0, 1, 0.001)
    x = p + (1 - p) * (p ** n)
    r = 0
    for i in range(n - 1):
        r = n * p ** (n - i - 1) * (1 - p) ** (i + 2)
    r = r + x
    pylab.grid(True)
    pylab.plot(p, r, lw = 2)
    pylab.show()
#
def isgraphical(s = []):
    '''
    Tests if list s is graphical. Returns 1, and a graph if the answer
    is yes. Otherwise, it returns 0, and None. The algorithm builds the
    adjacency matrix one row at a time.
    Example [4,4, 1, 1, 1, 1] is not graphical whereas [4,4,4,4,2,2, 1, 1] is
    '''
    s.sort()
    s.reverse()
    from numpy import zeros
    n = len(s)
    w = zeros((n, n))
    r = 0
    #print(g)
    while len(s) > 1:
        s.sort()
        s.reverse()
        #print(s, '\n')
        #print(w, '\n') 
        if s[0] >= len(s):
            break
        for i in range(len(s)):
            w[r, n - 1 - i] = s[-i - 1]
        #print(w, '\n')
        for i in range(s[0]):
            s[i + 1] = s[i + 1] - 1
        del s[0]
        #print(s)
        r = r + 1
    if s[0] == 0:
        #print(s)
        #print('The sequence is graphical. Here is a sample graph:', '\n')
        A = zeros((n, n))
        G = {}
        for i in range(n - 1):
            r = w[n - i - 2] - w[n - 1 - i]
            #print(r)
            x = r[n - i - 1 :]
            #print(x)
            A[n - i - 2, n - i - 1 :] = x
            A[n - i - 1 :, n - i - 2] = x
            #print(A, '\n')
        for i in range(n):
                G[i] = {}
                for j in range(n):
                    if A[i, j] == 1:
                        G[i][j] = 1
        #print(G)
        return 1, Graph(G)
    else:
        #print('The sequecne is not graphical.')
        return 0, None
# Generating all the possible graphical sequences for (n, m) graphs
def gen_gs(n = 3, m = 2):
    import copy
    GS = []
    s = [[]]
    k = []
    q = n
    while (n - 1 >= 0):
        k = []
        for i in s:
            for j in range(q):
                k.append([j]+i)
        s = k
        n = n - 1
    #print('this is s: ', s)
    for list in s:
        sum = 0
        #print('this is list: ', list)
        for i in list:
            sum = sum + i
        #print(list, sum)
        if (sum == 2 * m):
            #print('this is list: ', list, sum)
            list.sort()
            #print('this is sorted list: ', list)
            list.reverse()
            #print('this is reverse list: ', list)
            #print(list)
            temp_list = copy.deepcopy(list)
            k = isgraphical(temp_list)
            #print(k)
            if (k[0] == 1):
                #print('this is error list: ', list)
                GS.append(list)
                #print(GS)
    setGS = []
    for seq in GS:
        if seq not in setGS:
            setGS.append(seq)
    return setGS
#        
def ave_tree_leaves(n = 10):
    '''
    It generates n-vertex trees k times and returns its average leaf count
    '''
    ave = 0
    k = int(0.02 * (n ** (n - 2)))
    k = 1000
    print(k)
    for i in range(k):
        g = random_tree(n)
        l = g.leaves()
        alc = float(len(l)) / n
        ave = ave + alc
    return ave / k
#
def cartesian(g,h):
    '''
    Returns the cartesian product of graphs g and h
    '''  
    F = Graph({})
    vg = g.vertices()
    vh = h.vertices()
    vF = list(itertools.product(vg,vh))
    ghF = {}
    n = len(vF)
    F.add_vertices_list(range(n))
    for i in range(len(vF)):
        ghF[vF[i]] = i
    #print(ghF)
    #adding edges in coies of h
    for i in vg:
        for edge in h.edges():
            endv0 = ghF[(i,edge[0])]
            endv1 = ghF[(i,edge[1])]
            F.add_edge(endv0, endv1,1)
    #adding edges between copies of h
    for edge in g.edges():
        u = edge[0]
        v = edge[1]
        for i in vh:
            F.add_edge(ghF[u,i], ghF[v,i], 1)
    return F
    
    
def fileProc(file = 'C:\\Users\Esfahanian\Desktop\CourseWare\CSE835_Spring_2009\SampleGraphs\dl_twins_order08.txt'):
    input = open(file, 'r')
    w = []
    total = 0
    for b in input.readlines():
        if len(b) == 0:
            break
        g = Graph(eval(b))
        h = g.complement()
        if g.spanning_trees_count() != h.spanning_trees_count():
            w.append(g.g)
            total = total + 1
            g.display()
    print("total is ", total)
    return w
#
def n2pg(file = 'C:\cygwin\home\Esfahanian\\nauty24\Myout.txt'):
    input = open(file, 'r')
    w = []
    for b in input.readlines():
        if len(b) == 0:
            break
        g = Graph(eval(b))
        l = g.degree_sequence()
        w.append(l)
        if l[0] == l[g.order() - 1]:
            print(l)
            #g.display()
    return w
#
def relp(x, y, z):
    '''
    failure probabilities in K_3
    '''
    allFailing = x * y * z
    oneFailing = (1 - x) * (1 - y) * z + (1 - z) * (1 - y) * x + (1 - x) * (1 - z) * y
    twoFailing = x * y * (1 - z) + z * y * (1 - x) + x * z * (1 - y)
    noneFailing = (1 - x) * (1 - y) * (1 - z)
    print('All failing = ', allFailing)
    print('One Faling = ', oneFailing)
    print('Two Failing = ', twoFailing)
    print('None Failing = ', noneFailing)
    print('Sum of all = ', allFailing + oneFailing + twoFailing + noneFailing)

def n_choose_m(n,m):
    '''
    Returns c(n,m); number of ways of selecting m objects
    out of n, with no replacement, where order is ignored.
    '''
    if n < m:
        return 0
    b =[0]*(n+1)
    b[0] = 1
    for i in range(1,n+1):
        b[i] = 1
        j = i - 1
        while j > 0:
            b[j] +=b[j - 1]
            j -=1
    return b[m]
    
def nx2pg(G):
    import networkx as nx
    import pg
    adjList = G.adjacency_list()
    order = G.order()
    g = pg.Graph({})
    k = list(range(order))
    g.add_vertices_list(k)
    for i in k:
        for j in adjList[i]:
            g.add_edge(i,j,1)
    return g
    
def nxRandom(n,p):
    import networkx as nx
    h = nx.fast_gnp_random_graph(n,p)
    adjList = h.adjacency_list()
    print(adjList)
    order = h.order()
    import pg
    g = pg.Graph({})
    k = list(range(order))
    g.add_vertices_list(k)
    for i in k:
        for j in adjList[i]:
            g.add_edge(i,j,1)
    return g.g
    
    
def counter(n = 1):
    for i in range(n):
        g = random_tree()
        k = g.edgeImpact()
        l = g.edgeIndex()
        a = k.pop()
        #print(a)
        b = l.pop()
        #print(b)
        edgeImpact = a[1]
        edgeIndex = b[1]
        g.remove_edge(edgeIndex)
        c = g.components()
        u = edgeImpact[0]
        v = edgeImpact[1]
        x = edgeIndex[0]
        y = edgeIndex[1]
        #print(c, u, v)
        if (u in c[0] and v in c[0]) or (u in c[1] and v in c[1]):
            print("conter example")
            g.add_edge(x,y,1)
            print(g.g)
            return

def counter01(n = 1):
    for i in range(n):
        g = random_tree()     
        h = copy.deepcopy(g)
        k = g.edgeImpact()
        a = k.pop()
        edgeImpact = a[1]
        u = edgeImpact[0]
        v = edgeImpact[1]
        cen = g.centerTree()
        #print(u, v, cen)
        if u in cen or v in cen:
            print('A center is high impact end vertex.')
            continue
        else:
            g.remove_vertices(cen)
            c = g.components()
            #print(c)
            if (u in c[0] and v in c[0]) or (u in c[1] and v in c[1]):
                print("conter example")
                print(h.g)
                return
    print("None found.")
#counter01()
def TreeLFD():
    g = random_tree()
    deg = g.degree_sequence()
    #print(deg)
    Md = deg[0]
    DF = []
    for i in range(1,Md +1):
        a = deg.count(i)
        DF.append((a,i))
    #print(DF)    
    DF.sort()
    print( DF[0])
#TreeLFD()
def eic():
    #g = random_graph(10, 0.3)
    g = random_tree(6)
    eI = g.edgeImpact().pop()
    edge = eI[1]
    g.add_edge(edge[0], edge[1],1)
    eI2 = g.edgeImpact().pop()
    g.remove_edge(edge)
    eI3 = g.edgeImpactSet(2).pop()
    if eI3[0] > eI[0] + eI2[0]:
        print(g.g)
    else:
        print("no CE")
        
def counter03(n = 20):
    for i in range(n):
        g = random_tree()
        k = g.edgeImpact()
        l = g.edgeIndexDistance()
        a = k.pop()
        #print(a)
        b = l.pop()
        #print(b)
        edgeImpact = a[1]
        edgeIndex = b[1]
        g.remove_edge(edgeIndex)
        c = g.components()
        u = edgeImpact[0]
        v = edgeImpact[1]
        x = edgeIndex[0]
        y = edgeIndex[1]
        print(c)
        print(u, v)
        if (u in c[0] and v in c[0]) or (u in c[1] and v in c[1]):
            print("conter example")
            g.add_edge(x,y,1)
            print(g.g)
            return
    return("No CE")
#counter03()

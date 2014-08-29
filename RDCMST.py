import timeit
import sys
from Graph import *
from unionfind import *
from IndexedMinHeap import *
from sets import Set

__author__ = 'zaimmusa'

class DFS:
    def __init__(self, tree, source_node):
        self.graph = tree
        self.visited = dict()
        for v in self.graph.nodes.keys():
            self.visited[v] = False

        # dictionary of path lengths - populated in recursion
        self.path_lenght = dict()
        self.path_lenght[source_node] = 0

        # list of pre order - populated in recursion
        self.pre_order = list()

        # list of pre order edges - populated in recution
        self.pre_order_edges = list()

        # list of post order - populated in recursion
        self.post_order = list()

        # list of tree leafs - populated in recursion
        self.leafs = set()

        # parent dictionary - populated in recursion
        self.parent = dict()

        # call recursively bfs
        self.dfs(source_node, source_node)
        self.post_order.append(source_node)
        self.parent[source_node] = source_node

    def dfs(self, node, parent_node):
        self.visited[node] = True
        self.pre_order.append(node)
        is_leaf = True
        for edge in self.graph.adj(node):
            a = edge.to
            if a == parent_node:
                continue
            if not self.visited[a]:
                is_leaf = False
                self.parent[a] = node
                self.pre_order_edges.append(edge)
                self.dfs(a, node)
                self.post_order.append(a)
            else:
                raise InputError("Graph is not a tree !!!")
        if is_leaf:
            self.leafs.add(node)

class LongestPath:
    def __init__(self, tree, root, function):
        try:
            self.dfs = DFS(tree, root)

            # determine heights of nodes
            self.height = dict()
            for v in self.dfs.post_order:
                if v in self.dfs.leafs:
                    self.height[v] = 0
                else:
                    self.height[v] = max([self.height[e.to] + function(e) for e in tree.adj(v) if e.to in self.height])

            # determine longest path not descendant of node
            self.lp_nd = dict()
            self.lp_nd[root] = 0
            for v in self.dfs.pre_order:
                if v != root:
                    p = self.dfs.parent[v]

                    # longest path through parents parent
                    lp_tpp = self.lp_nd[p] + function(tree.get_edge(p, v))

                    # longest path through sibling
                    siblings = [c for c in [e.to for e in tree.adj(p)] if c != self.dfs.parent[p] and c != v]

                    if len(siblings) == 0:
                        self.lp_nd[v] = lp_tpp
                    else:
                        lp_s = max([self.height[c] + function(tree.get_edge(p, c)) + function(tree.get_edge(p, v)) for c in siblings])
                        self.lp_nd[v] = max(lp_tpp, lp_s)

                    # print v, ' tpp', lp_tpp,  ' siblings : ', siblings , ' -> ' , self.lp_nd[v]

            # determine longest path
            self.lp = dict()
            for v in tree.nodes.keys():
                if v in self.lp_nd and v in self.height:
                    self.lp[v] = max(self.lp_nd[v], self.height[v])

        except InputError as e:
            print e.message

def Dijkstra(graph, source, function):
    X = Set()
    sp = dict()
    X.add(source)
    sp[source] = 0
    heap = IndexedMinHeap(graph.noNodes)
    for edge in graph.adj(source):
        if edge is not None:
            heap.insert(edge.to, function(edge))

    while (len(X) != graph.noNodes):

        if heap.is_empty():
            break

        path_length, to = heap.pop_key_and_index()

        X.add(to)
        sp[to] = path_length

        for edge in graph.adj(to):
            if edge.to not in X:
                path_to_a = path_length + function(graph.get_edge(to, edge.to))
                if not heap.contains(edge.to):
                    heap.insert(edge.to, path_to_a)
                elif path_to_a < heap.get_key(edge.to):
                    heap.changeKey(edge.to, path_to_a)

    return True, sp

def kruskal_based_heuristic(graph, root, B):
    """
    Kruskal based heuristic for solving RDCMST

    Input: graph, root node and B-delay constraint

    Output: Minimum Spanning Tree
    """
    E = set()

    # Stage 1

    # sort edges by cost, then by delay, then by node
    L_e = sorted(graph._allEdges(), key=lambda x: ( x.cost, x.delay, (x.node - graph.noNodes)%graph.noNodes))

    # TODO ovo se mora modificirati
    C = UnionFind()
    C.insert_objects(graph.nodes)

    # inicijalizirati minimalno kasnjenje
    solution_found, d_min = Dijkstra(graph, root, lambda x: x.delay)
    if not solution_found:
        print 'Unable to find d_min for the graph. Graph is not connected?'
        return
    print 'minimum delay per node'
    for v in d_min:
        print v, ' : ', d_min[v]

    # init
    delta = dict()
    p = dict()
    delta_max = dict()
    v_C = dict()

    for v in graph.get_vertices():
        delta[v] = d_min[v]
        p[v] = v
        delta_max[v] = 0
        v_C[v] = v

    number_of_components = graph.noNodes
    while number_of_components > 1 and len(L_e) > 0:
        e = L_e.pop(0)
        print '->', e
        u = e.node
        v = e.to

        if C.find(u) != C.find(v):
            D_u = B - (delta[u] + e.delay + delta_max[v])
            D_v = B - (delta[v] + e.delay + delta_max[u])
            if D_u >= 0 or D_v >= 0:
                if D_u >= D_v:
                    C_u_v = v_C[u]
                    delta[v] = delta[u] + e.delay
                    p[v] = u
                    root_of_subtree = v
                else:
                    C_u_v = v_C[v]
                    delta[u] = delta[v] + e.delay
                    root_of_subtree = u

                tree = create_graph(graph, E)
                dfs = DFS(tree, root_of_subtree)
                for edge in dfs.pre_order_edges:
                    delta[edge.to] = delta[edge.node] + edge.delay
                    p[edge.to] = edge.node

                # merge components
                E.add(e)
                C.union_left(C_u_v, v_C[u]) # ovaj union je drugaciji od standardnog uniona
                C.union_left(C_u_v, v_C[v]) #
                number_of_components -= 1

                # TODO popraviti ovaj dio
                # update delta_max[w] for w in C_u_v
                tree = create_graph(graph, [e for e in E if C.find(e.node) == C_u_v and C.find(e.to) == C_u_v])
                search = LongestPath(tree, C_u_v, lambda x: x.delay)
                for x in search.lp:
                    delta_max[x] = search.lp[x]

                # print all edges in current solution
                print '+ ', e
    # stage 1 finished
    print "Edges in a tree after Stage 1:"
    for e in E:
        print e

    # TODO Stage 2
    print "Stage 2"

    return E

def create_graph(graph, edges):
    new = Graph(graph.noNodes)
    for edge in edges:
        new.add(edge)
    return new



def readGraph(filename):
    noNodes = 0
    with open(filename) as f:
        for line in f:
            if (noNodes == 0):
                noNodes = int(line.split()[0])
                graph = Graph(noNodes)
            else:
                data = []
                for x in line.split():
                    data.append(int(x))
                if len(data) == 3:
                    edge = WeightedEdge(data[0], data[1], data[2])
                elif len(data) == 4:
                    edge = WeightedDelayedEdge(data[0], data[1], data[2], data[3])
                graph.add(edge)
    return graph

def main(filename, algorithm, parameters):
    start = timeit.default_timer()

    graph = readGraph(filename)

    if algorithm.lower() == 'dfs':
        for par in parameters:
            print 'parameter :', par
        try:
            dfs = DFS(graph, int(parameters[0]))
            stop = timeit.default_timer()

            print "pre order :", dfs.pre_order
            print "post order :", dfs.post_order
            print "tree leafs :", dfs.leafs
            print "parenting :"
            for v in dfs.parent:
                print v, ':', dfs.parent[v]
            print 'Running time' , stop - start
        except InputError as e:
            # TODO ovo bolje
            print e.message

    elif algorithm.lower() == 'lp_in_tree':
        for par in parameters:
            print 'parameter :', par
        lp = LongestPath(graph, int(parameters[0]), lambda e: e.cost)

        print 'Longest paths: '
        for v in lp.lp:
            print v, " : ", lp.lp[v]

    elif algorithm.lower() == 'kbh':
        for par in parameters:
            print 'parameter :', par
        rdcmst_edges = kruskal_based_heuristic(graph, int(parameters[0]), int(parameters[1]))
        print 'Edges in the tree: '
        for e in rdcmst_edges:
            print e
    elif algorithm.lower() == 'print':
        print 'Graph :'
        print graph
    else:
        print 'Unknown algorithm', algorithm

if __name__ == "__main__":

    print 'Input graph : ', sys.argv[1]
    print 'Algorithm : ', sys.argv[2]
    print 'Parameters : ', sys.argv[3:]


    main(sys.argv[1], sys.argv[2], sys.argv[3:])
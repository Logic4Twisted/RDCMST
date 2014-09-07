import timeit
import sys
from Graph import *
from unionfind import *
from IndexedMinHeap import *
from LongestPath import *
from sets import Set

__author__ = 'zaimmusa'

def Dijkstra(graph, source, function):
    X = Set()
    X.add(source)

    # shortest path length
    sortest_path_length = dict()
    sortest_path_length[source] = 0

    # edge on the path to source
    shortes_path_edges = dict()
    shortes_path_edges[source] = None
    active_edges = dict()

    heap = IndexedMinHeap(graph.noNodes)
    for edge in graph.adj(source):
        if edge is not None:
            heap.insert(edge.to, function(edge))
            active_edges[edge.to] = edge

    while (len(X) != graph.noNodes):

        if heap.is_empty():
            break

        path_length, to = heap.pop_key_and_index()

        X.add(to)
        sortest_path_length[to] = path_length
        shortes_path_edges[to] = active_edges[to]

        for edge in graph.adj(to):
            if edge.to not in X:
                path_to_a = path_length + function(graph.get_edge(to, edge.to))
                if not heap.contains(edge.to):
                    heap.insert(edge.to, path_to_a)
                    active_edges[edge.to] = edge
                elif path_to_a < heap.get_key(edge.to):
                    heap.change_key(edge.to, path_to_a)
                    active_edges[edge.to] = edge

    return True, sortest_path_length, shortes_path_edges

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
    solution_found, d_min, sp_edges = Dijkstra(graph, root, lambda x: x.delay)
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

        if e not in E and C.find(u) != C.find(v):
            D_u = B - (delta[u] + e.delay + delta_max[v])
            D_v = B - (delta[v] + e.delay + delta_max[u])
            if D_u >= 0 or D_v >= 0:
                if D_u >= D_v:
                    #C_u_v = v_C[u]
                    C_u_v = C.find(u)
                    delta[v] = delta[u] + e.delay
                    p[v] = u
                    root_of_subtree = v
                else:
                    #C_u_v = v_C[v]
                    C_u_v = C.find(v)
                    delta[u] = delta[v] + e.delay
                    p[u] = v
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
                tree = create_graph(graph, [x for x in E if C.find(x.node) == C_u_v and C.find(x.to) == C_u_v])
                search = LongestPath(tree, C_u_v, lambda x: x.delay)
                for x in search.lp:
                    delta_max[x] = search.lp[x]

                # print all edges in current solution
                print '+ ', e
    # stage 1 finished
    print "Edges in a tree after Stage 1:"
    for e in E:
        print e

    print
    print "********* Stage 2 *********"
    print

    C_s = C.find(root)
    print 'C_s = ', C_s
    if number_of_components > 1:
        for i in graph.get_vertices():
            C_i = C.find(i)
            if C_i != C_s:
                print 'Node ',  i, ' in component ', C_i, ' not connected to root. Subtree root =', v_C[C_i]
                path_to_C_i = get_path(sp_edges, root, v_C[C_i])
                path_to_C_i.reverse()

                print 'path from ', v_C[C_i] , ' to ', root, ' : '
                for edge in path_to_C_i:
                    print edge

                # finds last u such that d_min[u] = delta[u]
                u = root
                for edge in path_to_C_i:
                    if d_min[edge.to] == delta[edge.to]:
                        u = edge.to
                    else:
                        break
                print 'u = ', u

                path_to_u = get_path(sp_edges, u, v_C[C_i])
                path_to_u.reverse()

                for edge in path_to_u:
                    assert d_min[edge.node] < d_min[edge.to]
                    print edge.node, edge.to, p[edge.to]
                    if p[edge.to] != edge.to and p[edge.to] != edge.node:
                        E.add(edge)
                        print 'add edge ', edge
                        edge_to_remove = graph.get_edge(p[edge.to], edge.to)
                        print 'edge to remove ', edge_to_remove
                        E.remove(edge_to_remove)
                        # TODO treba li ovdje update delta[edge.to] i p[edge.to] ???
                    if edge.to == v_C[C_i]:
                        print '!!! mislim da i ovdje treba dodati edge u skup rjesenja'
                        E.add(edge)
                        print 'add edge ', edge
                        p[edge.to] = edge.node
                print
    return E

def get_path(sp_edges, root, destination):
    path = list()
    if destination == root or sp_edges[destination] is None:
        return path
    edge = sp_edges[destination]
    path.append(edge)
    if edge.node != root:
        path.extend(get_path(sp_edges, root, edge.node))
    return path

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
        print '_'*50
        print 'Edges in the tree: '
        for e in rdcmst_edges:
            print e
        print 'Total cost :', sum(map(lambda x: x.cost, rdcmst_edges))
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
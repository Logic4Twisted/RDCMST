from Graph import *

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
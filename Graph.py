__author__ = 'zaimmusa'

class WeightedEdge:
    def __init__(self, node, to, cost):
        self.node = node
        self.to = to
        self.cost = cost

    def __str__(self):
        return 'Edge from ' + str(self.node) + ' to ' + str(self.to) + ' cost is ' + str(self.cost)

    def reverse(self):
        return WeightedEdge(self.to, self.node, self.cost)

    def __lt__(self, other):
        return self.cost < other.cost

    def __gt__(self, other):
        return other.__lt__(self)

class WeightedDelayedEdge (WeightedEdge):
    def __init__(self, node, to, cost, delay):
        self.node = node
        self.to = to
        self.cost = cost
        self.delay = delay

    def __str__(self):
        return 'Edge from ' + str(self.node) + ' to ' + str(self.to) + ' cost is ' + str(self.cost) + ' delay is ' + str(self.delay)

    def reverse(self):
        return WeightedDelayedEdge(self.to, self.node, self.cost, self.delay)

class InputError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class Graph:
    def __init__(self, noNodes):
        self.noNodes = noNodes
        self.noEdges = 0
        self.nodes = {}
        for n in range(1, noNodes + 1):
            self.nodes[n] = set()

    def add(self, edge):
        self.nodes[edge.node].add(edge)
        self.nodes[edge.to].add(edge.reverse())
        self.noEdges += 1

    def __str__(self):
        result = 'Number of nodes: ' + str(self.noNodes) + '\n'
        result += 'Number of edges: ' + str(self.noEdges) + '\n'
        for n in self.nodes.keys():
            for edge in self.nodes[n]:
                result += edge.__str__() + '\n'
        return result

    def adj(self, node):
        adj = []
        for x in self.nodes[node]:
            adj.append(x)
        return adj

    def _allEdges(self):
        alledges = list()
        for node in self.nodes:
            alledges.extend(self.adj(node))
        return alledges

    def get_edge(self, node1, node2):
        if node1 not in self.nodes:
            return None
        for edge in self.nodes[node1]:
            if edge.to == node2:
                return edge
        return None

    def get_vertices(self):
        return self.nodes.keys()

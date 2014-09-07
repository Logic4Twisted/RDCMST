from graph.Graph import Graph, WeightedEdge
from graph.LongestPath import LongestPath
import unittest

__author__ = 'zaimmusa'

class TestLongestPath(unittest.TestCase):

    def setUp(self):
        self.graph = Graph(5)

    def test_unweighted_chain(self):
        self.graph = Graph(5)
        self.graph.add(WeightedEdge(1,2,1))
        self.graph.add(WeightedEdge(2,3,1))
        self.graph.add(WeightedEdge(3,4,1))
        self.graph.add(WeightedEdge(4,5,1))

        search = LongestPath(self.graph, 1, lambda x: x.cost)
        self.assertEqual(search.lp[1], 4)
        self.assertEqual(search.lp[2], 3)
        self.assertEqual(search.lp[3], 2)
        self.assertEqual(search.lp[4], 3)
        self.assertEqual(search.lp[5], 4)

    def test_unweighted_basic_tree_1(self):
        self.graph = Graph(5)
        self.graph.add(WeightedEdge(1,2,1))
        self.graph.add(WeightedEdge(2,3,1))
        self.graph.add(WeightedEdge(3,4,1))
        self.graph.add(WeightedEdge(2,5,1))

        search = LongestPath(self.graph, 1, lambda x: x.cost)
        self.assertEqual(search.lp[1], 3)
        self.assertEqual(search.lp[2], 2)
        self.assertEqual(search.lp[3], 2)
        self.assertEqual(search.lp[4], 3)
        self.assertEqual(search.lp[5], 3)

    def test_unweighted_basic_tree_2(self):
        self.graph = Graph(5)
        self.graph.add(WeightedEdge(1,2,1))
        self.graph.add(WeightedEdge(2,3,1))
        self.graph.add(WeightedEdge(2,4,1))
        self.graph.add(WeightedEdge(2,5,1))

        search = LongestPath(self.graph, 1, lambda x: x.cost)
        self.assertEqual(search.lp[1], 2)
        self.assertEqual(search.lp[2], 1)
        self.assertEqual(search.lp[3], 2)
        self.assertEqual(search.lp[4], 2)
        self.assertEqual(search.lp[5], 2)

    def test_unweighted_tree_1(self):
        self.graph = Graph(17)
        self.graph.add(WeightedEdge(1,2,1))
        self.graph.add(WeightedEdge(2,3,1))
        self.graph.add(WeightedEdge(2,4,1))
        self.graph.add(WeightedEdge(3,12,1))
        self.graph.add(WeightedEdge(12,13,1))
        self.graph.add(WeightedEdge(12,14,1))
        self.graph.add(WeightedEdge(12,15,1))
        self.graph.add(WeightedEdge(15,16,1))
        self.graph.add(WeightedEdge(15,17,1))
        self.graph.add(WeightedEdge(4,5,1))
        self.graph.add(WeightedEdge(4,6,1))
        self.graph.add(WeightedEdge(5,7,1))
        self.graph.add(WeightedEdge(5,8,1))
        self.graph.add(WeightedEdge(5,9,1))
        self.graph.add(WeightedEdge(6,10,1))
        self.graph.add(WeightedEdge(10,11,1))


        search = LongestPath(self.graph, 12, lambda x: x.cost)
        self.assertEqual(search.lp[1], 5)
        self.assertEqual(search.lp[2], 4)
        self.assertEqual(search.lp[3], 5)
        self.assertEqual(search.lp[4], 5)
        self.assertEqual(search.lp[5], 6)
        self.assertEqual(search.lp[6], 6)
        self.assertEqual(search.lp[7], 7)
        self.assertEqual(search.lp[8], 7)
        self.assertEqual(search.lp[9], 7)
        self.assertEqual(search.lp[10], 7)
        self.assertEqual(search.lp[11], 8)
        self.assertEqual(search.lp[12], 6)
        self.assertEqual(search.lp[13], 7)
        self.assertEqual(search.lp[14], 7)
        self.assertEqual(search.lp[15], 7)
        self.assertEqual(search.lp[16], 8)
        self.assertEqual(search.lp[17], 8)

    def test_unweighted_tree_1(self):
        self.graph = Graph(17)
        self.graph.add(WeightedEdge(1,2,2))
        self.graph.add(WeightedEdge(2,3,2))
        self.graph.add(WeightedEdge(2,4,2))
        self.graph.add(WeightedEdge(3,12,1))
        self.graph.add(WeightedEdge(12,13,1))
        self.graph.add(WeightedEdge(12,14,1))
        self.graph.add(WeightedEdge(12,15,1))
        self.graph.add(WeightedEdge(15,16,1))
        self.graph.add(WeightedEdge(15,17,2))
        self.graph.add(WeightedEdge(4,5,1))
        self.graph.add(WeightedEdge(4,6,1))
        self.graph.add(WeightedEdge(5,7,1))
        self.graph.add(WeightedEdge(5,8,2))
        self.graph.add(WeightedEdge(5,9,1))
        self.graph.add(WeightedEdge(6,10,2))
        self.graph.add(WeightedEdge(10,11,1))


        search = LongestPath(self.graph, 11, lambda x: x.cost)
        self.assertEqual(search.lp[1], 8)
        self.assertEqual(search.lp[2], 6)
        self.assertEqual(search.lp[3], 8)
        self.assertEqual(search.lp[4], 8)
        self.assertEqual(search.lp[5], 9)
        self.assertEqual(search.lp[6], 9)
        self.assertEqual(search.lp[7], 10)
        self.assertEqual(search.lp[8], 11)
        self.assertEqual(search.lp[9], 10)
        self.assertEqual(search.lp[10], 11)
        self.assertEqual(search.lp[11], 12)
        self.assertEqual(search.lp[12], 9)
        self.assertEqual(search.lp[13], 10)
        self.assertEqual(search.lp[14], 10)
        self.assertEqual(search.lp[15], 10)
        self.assertEqual(search.lp[16], 11)
        self.assertEqual(search.lp[17], 12)

    def test_weighted_chain(self):
        self.graph = Graph(5)
        self.graph.add(WeightedEdge(1,2,5))
        self.graph.add(WeightedEdge(2,3,3))
        self.graph.add(WeightedEdge(3,4,7))
        self.graph.add(WeightedEdge(2,5,6))

        search = LongestPath(self.graph, 1, lambda x: x.cost)
        self.assertEqual(search.lp[1], 15)
        self.assertEqual(search.lp[2], 10)
        self.assertEqual(search.lp[3], 9)
        self.assertEqual(search.lp[4], 16)
        self.assertEqual(search.lp[5], 16)


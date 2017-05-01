RDCMST
======
Application that solves

Rooted Delay Constrained Minimum Spanning Tree Problem:

Problem definition:
Given an undirected graph G = (V, E) with cost and delay for every edge
,source node in V and delay bound B find MST such that very node from
V has a path to source node that is bounded by B (path using edges in tree).

implemented so far:
- Longest path in a tree algorithm (linear time)
- IndexedMinHeap.py Binary heap that has indexed items (idea from Algorithms 4 book by Sedgewick)
- RDCMST Kruskal based heuristic by Mario Ruthmaier

Usage :

python RDCMST.py graph_file ['dfs', 'lp_in_tree', 'kbh', 'print'] [parameters to algorithm root and maximum delay if kbh]

for example 

python RDCMST.py data/example_1.txt kbh 1 4


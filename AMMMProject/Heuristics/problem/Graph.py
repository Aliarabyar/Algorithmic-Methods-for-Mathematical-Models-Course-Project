'''
AMMM Project

Ali Arabyarmohammadi

Based on AMMM Lab Heuristics.
Copyright 2020 Luis Velasco.
'''
from Heuristics.problem.Node import Node


class Graph:
    def __init__(self):
        self.nodes = {}
        self.numNodes = 0

    def __iter__(self):
        return iter(self.nodes.values())

    def getNode(self, n):
        if n in self.nodes:
            return self.nodes[n]
        else:
            return None

    def getNodes(self):
        return self.nodes.keys()

    def addNode(self, node):
        self.numNodes = self.numNodes + 1
        new_vertex = Node(node)
        self.nodes[node] = new_vertex
        return new_vertex

    def addArc(self, frm, to, cost=0):
        if frm not in self.nodes:
            self.addNode(frm)
        if to not in self.nodes:
            self.addNode(to)

        self.nodes[frm].addAdjacent(self.nodes[to], cost)
        self.nodes[to].addAdjacent(self.nodes[frm], cost)

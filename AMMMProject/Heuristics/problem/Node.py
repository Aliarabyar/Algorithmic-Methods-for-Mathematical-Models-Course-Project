'''
AMMM Project

Ali Arabyarmohammadi

Based on AMMM Lab Heuristics.
Copyright 2020 Luis Velasco.
'''

class Node:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def addAdjacent(self, nod, cost=0):
        self.adjacent[nod.id] = cost

    def getAdjacent(self):
        return self.adjacent.keys()

    def getId(self):
        return self.id

    def getWeight(self, node):
        return self.adjacent[node]
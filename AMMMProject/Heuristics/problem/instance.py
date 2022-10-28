'''
AMMM Project

Ali Arabyarmohammadi

Based on AMMM Lab Heuristics.
Copyright 2020 Luis Velasco.
'''

from Heuristics.problem.Graph import Graph
from Heuristics.problem.solution import Solution
import numpy as np


class Instance(object):
    def __init__(self, config, inputData):
        self.config = config
        self.inputData = inputData
        self.n = inputData.n
        self.m = inputData.m

        GrG = Graph()
        G = self.MakeImageGraph(GrG, inputData)
        GrH = Graph()
        H = self.MakeShapeGraph(GrH, inputData)

        self.G = G
        self.H = H

    def createSolution(self):
        solution = Solution(self.G, self.H)
        solution.setVerbose(self.config.verbose)
        return solution

    def MakeShapeGraph(self, H, inputData):
        H = Graph()
        for x in range(self.m):
            H.addNode(x + 1)
        x = 1
        for i in inputData.H:
            y = 1
            for item in np.array(list(i)):
                if item > 0:
                    H.addArc(x, y, item)
                y += 1
            x += 1
        return H

    def MakeImageGraph(self, G, inputData):
        G = Graph()
        for x in range(self.n):
            G.addNode(x + 1)
        x = 1
        for i in inputData.G:
            y = 1
            for item in np.array(list(i)):
                if item > 0:
                    G.addArc(x, y, item)
                y += 1
            x += 1
        return G

    def checkInstance(self):

        if self.n < self.m:
            return False

        numArcG = 0
        for n in self.G.getNodes():
            adjacent = self.G.getNode(n).getAdjacent()
            numArcG += len(adjacent)

        numArcH = 0
        for n in self.H.getNodes():
            get_adjacent = self.H.getNode(n).getAdjacent()
            numArcH += len(get_adjacent)

        if numArcG < numArcH:
            return False

        if len(self.G.nodes) == 0:
            return False

        if len(self.H.nodes) == 0:
            return False

        return True

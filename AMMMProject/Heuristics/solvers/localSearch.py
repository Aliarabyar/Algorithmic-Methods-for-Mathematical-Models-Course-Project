'''
AMMM Project

Ali Arabyarmohammadi

Based on AMMM Lab Heuristics.
Copyright 2020 Luis Velasco.
'''

from Heuristics.solver import _Solver
from AMMMGlobals import AMMMException
import copy
import time
import math



class Move(object):
    def __init__(self, ShapeNode, currentNodeImage, newNodeImage):
        self.newNodeImage = newNodeImage
        self.currentNodeImage = currentNodeImage
        self.nodeShape = ShapeNode


class LocalSearch(_Solver):
    def __init__(self, config, instance):
        self.enabled = config.localSearch
        self.nhStrategy = config.neighborhoodStrategy
        self.policy = config.policy
        self.maxExecTime = config.maxExecTime
        super().__init__(config, instance)

    def sortedByDegreeAsc(self):
        ArcNum = {}
        for xy in self.instance.H.getNodes():
            adjacent = self.instance.H.nodes[xy].getAdjacent()
            ArcNum[xy] = len(adjacent)
        return sorted(ArcNum.items(), key=lambda x: x[1], reverse=True)

    def evaluateNeighbor(self, solution, moves):
        matched = copy.deepcopy(solution.matched)
        for move in moves:
            if not solution.chechFeasByIsomorphismCond(self.instance.H.nodes[move.nodeShape],
                                                       self.instance.G.nodes[move.newNodeImage]):
                return math.inf, matched
            matched[move.nodeShape] = move.newNodeImage
        weightNew = self.fullMatchingCost(matched)
        return weightNew, matched

    def exploreExchange(self, solution):
        bestNeighbor = solution
        ShapeSortedArcs = self.sortedByDegreeAsc()
        currCost = solution.getFitness()

        for nodeShape in ShapeSortedArcs:
            nodeShape = nodeShape[0]
            for NodeImage in range(self.instance.G.numNodes):
                NodeImage = NodeImage + 1
                if NodeImage in solution.matched.values():
                    continue
                moves = [Move(nodeShape, solution.matched[nodeShape], NodeImage)]
                newWeight, newMatch = self.evaluateNeighbor(solution, moves)
                if newMatch is None:
                    raise AMMMException('[exploreExchange] No neighbouring solution could be created')
                if currCost > newWeight:
                    if self.policy == 'FirstImprovement':
                        bestNeighbor.matched = newMatch
                        return bestNeighbor
                    else:
                        bestNeighbor.matched = newMatch
                        currCost = newWeight
        return bestNeighbor

    def fullMatchingCost(self, matching):
        weight = 0
        for ShapeAdj, ImgAdj in matching.items():
            for nodeHIndex, nodeGIndex in matching.items():
                if ShapeAdj not in list(self.instance.H.nodes[nodeHIndex].adjacent.keys()) \
                        or ImgAdj not in list(self.instance.G.nodes[nodeGIndex].adjacent.keys()):
                    localWeight = 0
                else:
                    localWeight = abs(self.instance.G.nodes[nodeGIndex].getWeight(ImgAdj) - self.instance.H.nodes[
                        nodeHIndex].getWeight(ShapeAdj))
                weight = weight + localWeight
        return weight

    def exploreNeighborhood(self, solution):
        if self.nhStrategy == 'Reassignment':
            return self.exploreReassignment(solution)
        else:
            raise AMMMException('Unsupported NeighborhoodStrategy(%s)' % self.nhStrategy)

    def solve(self, **kwargs):
        initialSolution = kwargs.get('solution', None)
        if initialSolution is None:
            raise AMMMException('[local search] No solution could be retrieved')

        if not initialSolution.isFeasible():
            return initialSolution
        self.startTime = kwargs.get('startTime', None)
        endTime = kwargs.get('endTime', None)

        incumbent = initialSolution
        incumbentCost = incumbent.getCost()
        iterations = 0

        # keep iterating while improvements are found
        while time.time() < endTime:
            iterations += 1
            neighbor = self.exploreNeighborhood(incumbent)
            if neighbor is None: break
            neighborCost = neighbor.getFitness()
            if incumbentCost <= neighborCost: break
            incumbent = neighbor
            incumbentCost = neighborCost

        return incumbent


# Implementation of a local search using one neighborhood and two different policies.
class LocalSearch(_Solver):
    def __init__(self, config, instance):
        self.enabled = config.localSearch
        self.nhStrategy = config.neighborhoodStrategy
        self.policy = config.policy
        self.maxExecTime = config.maxExecTime
        super().__init__(config, instance)

    def sortedByDegreeAsc(self):
        ArcNum = {}
        for xy in self.instance.H.getNodes():
            adjacent = self.instance.H.nodes[xy].getAdjacent()
            ArcNum[xy] = len(adjacent)
        return sorted(ArcNum.items(), key=lambda x: x[1], reverse=True)

    def evaluateNeighbor(self, solution, moves):
        matched = copy.deepcopy(solution.matched)
        for move in moves:
            if not solution.chechFeasByIsomorphismCond(self.instance.H.nodes[move.nodeShape],
                                                       self.instance.G.nodes[move.newNodeImage]):
                return math.inf, matched
            matched[move.nodeShape] = move.newNodeImage
        weightNew = self.fullMatchingCost(matched)
        return weightNew, matched

    def exploreReassignment(self, solution):
        bestNeighbor = solution
        ShapeSortedArcs = self.sortedByDegreeAsc()
        currCost = solution.getFitness()

        for nodeShape in ShapeSortedArcs:
            nodeShape = nodeShape[0]
            for NodeImage in range(self.instance.G.numNodes):
                NodeImage = NodeImage + 1
                if NodeImage in solution.matched.values():
                    continue
                moves = [Move(nodeShape, solution.matched[nodeShape], NodeImage)]
                newWeight, newMatch = self.evaluateNeighbor(solution, moves)
                if newMatch is None:
                    raise AMMMException('[exploreExchange] No neighbouring solution could be created')
                if currCost > newWeight:
                    if self.policy == 'FirstImprovement':
                        bestNeighbor.matched = newMatch
                        return bestNeighbor
                    else:
                        bestNeighbor.matched = newMatch
                        currCost = newWeight
        return bestNeighbor

    def fullMatchingCost(self, matching):
        weight = 0
        for ShapeAdj, ImgAdj in matching.items():
            for nodeHIndex, nodeGIndex in matching.items():
                if ShapeAdj not in list(self.instance.H.nodes[nodeHIndex].adjacent.keys()) \
                        or ImgAdj not in list(self.instance.G.nodes[nodeGIndex].adjacent.keys()):
                    localWeight = 0
                else:
                    localWeight = abs(self.instance.G.nodes[nodeGIndex].getWeight(ImgAdj) - self.instance.H.nodes[
                        nodeHIndex].getWeight(ShapeAdj))
                weight = weight + localWeight
        return weight

    def exploreNeighborhood(self, solution):
        if self.nhStrategy == 'Reassignment':
            return self.exploreReassignment(solution)
        else:
            raise AMMMException('Unsupported NeighborhoodStrategy(%s)' % self.nhStrategy)

    def solve(self, **kwargs):
        initialSolution = kwargs.get('solution', None)
        if initialSolution is None:
            raise AMMMException('[local search] No solution could be retrieved')

        if not initialSolution.isFeasible():
            return initialSolution
        self.startTime = kwargs.get('startTime', None)
        endTime = kwargs.get('endTime', None)

        incumbent = initialSolution
        incumbentCost = incumbent.getFitness()
        iterations = 0

        # keep iterating while improvements are found
        while time.time() < endTime:
            iterations += 1
            neighbor = self.exploreNeighborhood(incumbent)
            if neighbor is None: break
            neighborCost = neighbor.getFitness()
            if incumbentCost <= neighborCost: break
            incumbent = neighbor
            incumbentCost = neighborCost

        return incumbent

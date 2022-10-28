'''
AMMM Project

Ali Arabyarmohammadi

Based on AMMM Lab Heuristics.
Copyright 2020 Luis Velasco.
'''

import random, time
from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch


# Inherits from the parent abstract solver.
class Solver_Greedy(_Solver):

    def _selectCandidate(self, candidateList):
        if self.config.solver == 'Greedy':
            # sort candidate assignments by weights in ascending order
            sortedCandidateList = sorted(candidateList.items(), key=lambda x: x[1])
            # choose assignment with minimum weight
            return sortedCandidateList[0]
        return random.choice(candidateList)

    def sortedByDegreeAsc(self):
        ArcNum = {}
        for xy in self.instance.H.getNodes():
            adjacent = self.instance.H.nodes[xy].getAdjacent()
            ArcNum[xy] = len(adjacent)

        return sorted(ArcNum.items(), key=lambda x: x[1], reverse=True)

    def construction(self):
        solution = self.instance.createSolution()
        ShapeSortedArcs = self.sortedByDegreeAsc()
        for x in ShapeSortedArcs:
            x = x[0]
            candidateList = {}
            for v in range(self.instance.G.numNodes):
                v = v + 1
                if not solution.chechFeasByIsomorphismCond(self.instance.H.nodes[x],
                                                           self.instance.G.nodes[v]) or v in solution.matched.values():
                    continue
                else:
                    ng = self.instance.G.nodes[v]
                    nh = self.instance.H.nodes[x]
                    candidateList[v] = solution.CalcWeightDiff(ng, nh)
            if len(candidateList) == 0:
                solution.makeInfeasible()
                break
            else:
                bestCandidate = self._selectCandidate(candidateList)
                solution.assign(self.instance.G.getNode(bestCandidate[0]), self.instance.G.nodes[x])
                solution.cost = round(solution.cost + bestCandidate[1], 3)
        return solution

    def solve(self, **kwargs):
        self.startTimeMeasure()

        solver = kwargs.get('solver', None)
        if solver is not None:
            self.config.solver = solver
        localSearch = kwargs.get('localSearch', None)
        if localSearch is not None:
            self.config.localSearch = localSearch

        self.writeLogLine(float('inf'), 0)

        solution = self.construction()
        if self.config.localSearch:
            localSearch = LocalSearch(self.config, self.instance)
            endTime = self.startTime + self.config.maxExecTime
            solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

        self.elapsedEvalTime = time.time() - self.startTime
        self.writeLogLine(solution.getFitness(), 1)
        self.numSolutionsConstructed = 1
        self.printPerformance()

        return solution

'''
AMMM Project

Ali Arabyarmohammadi

Based on AMMM Lab Heuristics.
Copyright 2020 Luis Velasco.
'''

import random
import time
import numpy as np
from Heuristics.solver import _Solver
from Heuristics.solvers.localSearch import LocalSearch


# Inherits from the parent abstract solver.
class Solver_GRASP(_Solver):

    def _selectCandidate(self, candidateList, alpha):

        # Calculate the boundary highest load as a function of the
        # lowest and greatest loads, as well as the alpha parameter.
        candidateList = {k: candidateList[k] for k in sorted(candidateList, key=candidateList.get)}
        boundaryCost = list(candidateList.values())[0] + (
                    list(candidateList.values())[-1] - list(candidateList.values())[0]) * alpha

        maxIndex = 0
        for ImgNome in candidateList:  # Locate the items in RCL range.
            if candidateList[ImgNome] <= boundaryCost:
                maxIndex += 1

        # Generate RCL and randomly select an item
        if maxIndex == 0:
            RCL_Id = 0
        else:
            RCL_Id = random.choice(list(range(maxIndex)))
        return list(candidateList.items())[RCL_Id]

    def sortedByDegreeAsc(self):
        ArcNum = {}
        for xy in self.instance.H.getNodes():
            adjacent = self.instance.H.nodes[xy].getAdjacent()
            ArcNum[xy] = len(adjacent)
        return sorted(ArcNum.items(), key=lambda x: x[1], reverse=True)

    def _greedyRandomizedConstruction(self, alpha):
        # get an empty solution for the problem
        solution = self.instance.createSolution()
        ShapeSortedArcs = self.sortedByDegreeAsc()
        for NodeShape in ShapeSortedArcs:
            costs = {}
            for nodeImage in range(self.instance.G.numNodes):
                nodeImage = nodeImage + 1
                matched = solution.matched.values()
                FeasCond = solution.chechFeasByIsomorphismCond(self.instance.H.nodes[NodeShape[0]],
                                                               self.instance.G.nodes[nodeImage])
                if not FeasCond or nodeImage in matched:
                    continue
                else:
                    nodeSh = self.instance.H.nodes[NodeShape[0]]
                    nodeImg = self.instance.G.nodes[nodeImage]
                    costs[nodeImage] = solution.CalcWeightDiff(nodeImg, nodeSh)
            if len(costs) == 0:
                solution.makeInfeasible()
                break
            else:
                selectedCandidates = self._selectCandidate(costs, alpha)
                SelectedCandImage = self.instance.G.nodes[selectedCandidates[0]]
                selectedCandShape = self.instance.H.nodes[NodeShape[0]]
                solution.assign(SelectedCandImage, selectedCandShape)
                solution.cost = round(solution.cost + selectedCandidates[1], 3)
        return solution

    def GetListOfAlpha(self, alphatuning,times):
        if alphatuning:
            # Make a list of alpha * times
            aRange =  np.arange(0.0, 1.1, 0.1)
            listOfAlpha = np.tile(aRange, times)
        else:
            listOfAlpha = [self.config.alpha]
        return listOfAlpha


    def stopCriteria(self):
        self.elapsedEvalTime = time.time() - self.startTime
        if self.elapsedEvalTime > self.config.maxExecTime:
            return True
        else:
            return False


    def solve(self, **kwargs):

        alphatuning = False  # please change 'alphatuning' to True in order to alpha tuning
         # The GRASP algorithm has been executed 2 times
        # per instance, using different alpha values
        listOfAlpha = self.GetListOfAlpha(alphatuning,2)
        costs = {}
        for alpha_ref in listOfAlpha:
            self.startTimeMeasure()
            incumbent = self.instance.createSolution()
            incumbent.makeInfeasible()
            bestMinCostLimit = 1000

            iteration = 0
            stopCriteria = False
            while not stopCriteria:
                stopCriteria = self.stopCriteria()
                iteration += 1

                # force first iteration as a Greedy execution (alpha == 0)
                alpha = 0 if iteration == 1 else alpha_ref

                solution = self._greedyRandomizedConstruction(alpha)
                if self.config.localSearch:
                    localSearch = LocalSearch(self.config, None)
                    endTime = self.startTime + self.config.maxExecTime
                    solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

                if solution.isFeasible():
                    solutionGetFitness = solution.SolutiongetFitness()
                    if solutionGetFitness < bestMinCostLimit:
                        count = 0
                        incumbent = solution  # best current solution
                        bestMinCostLimit = solutionGetFitness
                        self.writeLogLine(bestMinCostLimit, iteration)
                        solution.cost = bestMinCostLimit
                    else:
                        count += 1
            if alpha in costs:
                costs[alpha].append(bestMinCostLimit)
            else:
                costs[alpha] = [bestMinCostLimit]
            self.numSolutionsConstructed = iteration
            self.printPerformance()
        if alphatuning:
            print("Alpha tuning: ", costs)
        return incumbent


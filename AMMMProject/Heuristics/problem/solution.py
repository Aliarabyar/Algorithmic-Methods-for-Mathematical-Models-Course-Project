'''
AMMM Project

Ali Arabyarmohammadi

Based on AMMM Lab Heuristics.
Copyright 2020 Luis Velasco.
'''

import copy
from Heuristics.solution import _Solution


class Solution(_Solution):
    def __init__(self, G, H):
        self.G = G
        self.H = H
        self.cost = 0
        self.matched = {}  # hash table: node in shape Id -> node in image Id
        super().__init__()

    def CalcWeightDiff(self, nodeImage, nodeShape):
        cost = 0
        for shapeAdj, imageAdj in self.matched.items():
            if imageAdj not in list(nodeImage.adjacent.keys()) or shapeAdj not in list(nodeShape.adjacent.keys()):
                local_cost = 0
            else:
                local_cost = abs(nodeImage.getWeight(imageAdj) - nodeShape.getWeight(shapeAdj))

            cost = cost + local_cost

        return cost

    def SolutiongetFitness(self):
        cost = 0

        for neighbor_shape, neighbor_image in self.matched.items():
            for nodeShapeIndex, nodeImageIndex in self.matched.items():
                nodeImage = self.G.nodes[nodeImageIndex]
                nodeShape = self.H.nodes[nodeShapeIndex]
                if neighbor_image not in list(nodeImage.adjacent.keys()) or neighbor_shape not in list(
                        nodeShape.adjacent.keys()):
                    local_cost = 0
                else:
                    weight1 = nodeShape.getWeight(neighbor_shape)
                    weight2 = nodeImage.getWeight(neighbor_image)
                    local_cost = abs(weight2 - weight1)
                cost = cost + local_cost

        return cost / 2

    def chechFeasByIsomorphismCond(self, ShapeNode, ImageNode):
        if ImageNode.id in list(self.matched.values()) or len(ImageNode.adjacent) < len(ShapeNode.adjacent):
            return False
        matchesInshape = set(list(self.matched.keys())).intersection(list(ShapeNode.adjacent.keys()))
        matchesInimage = set(list(self.matched.values())).intersection(list(ImageNode.adjacent.keys()))
        if set([self.matched[x] for x in matchesInshape]) != matchesInimage:
            return False
        return True

    def assign(self, nodeImage, nodeShape):
        self.matched[nodeShape.id] = nodeImage.id

        return True

    def unassign(self, taskId, cpuId):
        if not self.isFeasibleToUnassignTaskFromCPU(taskId, cpuId): return False

        del self.taskIdToCPUId[taskId]
        self.cpuIdToListTaskId[cpuId].remove(taskId)
        self.availCapacityPerCPUId[cpuId] += self.tasks[taskId].getTotalResources()

        self.updateHighestLoad()
        return True

    def __str__(self):
        strSolution = 'OBJECTIVE = %5.f;\n' % self.cost
        if self.cost == float('inf'): return strSolution

        for key, val in self.matched.items():
            strSolution += 'f( ' + str(key) + ' )' + ' = ' + str(val) + '\n'

        return strSolution

    def saveToFile(self, filePath):
        f = open(filePath, 'w')
        f.write(self.__str__())
        f.close()

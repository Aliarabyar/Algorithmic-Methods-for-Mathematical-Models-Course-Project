'''
AMMM Project

Ali Arabyarmohammadi

Based on AMMM P2 Instance Generator v2.0.
Copyright 2020 Luis Velasco.
'''
import math
import numpy as np
import os, random


class InstanceGenerator(object):
    # Generate instances based on read configuration.

    def __init__(self, config):
        self.config = config

    def generate(self):
        instancesDirectory = self.config.instancesDirectory
        fileNamePrefix = self.config.fileNamePrefix
        fileNameExtension = self.config.fileNameExtension
        numInstances = self.config.numInstances


        # number of nodes in Image graph
        n = self.config.n
        # number of nodes in Shape graph
        m = self.config.m

        # number of edges in Image graph
        # In order to have all the vertices connected to at least one edge,
        # number of edges should be at least n-1 (and less than N x N as the maximum value)
        e = self.config.e

        # number of edges in Shape graph
        # In order to have all the vertices connected to at least one edge,
        # number of edges should be at least m-1 (and also less than W x W as the maximum value)
        f = self.config.f


        if not os.path.isdir(instancesDirectory):
            raise AMMMException('Directory(%s) does not exist' % instancesDirectory)




        for i in range(numInstances):
            instancePath = os.path.join(instancesDirectory, '%s_%d.%s' % (fileNamePrefix, i, fileNameExtension))
            fInstance = open(instancePath, 'w')

            # Generating graphs
            GraphG, densityG = self.defineMatrix(n, e)
            GraphH, densityH = self.defineMatrix(m, f)

            load = m / n
            print("load:", load)
            print("Image graph density: ", densityG)
            print("Shape graph density: ", densityH)


            fInstance.write('n = %d;\n' % n)
            fInstance.write('m = %d;\n' % m)


            fInstance.write('\nG =\n  [\n')
            for p_i in GraphG:
                fInstance.write('    [ %s ]\n' % (' '.join(map(str, p_i))))
            fInstance.write('  ];\n\nH =\n  [\n')
            for s_i in GraphH:
                fInstance.write('    [ %s ]\n' % (' '.join(map(str, s_i))))
            fInstance.write('  ];')

            fInstance.close()

    def defineMatrix(self, node, edge ):
        Matrix = np.zeros((node, node), dtype=float)
        NumNonZero = 0
        while NumNonZero <= edge - 1:
            s = random.sample(range(0, node), 2)
            randunif = round(random.uniform(0, 1), 2)
            Matrix[s[0]][s[1]] = randunif
            Matrix[s[1]][s[0]] = randunif
            NumNonZero = np.count_nonzero(Matrix) / 2

        density = round(edge / math.comb(node, 2), 2)


        return Matrix ,density




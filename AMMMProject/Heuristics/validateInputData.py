'''
AMMM Project

Ali Arabyarmohammadi

Based on AMMM Lab Heuristics.
Copyright 2020 Luis Velasco.
'''

from AMMMGlobals import AMMMException
import numpy as np
import copy

# Validate instance attributes read from a DAT file.
# It validates the structure of the parameters read from the DAT file.
# It does not validate that the instance is feasible or not.
# Use Problem.checkInstance() function to validate the feasibility of the instance.
class ValidateInputData(object):
    @staticmethod
    def validate(data):
        # Validate that all input parameters were found
        for paramName in ['n', 'm', 'G', 'H']:
            if paramName not in data.__dict__:
                raise AMMMException('Parameter/Set(%s) not contained in Input Data' % str(paramName))

        # Validate n
        n = data.n
        if not isinstance(n, int) or (n <= 0):
            raise AMMMException('n(%s) has to be a positive integer value.' % str(n))

        # Validate m
        m = data.m
        if not isinstance(m, int) or (m <= 0):
            raise AMMMException('m(%s) has to be a positive integer value.' % str(m))

        # Validate G
        G = copy.deepcopy(list(data.G))
        if len(G) != n:
            raise AMMMException('Size of G(%d) does not match with value of n(%d).' % (len(G), n))

        for value in G:
            for item in np.array(list(value)):
                if not isinstance(item, (int, float)) or (item < 0) or (item > 1):
                    raise AMMMException('Invalid parameter value(%s) in G. Should be a float greater or equal than zero and lower equal to 1.' % str(item))

        # Validate H
        H = copy.deepcopy(list(data.H))
        if len(H) != m:
            raise AMMMException('Size of H(%d) does not match with value of m(%d).' % (len(H), m))

        for value in H:
            temp = np.array(list(value))
            for item in np.array(list(value)):
                if not isinstance(item, (int, float)) or (item < 0) or (item > 1):
                    raise AMMMException('Invalid parameter value(%s) in H. Should be a float greater or equal than zero and lower equal to 1.' % str(item))


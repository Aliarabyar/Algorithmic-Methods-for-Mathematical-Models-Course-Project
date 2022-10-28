'''
AMMM Project

Ali Arabyarmohammadi

Based on AMMM Lab Heuristics Main Function.
Copyright 2020 Luis Velasco.
'''

from argparse import ArgumentParser
from pathlib import Path

import sys
import math
from Heuristics.datParser import DATParser
from AMMMGlobals import AMMMException
from Heuristics.validateInputData import ValidateInputData
from Heuristics.ValidateConfig import ValidateConfig
from Heuristics.solvers.solver_Greedy import Solver_Greedy
from Heuristics.solvers.solver_GRASP import Solver_GRASP
from Heuristics.problem.instance import Instance


class Main:
    def __init__(self, config):
        self.config = config

    def run(self, data):
        try:
            if self.config.verbose: print('Creating Problem Instance...')
            instance = Instance(self.config, data)
            if self.config.verbose: print('Solving the Problem...')
            if instance.checkInstance():
                initialSolution = None
                if self.config.solver == 'Greedy' or self.config.solver == 'Random':
                    solver = Solver_Greedy(self.config, instance)
                elif self.config.solver == 'GRASP':
                    solver = Solver_GRASP(self.config, instance)
                else:
                    raise AMMMException('Solver %s not supported.' % str(self.config.solver))
                solution = solver.solve(solution=initialSolution)

                if not math.isinf(solution.cost):
                    for s in solution.matched:
                        print('f(', str(s), ') = ', str(solution.matched[s]))
                    print('OBJECTIVE: %s' % str(round(solution.cost, 2)))
                else:
                    print('Solution Not Found.')
                solution.saveToFile(self.config.solutionFile)
            else:
                print('Instance is infeasible.')
                solution = instance.createSolution()
                solution.makeInfeasible()
                solution.saveToFile(self.config.solutionFile)
            return 0
        except AMMMException as e:
            print('Exception:', e)
            return 1


if __name__ == '__main__':
    parser = ArgumentParser(description='AMMM Project Heuristics')
    parser.add_argument('-c', '--configFile', nargs='?', type=Path,
                        default=Path(__file__).parent / 'config/config.dat', help='specifies the config file')
    args = parser.parse_args()

    config = DATParser.parse(args.configFile)
    ValidateConfig.validate(config)
    inputData = DATParser.parse(config.inputDataFile)
    ValidateInputData.validate(inputData)

    if config.verbose:
        print('AMMM Project Heuristics')
        print('-------------------')
        print('Config file %s' % args.configFile)
        print('Input Data file %s' % config.inputDataFile)

    main = Main(config)
    sys.exit(main.run(inputData))

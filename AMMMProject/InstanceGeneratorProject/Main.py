'''
AMMM Project

Ali Arabyarmohammadi

Based on AMMM P2 Instance Generator v2.0 - Main function.
Copyright 2020 Luis Velasco.
'''

import sys
from Heuristics.datParser import DATParser
from InstanceGeneratorProject.ValidateConfig import ValidateConfig
from InstanceGeneratorProject.InstanceGenerator import InstanceGenerator
from AMMMGlobals import AMMMException

def run():
    try:
        configFile = "config\config.dat"
        print("AMMM Project Instance Generator")
        print("-----------------------")
        print("Reading Config file %s..." % configFile)
        config = DATParser.parse(configFile)
        ValidateConfig.validate(config)
        print("Creating Instances...")
        instGen = InstanceGenerator(config)
        instGen.generate()

        print("Done")
        return 0
    except AMMMException as e:
        print("Exception: %s", e)
        return 1

if __name__ == '__main__':
    sys.exit(run())

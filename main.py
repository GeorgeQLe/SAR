# Copyright 2019 George Le

# built-in modules and packages 
from sys import argv

# modules
from areatype import AreaType
from simulation import Simulation

def main():
    requestedAreaType = AreaType.default
    # if there were command line arguments
    if len(argv) > 1:
        if isinstance(argv[1], AreaType):
            pass

    simulation = Simulation()
    simulation.setup_simulation(x=89, y=89, areatype=requestedAreaType, num_search_targets=1)
    simulation.run_simulation(30)
    
if __name__ == "__main__":
    main()
# Copyright 2019 George Le

from sys import argv

from areatype import AreaType
from simulation import Simulation

def main():
    x = 5
    y = 5
    
    if len(argv) > 1:
        if len(argv) == 3:
            x = int(argv[1])
            y = int(argv[2])

    simulation = Simulation()
    simulation.setup_simulation(x=x, y=y, areatype=AreaType.woodlands, num_search_targets=1)
    simulation.run_simulation(30)
    
if __name__ == "__main__":
    main()
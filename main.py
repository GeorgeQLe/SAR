# Copyright 2019 George Le

from areatype import AreaType
from simulation import Simulation

def main():
    simulation = Simulation()
    simulation.setup_simulation(x=30, y=30, areatype=AreaType.woodlands, num_search_targets=1)
    simulation.run_simulation(30)
    
if __name__ == "__main__":
    main()
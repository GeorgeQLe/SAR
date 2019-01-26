# Copyright 2019 George Le

from simulation import Simulation

import unittest

class SimulationUnitTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._simulation = Simulation()

    def generate_sim(self):
        

def main():
    simulation = Simulation()
    simulation.generate_simulation(30, 30, 3, 1)
    simulation.run_simulation(30)
    
if __name__ == "__main__":
    unittest.main()
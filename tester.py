from simulation import Simulation

class Tester():

    def __init__(self):
        self.simulation = Simulation()
        
    def test_individual(self, individual):
        self.simulation.setup_simulation(10, 10, 1, 1, individual)
        return self.simulation.run_simulation(30)

    def test_group(self, population):
        counter         = 1 # a counter value storing the number of runs of the simulation
        return_scores   = list() # the return values of the function 
        
        # for each individual of the population, perform a run of the simulation
        for individual in population:
            self.simulation.setup_simulation(10, 10, 1, 1, individual)
            return_scores.append(self.simulation.run_simulation(30))
            counter += 1
        return return_scores
from areatype import AreaType
from simulation import Simulation

def test_individual(individual):
    simulation  = Simulation()
    simulation.setup_simulation(10, 10, AreaType.woodlands, 1, 1, individual)
    return simulation.run_simulation(30)

def test_group(population):
    counter         = 1 # a counter value storing the number of runs of the simulation
    return_scores   = list() # the return values of the function 
    
    # for each individual of the population, perform a run of the simulation
    for individual in population:
        simulation  = Simulation() # create an instance of the Simulation class
        simulation.setup_simulation(10, 10, AreaType.woodlands, 1, 1, individual)
        return_scores.append(simulation.run_simulation(30))
        print("Simulation number:", counter, "complete")
        counter += 1
    return return_scores
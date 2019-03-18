# Copyright 2019 George Le

from sys import argv

# from areatype import AreaType
from simulation import Simulation
# from geneticalgorithm import GeneticAlgorithm

from random import uniform

def main():
    pass
    # x = 30
    # y = 30
    
    # if len(argv) > 1:
    #     if len(argv) == 3:
    #         x = int(argv[1])
    #         y = int(argv[2])

    # simulation = Simulation()
    # simulation.setup_simulation(x=x, y=y, areatype=AreaType.woodlands, num_search_targets=1)
    # simulation.run_simulation(30)
    
    # print("Start Creating Neural Network")
    # nn = NeuralNetwork()
    # nn.create_layer(index= 0, size= 9, size_of_next_layer= 4)
    # nn.create_layer(index= 1, size= 4, size_of_next_layer= 9)
    # nn.create_layer(index= 2, size= 9)
    
    # inputs = [ 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9 ]

    # print("Neural Network outputs:", nn.evaluate(inputs=NeuralNetworkInputs(inputs)))

    # print("Neuron weights at neuron #", 13, ":", nn.search_neuron_weights_by_ID(13))

if __name__ == "__main__":
    main()
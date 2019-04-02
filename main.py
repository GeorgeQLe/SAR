# Copyright 2019 George Le

from sys import argv

from areatype import AreaType
from neuralnetwork import NeuralNetwork, NeuralNetworkInputs
from geneticalgorithm import GeneticAlgorithm, Simulation
from searchagent import SearchAgent

from collections import OrderedDict
from random import randint, uniform

def main():
    x = 30
    y = 30

    # if len(argv) > 1:
    #     if len(argv) == 3:
    #         x = int(argv[1])
    #         y = int(argv[2])

    # simulation = Simulation()
    # simulation.setup_simulation(x=x, y=y, areatype=AreaType.woodlands, num_search_targets=1)
    # simulation.run_simulation(30)

    

    ga = GeneticAlgorithm()
    ga.run(1, 5, 80, OrderedDict((
        (0, 11), (1, 15), (2, 24)
    )))

    # print("Start Creating Neural Network")
    # nn = NeuralNetwork()
    # nn.create_layer(index= 0, size= 9, size_of_next_layer= 4)
    # nn.create_layer(index= 1, size= 4, size_of_next_layer= 9)
    # nn.create_layer(index= 2, size= 9, last_layer= True)
    
    # inputs = [ 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9 ]

    # print("Neural Network outputs:", nn.evaluate(inputs=NeuralNetworkInputs(inputs)))

    # print("Neuron weights at neuron #", 13, ":", nn.search_neuron_weights_by_ID(13))

    # nn_weights = nn.get_weights()
    # print("All neuron weights: ")
    # print(nn_weights.weights)
    # for IDs in nn_weights.weights.keys():
    #     print("Neuron", IDs, ":", nn_weights.weights[IDs])
    # print("Layer size", nn_weights.layer_size)

    # new_nn = NeuralNetwork()
    # new_nn.create_layer(index= 0, size= 9, size_of_next_layer= 4)
    # new_nn.create_layer(index= 1, size= 4, size_of_next_layer= 9)
    # new_nn.create_layer(index= 2, size= 9, last_layer= True)

    # new_nn.override_weights(nn_weights)

    # new_weights = new_nn.get_weights()
    # print("New neuron weights: ")
    # print(new_weights.weights)
    # for IDs in new_weights.weights.keys():
    #     print("Neuron", IDs, ":", new_weights.weights[IDs])
    
if __name__ == "__main__":
    main()
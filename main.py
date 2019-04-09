# Copyright 2019 George Le

from sys import argv

from areatype import AreaType
from neuralnetwork import NeuralNetwork
from geneticalgorithm import GeneticAlgorithm, Simulation
from searchagent import SearchAgent

from collections import OrderedDict
from math import exp
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
    ga.run(layers_info= dict({
            0 : (9, 5),
            1 : (5, 1)
            }), 
            num_generations= 1, 
            number_of_individuals= 5, 
            number_of_individual_genes= 50)
    
#     value = -2
#     add_value = 0.1
#     while value < 2.3:
#         print("Input:", value, "Output:", round(sigmoid(value), 4))
#         value+=add_value

# def sigmoid(input):
#     return 1.0 / (1.0 + exp(input * -1))

    weights = list()
    for i in range(40):
        weights.append(round(uniform(-2, 2.3), 4))
    nn = NeuralNetwork(bias=0, num_layers=3, layers_info=dict({
                                                            0 : (9, 4),
                                                            1 : (4, 1)
                                                            }), num_weights= 40, weights=weights)
    input = list()
    for j in range(9):
        input.append(round(uniform(-2, 2.3), 2))
    nn.evaluate(inputN1= input)
    
if __name__ == "__main__":
    main()
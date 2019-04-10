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
    

    ga = GeneticAlgorithm()
    ga.run(layers_info= dict({
            0 : (9, 5),
            1 : (5, 1)
            }), 
            num_generations= 1, 
            number_of_individuals= 5, 
            number_of_individual_genes= 50)

if __name__ == "__main__":
    main()
# Copyright 2019 George Le

from neuralnetwork import NeuralNetworkWeights

class GeneticAlgorithm:

    def __init__(self):
        self.__current_generation_num   = 0
        self.__number_of_individuals    = 0 # number of individuals in each generations
        self.__number_of_generations    = 0 # number of generations that the genetic algorithm will run through
        self.__old_populations          = { int : list() } # this is a dict holding a key-value pair (population index (int) : list(Neuron Weights)) 
        self.__population               = list()

    def run(self, num_generations, num_individuals):
        self.__number_of_generations = num_generations
        self.__number_of_individuals = num_individuals
        self.__generate_new_population()

    def __generate_new_population(self):
        self.__current_generation_num += 1
        for i in range(self.__number_of_individuals):
            individual = NeuralNetworkWeights()

    def __test_population(self):
        pass
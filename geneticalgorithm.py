# Copyright 2019 George Le

from neuralnetwork import NeuronWeights
from simulation import Simulation

from collections import OrderedDict
from random import uniform

class GeneticAlgorithm:

    def __init__(self):
        self.__current_generation_num       = 0
        self.__number_of_generations        = 0 # number of generations that the genetic algorithm will run through
        self.__number_of_individual_genes   = 0 # number of genes that belong to an individual
        self.__number_of_individuals        = 0 # number of individuals in each generations
        self.__old_populations              = { int : list() } # this is a dict holding a key-value pair (population index (int) : list(Neural Network Weights)) 
        self.__population                   = list()

    def __crossover(self, parent1, parent2):
        pass

    def __generate_new_population(self):
        self.__current_generation_num       += 1

        layers_size = {
            0 : 9,
            1 : 13,
            2 : 22
        }
        # the total number of neurons in the neural network
        self.__number_of_individual_genes = layers_size[2]
    
        nn_weights = OrderedDict()
        weights = list()
        # creates the n number of neural networks that comprise the GA population
        for i in range(self.__number_of_individuals):
            # creates the 22 neurons of the neural network
            for j in range(self.__number_of_individual_genes):
                # creates the 72 weights of the neuron
                for k in range(72):
                    weights.append(round(uniform(0.0, 1.0), 2))
                neuron_weights = NeuronWeights(weights)
            self.__population.append(neuron_weights)
        print("Population")
        counter = 0
        print(self.__population[0].weights)
        # for weights in self.__population:
        #     print("Weights #", counter, ":", weights.weights)

    def __test_population(self):
        simulation = Simulation()

    def run(self, num_generations, number_of_individuals):
        self.__number_of_generations = num_generations
        self.__number_of_individuals = number_of_individuals

        while self.__current_generation_num < self.__number_of_generations:
            self.__current_generation_num       += 1
            if self.__current_generation_num == 1:
                # create a brand new population
                self.__generate_new_population()
            self.__test_population()
# Copyright 2019 George Le

from neuralnetwork import NeuronWeights
from simulation import AreaType, SearchAgent, Simulation

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

    def __generate_new_population(self, layers_size):
        # creates the n number of neural networks that comprise the GA population
        for i in range(self.__number_of_individuals):
            weights = list()
            # creates the 72 weights of a neural network
            for j in range(self.__number_of_individual_genes):
                weights.append(round(uniform(0.0, 1.0), 2))
            neuron_weights = NeuronWeights(weights)
            self.__population.append({ 0 : neuron_weights.create_from_neural_network_weights(layers_size) })
        print("Length of population:", len(self.__population))
        print("Population:", self.__population)

    def __replacement(self):
        pass

    def __selection(self):
        pass

    def __test_population(self):
        simulation = Simulation()
        # for each individual of the population, perform a run of the simulation
        for individual in self.__population:
            # separates the neural network weights
            for neuralnetworkweights in individual.keys():
                print("Neural network weights:", individual[neuralnetworkweights])
                temp_individual = list()
                temp_individual.append(individual[neuralnetworkweights])
                simulation.setup_simulation(30, 30, AreaType.woodlands, 1, 1, temp_individual)
                simulation.run_simulation(20)

    def run(self, num_generations, number_of_individuals, number_of_individual_genes, layers_size):
        self.__number_of_generations        = num_generations
        self.__number_of_individuals        = number_of_individuals
        self.__number_of_individual_genes   = number_of_individual_genes

        while self.__current_generation_num < self.__number_of_generations:
            self.__current_generation_num       += 1
            if self.__current_generation_num == 1:
                # create a brand new population
                print("Generate new population")
                self.__generate_new_population(layers_size)
            print("Test population")
            self.__test_population()
            self.__selection()
            self.__replacement()
        print("GA run complete")
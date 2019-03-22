# Copyright 2019 George Le

from neuralnetwork import NeuronWeights
from simulation import AreaType, SearchAgent, Simulation

from collections import OrderedDict
from random import randint, uniform

class GeneticAlgorithm:

    def __init__(self):
        self.__current_generation_num       = 0
        self.__number_of_generations        = 0 # number of generations that the genetic algorithm will run through
        self.__number_of_individual_genes   = 0 # number of genes that belong to an individual
        self.__number_of_individuals        = 0 # number of individuals in each generations
        self.__old_populations              = { int : list() } # this is a dict holding a key-value pair (population index (int) : list(Neural Network Weights)) 
        self.__population                   = list()        # this is a list holding the GA's current population
        self.__scores                       = OrderedDict() # this is a dict holding a key-value pair ()

    def __crossover(self, parent1, parent2):
        print(len(parent1), len(parent2))
        # single point crossover
        for i in range(len(parent1)):
            pass

    def __generate_new_population(self, layers_size):
        # creates the n number of neural networks that comprise the GA population
        for i in range(self.__number_of_individuals):
            weights = list()
            # creates the 80 weights of a neural network
            for j in range(self.__number_of_individual_genes):
                weights.append(round(uniform(0.0, 1.0), 2))
            neuron_weights = NeuronWeights(weights)
            self.__population.append(neuron_weights.create_from_neural_network_weights(layers_size))
            
            for nn_weight in self.__population:
                print(nn_weight.weights)

    def __replacement(self):
        for ID in self.__scores.keys():
            pass

    def __selection(self):
        return_parents = list()
        # to select two parents
        for n in range(2):
            # from four possible randomly selected individuals of the population
            for i in range(4):
                tournament_pool = dict()
                random_roll = randint(0, self.__number_of_individuals - 1)
                
                

    def __test_population(self):
        simulation = Simulation()
        counter = 1
        return_pop_info = OrderedDict()
        # for each individual of the population, perform a run of the simulation
        for individual in self.__population:
            # separates the neural network weights
            for neuralnetworkweights in individual.keys():
                print("Simulation number:", counter)
                counter += 1
                temp_individuals = list()
                temp_individuals.append(individual[neuralnetworkweights])
                print("NN weights:", neuralnetworkweights)
                print("Individual:", individual[neuralnetworkweights])
                simulation.setup_simulation(10, 10, AreaType.woodlands, 1, 1, temp_individuals)
                return_pop_info[counter] = simulation.run_simulation(30)
            return return_pop_info

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
            #print("Test population")
            #self.__scores = self.__test_population()
            #self.__selection()
            #self.__replacement()
        print("GA run complete")
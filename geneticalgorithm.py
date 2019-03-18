# Copyright 2019 George Le

from neuralnetwork import NeuronWeights

from random import uniform

class GeneticAlgorithm:

    def __init__(self):
        self.__current_generation_num       = 0
        self.__number_of_generations        = 0 # number of generations that the genetic algorithm will run through
        self.__number_of_individual_genes   = 0 # number of genes for each individual
        self.__number_of_individuals        = 0 # number of individuals in each generations
        self.__old_populations              = { int : list() } # this is a dict holding a key-value pair (population index (int) : list(Neuron Weights)) 
        self.__population                   = list()

    def run(self, num_generations, num_individuals, num_individual_genes):
        self.__number_of_generations        = num_generations
        self.__number_of_individual_genes   = num_individual_genes 
        self.__number_of_individuals        = num_individuals
        self.__generate_new_population()

    def __generate_new_population(self):
        self.__current_generation_num += 1
        for i in range(self.__number_of_individuals):
            individual_genes = list()
            for j in range(self.__number_of_individual_genes):
                individual_genes.append(round(uniform(0.0, 1.0), 2))
            self.__population.append(NeuronWeights(individual_genes))

    def __test_population(self):
        pass
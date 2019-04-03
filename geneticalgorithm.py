# Copyright 2019 George Le

from neuralnetwork import NeuralNetwork
from simulation import AreaType, SearchAgent, Simulation

from collections import OrderedDict
from random import randint, uniform

from operator import itemgetter

class GeneticAlgorithm:

    def __init__(self):
        self.__current_generation_num       = 0
        self.__mutation_rate                = 5 # the rate in which random mutations happen in the GA, default is 5%
        self.__number_of_generations        = 0 # number of generations that the genetic algorithm will run through
        self.__number_of_individual_genes   = 0 # number of genes that belong to an individual
        self.__number_of_individuals        = 0 # number of individuals in each generations
        self.__old_populations              = { int : list() } # this is a dict holding a key-value pair (population index (int) : list(Neural Network Weights)) 
        self.__population                   = list() # this is a list holding the GA's current population
        self.__scores                       = list() # this is a dict holding a list of dicts key-value pair (ID : score)

    def __crossover(self, parent1 = list(), parent2 = list()):
        # single point crossover
        self.__singlepoint_crossover(parent1, parent2)

        # two point crossover
        self.__twopoint_crossover(parent1, parent2)

        # tournament pool
        
        # replace the winners of the tournament poll if they are better than the existing population
        self.__replacement(parent1, parent2)

    def __generate_new_population(self, layers_info):
        # creates the n number of neural networks that comprise the GA population
        for i in range(self.__number_of_individuals):
            individual = list()
            # create neural network representation
            for j in range(self.__number_of_individual_genes):
                individual.append(round(uniform(0.0, 1.0), 2))
            self.__population.append(individual)

    def __replacement(self, parent1, parent2):
        worst_score = 0
        second_worst = 0
        worst_index = len(self.__population) - 1
        second_index = len(self.__population) - 1
        index = 1
        for score in self.__scores:
            prev_second_worst = second_worst
            prev_second_worst_index = second_index
            if score[index] < second_worst:
                second_worst = score[index]
                second_index = index
            if score[index] < worst_score:
                worst_score = score[index]
                worst_index = index

                second_worst = prev_second_worst
                second_index = prev_second_worst_index
            index += 1
        self.__population[second_index - 1] = parent2
        self.__population[worst_index - 1] = parent1
        
    def __selection(self):
        return_parents = list()
        exclusion_list = list()
        # to select two parents
        while len(return_parents) != 2:
            random_roll = randint(0, len(self.__population) - 1)
            if random_roll not in exclusion_list:
                return_parents.append(self.__population[random_roll])
                exclusion_list.append(random_roll)
        self.__crossover(return_parents[0], return_parents[1])

    def __singlepoint_crossover(self, parent1 = list(), parent2 = list()):
        random_rolls = list()
        for i in range(len(parent1)):
            nn_weights1 = parent1
            nn_weights2 = parent2
            random_roll = randint(0, len(parent1) - 1)
            nn_weights1[random_roll], nn_weights2[random_roll] = nn_weights2[random_roll], nn_weights1[random_roll]
            random_rolls.append(random_roll)
        return random_rolls

    def __tournament_pool(self):
        # determine if there will be a mutation at all
        random_roll = randint(1, 100)
        # mutation rate
        if random_roll > self.__mutation_rate:
            pass

    def __twopoint_crossover(self, parent1 = list(), parent2 = list()):
        random_roll1 = randint(0, len(parent1) - 1)
        random_roll2 = randint(random_roll1, len(parent2) - 1)
        index = random_roll1
        nn_weights1 = parent1
        nn_weights2 = parent2
        while index < random_roll2:
            nn_weights1[index], nn_weights2[index] = nn_weights2[index], nn_weights1[index]
            index += 1
        parent1 = nn_weights1
        parent2 = nn_weights2
        return tuple(random_roll1, random_roll2)

    def __test_population(self):
        counter = 1
        return_pop_info = list()
        
        # for each individual of the population, perform a run of the simulation
        for individual in self.__population:
            simulation = Simulation()
            simulation.setup_simulation(10, 10, AreaType.woodlands, 1, 1, individual)
            return_pop_info.append(simulation.run_simulation(30, counter))
            print("Simulation number:", counter, "complete")
            counter += 1
        return return_pop_info

    def run(self, layers_info, num_generations, number_of_individuals, number_of_individual_genes):
        self.__number_of_generations        = num_generations
        self.__number_of_individuals        = number_of_individuals
        self.__number_of_individual_genes   = number_of_individual_genes

        while self.__current_generation_num < self.__number_of_generations:
            self.__current_generation_num       += 1
            if self.__current_generation_num == 1:
                # create a brand new population
                self.__generate_new_population(layers_info)
            self.__scores = self.__test_population()
            for weights in self.__population:
                print(weights)
            for i in range(10):
                self.__selection()
        print("GA run complete")
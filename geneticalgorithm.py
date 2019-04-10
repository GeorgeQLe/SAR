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
        self.__scores                       = list() # this is a list of scores of the population, the index of the score should correspond to the index
                                                     # of the scored individual in the population list

    def __generate_new_population(self, layers_info):
        # creates the n number of neural networks that comprise the GA population
        for i in range(self.__number_of_individuals):
            individual = list()
            # create neural network representation
            for j in range(self.__number_of_individual_genes):
                individual.append(round(uniform(-2.0, 2.3), 4))
            self.__population.append(individual)
            
    def __selection(self):
        parents = list()
        # to select two parents

        # TODO ADD PROBABILITIES WITH MUTATION RATE FOR ALL GA OPERATIONS
        print("Selection")
        parents = self.__tournament_pool()
        print(parents)
        print("Before crossover")
        print("Parent1:", parents[0])
        print("Parent2:", parents[1])
        self.__crossover(parents[0], parents[1])
        print("After crossover")
        print("Parent1:", parents[0])
        print("Parent2:", parents[1])

        self.__mutation(parents[0])
        self.__mutation(parents[1])
        print("After mutation")
        print("Parent1:", parents[0])
        print("Parent2:", parents[1])
        # replace the winners of the tournament pool if they are better than the existing population
        self.__replacement(parents[0], parents[1])

    def __tournament_pool(self):
        # determine if there will be a mutation at all
        random_roll     = randint(1, 100)
        # stores the best from the first selection from the population
        stored_best     = list()

        # selected parents for the replacement
        parents  = list()

        # selecting individuals from the population
        tp_indexes        = list()
        while len(tp_indexes) != 4:
            random_roll = randint(0, len(self.__population) - 1)
            if random_roll not in tp_indexes:
                tp_indexes.append(random_roll)
        while len(parents) != 2:
            best_score          = self.__scores[0]
            best_score_index    = 0
            for index in tp_indexes:
                if self.__scores[index] > best_score and self.__scores[index] not in stored_best:
                    best_score          = self.__scores[index]
                    best_score_index    = index
            # add the selected two best parents
            parents.append(self.__population[best_score_index])
            stored_best.append(best_score)
        return parents

    def __crossover(self, parent1 = list(), parent2 = list()):
        print("Before single point crossover")
        print("Parent1:", parent1)
        print("Parent2:", parent2)
        # single point crossover
        self.__singlepoint_crossover(parent1, parent2)
        print("Before two point crossover")
        print("Parent1:", parent1)
        print("Parent2:", parent2)
        # two point crossover
        self.__twopoint_crossover(parent1, parent2)
        print("After crossover")
        print("Parent1:", parent1)
        print("Parent2:", parent2)

    def __singlepoint_crossover(self, parent1 = list(), parent2 = list()):
        random_roll = randint(0, len(parent1) - 1)
        nn_weights1 = parent1
        nn_weights2 = parent2
        print("Random roll:", random_roll)
        while random_roll < len(parent1):    
            nn_weights1[random_roll], nn_weights2[random_roll] = nn_weights2[random_roll], nn_weights1[random_roll]
            random_roll+=1
        parent1 = nn_weights1
        parent2 = nn_weights2

    def __twopoint_crossover(self, parent1 = list(), parent2 = list()):
        random_roll1 = randint(0, len(parent1) - 1)
        random_roll2 = randint(random_roll1, len(parent2) - 1)
        index       = random_roll1
        nn_weights1 = parent1
        nn_weights2 = parent2
        print("Random roll1:", random_roll1)
        print("Random roll2:", random_roll2)
        while index < random_roll2:
            nn_weights1[index], nn_weights2[index] = nn_weights2[index], nn_weights1[index]
            index += 1
        parent1 = nn_weights1
        parent2 = nn_weights2
        return tuple((random_roll1, random_roll2))

    def __mutation(self, individual):
        random_roll                 = randint(0, len(individual) - 1)
        print("Random roll:", random_roll)
        individual[random_roll] = round(uniform(-2, 2.3), 4)

    def __replacement(self, parent1, parent2):
        simulation  = Simulation()
        simulation.setup_simulation(10, 10, AreaType.woodlands, 1, 1, parent1)
        score1      = simulation.run_simulation(30)
        simulation.setup_simulation(10, 10, AreaType.woodlands, 1, 1, parent2)
        score2      = simulation.run_simulation(30)

        # designate parent 1 as the worst if parent1 is not worst than parent2
        # then swap the two parents
        if score1 > score2:
            temp_parent = parent1
            parent1 = parent2
            parent2 = temp_parent 

        # determine the two worst scores of the existing population
        worst_score     = 0
        second_worst    = 0
        worst_index     = len(self.__population) - 1
        second_index    = len(self.__population) - 1

        # get min of scores array
        # get index of element that is min
        # swap min if score of parent is greater than min
        # repeat for second parentS


        for index in range(len(self.__scores)):
            prev_second_worst = second_worst
            prev_second_worst_index = second_index
            if self.__scores[index] < second_worst:
                second_worst = self.__scores[index]
                second_index = index
            if self.__scores[index] < worst_score:
                worst_score = self.__scores[index]
                worst_index = index

                second_worst = prev_second_worst
                second_index = prev_second_worst_index
            index += 1
        # if the two new parents' scores are higher than the two worst of
        # the current population then replace them
        if score2 > second_worst and score1 > worst_score:
            print("Improvement!!!!!!!!!")
            self.__population[second_index - 1] = parent2
            self.__scores[second_index - 1] = score2
            self.__population[worst_index - 1] = parent1
            self.__scores[second_index - 1] = score1

    def __test_population(self):
        counter = 1
        return_scores = list()
        
        # for each individual of the population, perform a run of the simulation
        for individual in self.__population:
            simulation = Simulation()
            simulation.setup_simulation(10, 10, AreaType.woodlands, 1, 1, individual)
            return_scores.append(simulation.run_simulation(30))
            print("Simulation number:", counter, "complete")
            counter += 1
        return return_scores

    def run(self, layers_info, num_generations, number_of_individuals, number_of_individual_genes):
        self.__number_of_generations        = num_generations
        self.__number_of_individuals        = number_of_individuals
        self.__number_of_individual_genes   = number_of_individual_genes

        while self.__current_generation_num < self.__number_of_generations:
            self.__current_generation_num       += 1
            if self.__current_generation_num == 1:
                # create a brand new population
                self.__generate_new_population(layers_info)
                for i in range(len(self.__population)):
                    print(self.__population[i])
            self.__scores = self.__test_population()
            for i in range(len(self.__population)):
                print(self.__population[i])
                print(self.__scores[i])

            self.__selection()

        #     # record the most recent population into the history of the genetic algorithm
        #     self.__old_populations[self.__current_generation_num] = self.__population
        # for i in range(len(self.__population)):
        #     print(self.__population[i])
        #     print(self.__scores[i])
        print("GA run complete")
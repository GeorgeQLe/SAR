# Copyright 2019 George Le

from file import write_to_file
from neuralnetwork import NeuralNetwork
from tester import Tester

from collections import OrderedDict
from random import randint, uniform
from statistics import median

class GeneticAlgorithm:

    def __init__(self, debug = True, path_filename = "./Dumps/GA.txt"):
        # genetic algorithm settings
        self.__debug                        = debug # 
        self.__path_filename                = "./Dumps/GA.txt" # by default the output of the GA is put in the Dumps directory in GA.txt

        self.__number_of_generations        = 0 # number of generations that the genetic algorithm will run through
        self.__number_of_individual_genes   = 0 # number of genes that belong to an individual
        self.__number_of_individuals        = 0 # number of individuals in each generations

        # information for when the genetic algorithm runs 
        self.__current_generation_num       = 0 # a counter which tracks the current generation that the GA is running
        self.__old_populations              = dict() # this is a dict holding a key-value pair (population index (int) : list(Neural Network Weights)) 
        self.__population                   = list() # this is a list holding the GA's current population
        self.__scores                       = list() # this is a list of scores of the population, the index of the score should correspond to the index
                                                     # of the scored individual in the population list

        # mutation settings
        self.__mutation_rate_single_point   = 50 # the rate in which single point crossover happens in the GA, default is 50%
        self.__mutation_rate_two_point      = 75 # the rate in which two point crossover happens in the GA, default is 75%
        self.__mutation_rate                = 5 # the rate in which a fixed point mutation occurs in the GA, default is 5%

        # test
        self.__tester                       = Tester()

    def __generate_new_population(self, layers_info):
        # creates the n number of neural networks that comprise the GA population
        for i in range(self.__number_of_individuals):
            individual = list()
            # create neural network representation
            for j in range(self.__number_of_individual_genes):
                individual.append(round(uniform(-2.0, 2.0), 4))
            self.__population.append(individual)
            
    def __selection(self):
        # initialize the container for the two parents
        parents = list()
        # uses a tournament pool to select two parents
        print("SELECTION")
        parents = self.__tournament_pool()

        print("PARENTS BEFORE CROSSOVER")
        print("Parents 1", parents[0])
        print("Parents 2", parents[1])
        self.__crossover(parents[0], parents[1])

        random_roll = randint(1, 100)
        if random_roll > self.__mutation_rate:
            self.__mutation(parents[0])
            print("After mutation")
            print("Parent1:", parents[0])
        random_roll = randint(1, 100)
        if random_roll > self.__mutation_rate:
            self.__mutation(parents[1])
            print("After mutation")
            print("Parent2:", parents[1])

        # replace the winners of the tournament pool if they are better than the existing population
        self.__replacement(parents[0], parents[1])

    def __tournament_pool(self):
        # stores the best index from the first selection from the population
        stored_best     = list()
        # selected parents for the replacement
        parents         = list()
        
        # selects 2 parents out of the four
        while len(parents) != 2:
            # selecting individuals from the population, stores the indexes of the selected individuals
            tp_indexes  = list()
            tp_scores   = list()
            while len(tp_indexes) != 4:
                random_roll = randint(0, len(self.__population) - 1)
                if random_roll not in tp_indexes and random_roll not in stored_best:
                    tp_indexes.append(random_roll)
                    tp_scores.append(self.__scores[random_roll])
            
            # from the selected individuals, get the best score
            best_score  = max(tp_scores)
            # with the best score get the index of the individual with the best score
            # if there are ties, will select the smallest index of the best score 
            best_score_index = self.__scores.index(best_score)
            if best_score_index in stored_best:
                indices = [i for i, x in enumerate(self.__scores) if x == best_score]
                for index in indices:
                    if index not in stored_best:
                        best_score_index = index
                        break
            # add the selected two best parents
            parents.append(self.__population[best_score_index])
            # set stored_best to best scored index
            stored_best.append(best_score_index)
        print("Selected parents at indexes:", stored_best)
        return parents

    def __crossover(self, parent1 = list(), parent2 = list()):
        print("Before crossover")
        print("Parent 1:", parent1)
        print("Parent 2:", parent2)
        # single point crossover
        random_roll = randint(1, 100)
        if random_roll > self.__mutation_rate_single_point:
            print("Does single point")
            self.__singlepoint_crossover(parent1, parent2)
            print("Before two point crossover")
            print("Parent 1:", parent1)
            print("Parent 2:", parent2)
        # two point crossover
        random_roll = randint(1, 100)
        if random_roll > self.__mutation_rate_two_point:
            print("Does two point")
            self.__twopoint_crossover(parent1, parent2)
            print("After crossover")
            print("Parent 1:", parent1)
            print("Parent 2:", parent2)

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
        print("Random roll 1:", random_roll1)
        print("Random roll 2:", random_roll2)
        while index < random_roll2:
            nn_weights1[index ], nn_weights2[index] = nn_weights2[index], nn_weights1[index]
            index += 1
        parent1 = nn_weights1
        parent2 = nn_weights2
        return tuple((random_roll1, random_roll2))

    def __mutation(self, individual):
        random_roll                 = randint(0, len(individual) - 1)
        print("Random roll:", random_roll)
        individual[random_roll] = round(uniform(-2, 2.3), 4)

    def __replacement(self, parent1, parent2):
        score1      = self.__tester.test_individual(parent1)
        score2      = self.__tester.test_individual(parent2)

        # designate parent 1 as the worst if parent1 is not worst than parent2
        # then swap the two parents
        if score1 > score2:
            temp_parent = parent1
            parent1 = parent2
            parent2 = temp_parent 

        # get min of scores array
        # get index of element that is min
        # swap min if score of parent is greater than min
        # repeat for second parent
        min_score = min(self.__scores)
        min_index = self.__scores.index(min_score)
        if score1 > min_score:
            print("Replace parent 1 with individual", min_index + 1)
            print("Individual to be replaced:", self.__population[min_index])
            print("Parent 1:", parent1)
            self.__population[min_index] = parent1
            print("New Individual:", self.__population[min_index])
            self.__scores[min_index] = score1

        min_score = min(self.__scores)
        min_index = self.__scores.index(min_score)

        if score2 > min_score:
            print("Replace parent 2 with individual", min_index + 1)
            print("Individual to be replaced:", self.__population[min_index])
            print("Parent 2", parent2)
            self.__population[min_index] = parent2
            print("New Individual:", self.__population[min_index])
            self.__scores[min_index] = score2

        self.__stable_replacement()
    
    def __stable_replacement(self):
        self.__custom_quicksort(0, len(self.__scores) - 1)

        for population_index in range(0, round(len(self.__scores)/2)):
            individual = list()
            for individual_index in range(self.__number_of_individual_genes):
                individual.append(round(uniform(-2.0, 2.0), 4))
            self.__population[population_index] = individual
        # checks the rest of the population for any invalid move individuals and replace them 
        for population_index in range(round(len(self.__scores)/2), len(self.__population)):
            if self.__scores[population_index] == -10000:
                individual = list()
                for individual_index in range(self.__number_of_individual_genes):
                    individual.append(round(uniform(-2.0, 2.0), 4))
                self.__population[population_index] = individual

    def __custom_quicksort(self, low, high):
        if low < high:
            # pi is partition index, self.__scores[p] is now at the right place
            pi = self.__custom_partition(low, high)

            # separately sort elements before partition and after partition
            self.__custom_quicksort(low, pi - 1)
            self.__custom_quicksort(pi + 1, high)

    def __custom_partition(self, low, high):
        index = low - 1     # index of smaller element
        pivot = self.__scores[high]   # pivot

        for j in range(low, high):
            # If current element is smaller than or equal to pivot
            if self.__scores[j] <= pivot:
                # increment index of smaller element
                index = index + 1
                self.__scores[index],self.__scores[j] = self.__scores[j], self.__scores[index]
                self.__population[index],self.__population[j] = self.__population[j], self.__population[index]
        self.__scores[index + 1],self.__scores[high] = self.__scores[high], self.__scores[index + 1]
        self.__population[index + 1], self.__population[high] = self.__population[high], self.__population[index + 1]
        return (index + 1)
            

    def __test_population(self):
        # test the current population and return the resulting scores
        # test_group function found in tester.py
        return self.__tester.test_group(self.__population)

    def run(self, layers_info, num_generations, number_of_individuals, number_of_individual_genes):
        self.__number_of_generations        = num_generations
        self.__number_of_individuals        = number_of_individuals
        self.__number_of_individual_genes   = number_of_individual_genes

        while self.__current_generation_num < self.__number_of_generations:
            self.__current_generation_num   += 1
            print("START GENERATION", self.__current_generation_num)
            print()
            if len(self.__population) > 0:
                for i in range(len(self.__population)):
                    print("Genes of individual", i + 1, ":", self.__population[i])
                    print("Score for individual", i + 1, ":", self.__scores[i])
                print()
            if self.__current_generation_num == 1:
                # create a brand new population
                print("GENERATE NEW POPULATION")
                print()
                self.__generate_new_population(layers_info)
                for i in range(len(self.__population)):
                    print("Genes of individual", i + 1, ":", self.__population[i])
                print()

            print("TEST POPULATION AT GENERATION", self.__current_generation_num)
            print()
            self.__scores = self.__test_population()

            self.__selection()
            print("RESULT OF GENERATION", self.__current_generation_num)
            print()
            # record the most recent population into the history of the genetic algorithm
            # self.__old_populations[self.__current_generation_num] = self.__population
            for i in range(len(self.__population)):
                print("Genes of individual", i + 1, ":", self.__population[i])
                print("Score for individual", i + 1, ":", self.__scores[i])
            print()
            output = "\nBest score for generation " + str(self.__current_generation_num) + ": " + str(self.__scores[len(self.__scores) - 1]) + "\n"
            write_to_file("GA.txt", output, "./Dumps/")
        # for generation_num in self.__old_populations.keys():
        #     print("Generation:", generation_num)
        #     for individual in self.__old_populations[generation_num]:
        #         print("Individual:", individual)
        print("GA run complete")
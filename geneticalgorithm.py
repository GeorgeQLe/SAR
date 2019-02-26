# Copyright 2019 George Le

class GeneticAlgorithm:

    def __init__(self):
        self.__current_generation_num   = 0
        self.__number_of_individuals    = 0
        self.__number_of_generations    = 0
        self.__old_populations          = { int : list }
        self.__population               = list

    def add_population(self):
        pass

    def __generate_new_population(self):
        pass

    def __test_population(self):
        pass

    def __output(self):
        pass
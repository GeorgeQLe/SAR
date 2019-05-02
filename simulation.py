# Copyright 2019 George Le

from environment import Environment
from searchagent import SearchAgent
from grader import grade

from collections import OrderedDict

class Simulation:

    def __init__(self):
        self.__environment          = Environment()
        self.__frequency_falsepos   = 0
        self.__searchagent          = SearchAgent()

    def __setup_test_environment(self, x = 10, y = 10):
        self.__environment.clear()
        self.__environment.generate(x, y)
        self.__environment.add_target()

    def __setup_search_agent(self, searchagent_genes = list()):
       self.__searchagent.set_brain(searchagent_genes)
       self.__environment.add_search_agent()

    def run_simulation(self, num_of_turns = 300):
        return_scores = list()

        for i in range(num_of_turns):
            # agent think and validation of the decision
            move_result = self.__environment.move_searchagent(self.__searchagent.agent_id(), self.__searchagent.think(self.__environment.get_adjacent_tiles(self.__searchagent.agent_id())))
            if move_result[1] == True:
                # agent move if the move is valid
                self.__searchagent.move(move_result[0])
                if self.__environment.check_target(self.__searchagent.agent_id()):
                    self.__searchagent.search_success()
            else:
                # if the move is invalid, returns a value far beyond the lowest possible value
                self.__searchagent.reset()
                return -10000
            # self.__environment.draw()
        return_scores = grade(self.__searchagent)
        self.__environment.clear()
        self.__searchagent.reset()
        return return_scores

    def setup_simulation(self, x = 10, y = 10, num_search_targets = 1, num_search_agents = 1, searchagent_genes = list()):
        self.__setup_test_environment(x, y)
        self.__setup_search_agent(searchagent_genes)
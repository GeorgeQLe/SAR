# Copyright 2019 George Le

from environment import Environment
from searchagents import SearchAgents, SearchAgentsType

class Simulation:

    def __init__(self):
        self.__environment          = Environment()
        self.__frequency_falsepos   = 0
        self.__target_locations     = {}
        self.__searchagents         = []

    def __generate_test_environment(self, x = 1, y = 1, num_search_targets = 1):
        self.__environment.set_environment(x, y, num_search_targets)

    def __generate_search_agents(self, num_search_agents = 1):
        for i in range(num_search_agents):
            temp = SearchAgents(SearchAgentsType.drone)
            self.__searchagents.append(temp)

    def generate_simulation(self, x = 1, y = 1, num_search_targets = 1, num_search_agents = 1):
        self.__generate_test_environment(x, y, num_search_agents)
        self.__generate_search_agents(num_search_agents)

    def run_simulation(self, num_of_turns = 30):
        self.__environment.generate(self.__frequency_falsepos)
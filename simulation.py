# Copyright 2019 George Le

from areatype import AreaType
from environment import Environment
from searchagents import SearchAgents, SearchAgentsType

class Simulation:

    def __init__(self):
        print("Simulation created")
        self.__environment          = Environment()
        self.__frequency_falsepos   = 0
        self.__target_locations     = {}
        self.__searchagents         = []

    def __setup_test_environment(self, x = 1, y = 1, areatype = AreaType.default, num_search_targets = 1):
        self.__environment.set_environment(x, y, areatype, num_search_targets)

    def __setup_search_agents(self, num_search_agents = 1):
        for i in range(num_search_agents):
            temp = SearchAgents(SearchAgentsType.drone)
            self.__searchagents.append(temp)

    def setup_simulation(self, x = 1, y = 1, areatype = AreaType.default, num_search_targets = 1, num_search_agents = 1):
        self.__setup_test_environment(x, y, areatype, num_search_agents)
        self.__setup_search_agents(num_search_agents)

    def run_simulation(self, num_of_turns = 30):
        self.__environment.generate(self.__frequency_falsepos)
        print("Environment generated")
        self.__environment.draw()
        for i in range(num_of_turns):
            pass     
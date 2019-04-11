# Copyright 2019 George Le

from areatype import AreaType
from grader import grade
from searchagent import Environment, NeuralNetwork, SearchAgent, SearchAgentsType

from collections import OrderedDict

class Simulation:

    def __init__(self):
        self.__environment          = Environment()
        self.__frequency_falsepos   = 0
        self.__searchagents         = list()

    def __setup_test_environment(self, x = 1, y = 1, areatype = AreaType.default, num_search_targets = 1):
        self.__environment.set_environment(x, y, areatype, num_search_targets)
        self.__environment.change_home_tile(0, 0)

    def __setup_search_agents(self, num_search_agents = 1, searchagents = list()):
        self.__searchagents.clear()
        if num_search_agents == 1:
            temp = SearchAgent(initial_position_x= 0, initial_position_y= 0, search_skill= 2, fuel_level= 100, max_fuel = 100, search_agent_type= SearchAgentsType.drone, ID= 1)
            temp.set_brain(searchagents)
            self.__searchagents.append(temp)
        else:
            # for each of the search agents, plug in a neural network into it
            for i in range(num_search_agents):
                temp = SearchAgent(initial_position_x= 0, initial_position_y= 0, search_skill= 2, fuel_level= 100, max_fuel = 100, search_agent_type= SearchAgentsType.drone, ID= i + 1)
                temp.set_brain(searchagents[i])
                self.__searchagents.append(temp)
        self.__environment.add_search_agents(num_search_agents)

    def run_simulation(self, num_of_turns = 300):
        return_scores = list()
        self.__environment.generate(self.__frequency_falsepos)

        for i in range(num_of_turns):
            # print("Turn", i + 1)
            for j in range(len(self.__searchagents)):
                self.__environment.move_search_agent(searchagent_ID= self.__searchagents[j].get_ID(), new_position= self.__searchagents[j].turn(self.__environment))
            # self.__environment.draw()
        for i in range(len(self.__searchagents)):
            return_scores.append(grade(agent= self.__searchagents[i]))

        if len(self.__searchagents) == 1:
            return_scores = return_scores[0]
        self.__environment.empty()
        return return_scores

    def setup_simulation(self, x = 1, y = 1, areatype = AreaType.default, num_search_targets = 1, num_search_agents = 1, searchagents = list()):
        self.__setup_test_environment(x, y, areatype, num_search_agents)
        self.__setup_search_agents(num_search_agents, searchagents)
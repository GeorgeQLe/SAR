# Copyright 2019 George Le

from areatype import AreaType
from searchagent import Environment, NeuralNetwork, SearchAgent, SearchAgentsType

class Simulation:

    def __init__(self):
        print("Simulation created")
        self.__environment          = Environment()
        self.__frequency_falsepos   = 0
        self.__searchagents         = list()

    def __setup_test_environment(self, x = 1, y = 1, areatype = AreaType.default, num_search_targets = 1):
        print("Setup test environment")
        self.__environment.set_environment(x, y, areatype, num_search_targets)

    def __setup_search_agents(self, num_search_agents = 1, population = list()):
        if len(population) != num_search_agents:
            if len(population) > num_search_agents:
                difference_population = len(population) - num_search_agents
                for i in range(difference_population):
                    population.pop()
            elif len(population) < num_search_agents:
                difference_population = num_search_agents - len(population)
                for i in range(difference_population):
                    temp_nn = NeuralNetwork(num_layers= 3)
                    temp_nn.create_layer(index= 0, size= 9, size_of_next_layer= 4)
                    temp_nn.create_layer(index= 1, size= 4, size_of_next_layer= 9)
                    temp_nn.create_layer(index= 2, size= 9, last_layer= True)
                    population.append(temp_nn)
        # creates a temp population in case there are neuron weights that need to plugged into 
        # neural networks in the population
        temp_population = population
        for nn in population:
            if not isinstance(nn, NeuralNetwork):
                temp_nn = NeuralNetwork()
                # TODO

        print("Start creating Search Agent")
        for i in range(num_search_agents):
            temp = SearchAgent(search_agent_type= SearchAgentsType.drone)
            temp.set_brain(population[i])
            self.__searchagents.append(temp)
        self.__environment.add_search_agents(num_search_agents)

    def run_simulation(self, num_of_turns = 30):
        self.__environment.generate(self.__frequency_falsepos)
        print("Environment generated")
        for i in range(num_of_turns):
            print("Turn", i + 1)
            for searchagent in self.__searchagents:
                searchagent.resolve_turn(self.__environment)
        self.__environment.empty()

    def setup_simulation(self, x = 1, y = 1, areatype = AreaType.default, num_search_targets = 1, num_search_agents = 1, searchagents = list()):
        self.__setup_test_environment(x, y, areatype, num_search_agents)
        self.__setup_search_agents(num_search_agents, searchagents)
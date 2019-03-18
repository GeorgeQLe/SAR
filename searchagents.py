# Copyright 2019 George Le

import enum

from environment import AdjacentTiles, Environment
from neuralnetwork import NeuralNetwork, NeuralNetworkInputs
from tile import resolve_tiletype_as_float, TileType

class SearchAgentsType(enum.Enum):
    human = 0
    drone = 1

class SearchAgents:
    def __init__(self, search_agent_type = SearchAgentsType.human):
        self.__brain            = NeuralNetwork()
        
        self.__fuel_level       = 0
        self.__max_fuel         = 0
        self.__position         = (0, 0)
        self.__steps_taken      = 0
        self.__targets_found    = 0
        self.__turns_taken      = 0
        self.__type             = search_agent_type

    def __get_adjacent_tiles(self, environment = Environment()):
        return environment.search_adjacent_tiles(self.__position[0], self.__position[1])

    def __move(self, adjacent_tiles = AdjacentTiles()):
        # reduce the amount of fuel the search agent has by one
        self.__fuel_level -= 1

    def __search(self, environment):
        pass

    def __think(self, environment = Environment(), current_tiletype = TileType.void):
        adjacent_tiles = self.__get_adjacent_tiles(environment)
        adj_list = adjacent_tiles.listify()
        adj_list.append(resolve_tiletype_as_float(current_tiletype))

        decision_list = self.__brain.evaluate(NeuralNetworkInputs(adj_list))
        decision = decision_list.index(max(decision_list))
        if decision == 0:
            pass
        elif decision == 1:
            pass
        elif decision == 2:
            pass
        elif decision == 3:
            pass
        elif decision == 4:
            pass
        elif decision == 5:
            pass
        elif decision == 6:
            pass
        elif decision == 7:
            pass
        elif decision == 8:
            pass

    def resolve_turn(self, environment):
        self.__think(self.__get_adjacent_tiles(environment))

    def set_brain(self, new_brain = NeuralNetwork()):
        self.__brain = new_brain
# Copyright 2019 George Le

import enum

from environment import AdjacentTiles, Environment
from neuralnetwork import NeuralNetwork, NeuralNetworkInputs
from tile import resolve_tiletype_as_float, TileTargetInfo, TileType

class Direction(enum.IntEnum):
    STAY    = 0
    NW      = 1
    N       = 2
    NE      = 3
    E       = 4
    SE      = 5
    S       = 6
    SW      = 7
    W       = 8

class SearchAgentsType(enum.Enum):
    human = 0
    drone = 1

class SearchAgents:
    def __init__(self, search_agent_type = SearchAgentsType.human):
        self.__brain            = NeuralNetwork()
        
        self.__fuel_level       = 0
        self.__max_fuel         = 0
        self.__position         = (0, 0)
        self.__search_skill     = 2
        self.__steps_taken      = 0
        self.__targets_found    = 0
        self.__turns_taken      = 0
        self.__type             = search_agent_type

    def __get_adjacent_tiles(self, environment = Environment()):
        return environment.search_adjacent_tiles(self.__position[0], self.__position[1])

    def __move(self, direction = 0, environment = Environment()):
        if (self.__fuel_level + 1) > self.__max_fuel:
            pass
        # reduce the amount of fuel the search agent has by one
        self.__fuel_level    -= 1
        self.__steps_taken   += 1

    def __search(self, environment = Environment()):
        # return the result of a search on the current tile it is on
        return environment.search_tile(self.__position[0], self.__position[1], self.__search_skill)

    def __think(self, environment = Environment(), current_tiletype = TileType.void):
        adjacent_tiles = self.__get_adjacent_tiles(environment)
        adj_list = adjacent_tiles.listify()
        adj_list.append(resolve_tiletype_as_float(current_tiletype))

        decision_list = self.__brain.evaluate(NeuralNetworkInputs(adj_list))
        decision = decision_list.index(max(decision_list))
        if decision == 0:
            self.__search(environment)
        elif decision >= 1 and decision <= 8:
            self.__move(decision, environment)

    def resolve_turn(self, environment):
        self.__think(self.__get_adjacent_tiles(environment))
        self.__turns_taken += 1

    def set_brain(self, new_brain = NeuralNetwork()):
        self.__brain = new_brain
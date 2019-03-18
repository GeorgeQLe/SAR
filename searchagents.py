# Copyright 2019 George Le

import enum

from environment import AdjacentTiles, Environment
from neuralnetwork import NeuralNetwork, NeuralNetworkInputs
from tile import resolve_tiletype_as_float, TileTargetInfo, TileType

from collections import OrderedDict

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

class Move_Error(enum.IntEnum):
    NOTENOUGHFUEL   = 0
    MOVEOUTOFBOUND  = 1

class SearchAgentsType(enum.Enum):
    human = 0
    drone = 1

class SearchAgents:
    def __init__(self, initial_position_x = 0, initial_position_y = 0, search_skill = 2, fuel_level = 0, max_fuel = 0, search_agent_type = SearchAgentsType.human):
        self.__brain            = NeuralNetwork()
        self.__fuel_level       = fuel_level
        self.__max_fuel         = max_fuel
        self.__path_taken       = OrderedDict()
        self.__position         = (initial_position_x, initial_position_y)
        self.__search_skill     = search_skill
        self.__steps_taken      = 0
        self.__targets_found    = 0
        self.__turns_taken      = 0
        self.__type             = search_agent_type

    def __get_adjacent_tiles(self, environment = Environment()):
        return environment.search_adjacent_tiles(self.__position[0], self.__position[1])

    def __move(self, direction = 0, environment = Environment()):
        # checks to see if the search agent has enough fuel to move
        if (self.__fuel_level + 1) > self.__max_fuel:
            return False
        # create a temp coordinates
        new_coord = list(self.__position)

        if direction == Direction.NW:
            new_coord[0] -= 1 # x - 1
            new_coord[1] += 1 # y + 1
        elif direction == Direction.N:
            new_coord[1] += 1 # y + 1
        elif direction == Direction.NE:
            new_coord[0] += 1 # x + 1
            new_coord[1] += 1 # y + 1
        elif direction == Direction.E:
            new_coord[0] += 1 # x + 1
        elif direction == Direction.SE:
            new_coord[0] += 1 # x + 1
            new_coord[1] -= 1 # y - 1
        elif direction == Direction.S:
            new_coord[1] -= 1 # y - 1
        elif direction == Direction.SW:
            new_coord[0] -= 1 # x - 1
            new_coord[1] -= 1 # y - 1
        elif direction == Direction.W:
            new_coord[0] -= 1 # x - 1
        elif direction == Direction.STAY:
            # stay is only for the home tile and lets the search agent refuel
            self.__fuel_level = self.__max_fuel

        if environment.check_tile(new_coord[0], new_coord[1]) == False:
            return False
        # reduce the amount of fuel the search agent has by one
        self.__fuel_level    -= 1
        self.__steps_taken   += 1
        self.__position      = tuple(new_coord)

    def __search(self, environment = Environment()):
        self.__fuel_level   -= 1
        self.__steps_taken  += 1
        # return the result of a search on the current tile it is on
        return environment.search_tile(self.__position[0], self.__position[1], self.__search_skill)

    def __think(self, environment = Environment(), current_tiletype = TileType.void):
        adjacent_tiles = self.__get_adjacent_tiles(environment)
        adj_list = adjacent_tiles.listify()
        adj_list.append(resolve_tiletype_as_float(current_tiletype))

        decision_list = self.__brain.evaluate(NeuralNetworkInputs(adj_list))
        decision = decision_list.index(max(decision_list))
        if decision == 0 and not environment.check_home(self.__position[0], self.__position[1]):
            self.__search(environment)
        else:
            self.__move(decision, environment)

    def resolve_turn(self, environment):
        self.__think(self.__get_adjacent_tiles(environment))
        self.__turns_taken += 1

    def set_brain(self, new_brain = NeuralNetwork()):
        self.__brain = new_brain
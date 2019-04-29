# Copyright 2019 George Le

import enum

from direction import resolve_decision_as_direction
from environment import Environment
from file import write_to_file
from neuralnetwork import NeuralNetwork
from tiletype import TileType

from collections import OrderedDict
from random import randint


class Move_Error(enum.IntEnum):
    NOTENOUGHFUEL   = 0
    MOVEOUTOFBOUND  = 1

class SearchAgentsType(enum.Enum):
    human = 0
    drone = 1

class SearchAgent:
    def __init__(self, initial_position_x = 0, initial_position_y = 0, search_skill = 2, fuel_level = 0, max_fuel = 0, search_agent_type = SearchAgentsType.human, ID = 0):
        self.__brain            = NeuralNetwork()   # the controller of the SearchAgent class
        self.__ID               = ID
        self.__type             = search_agent_type
        
        self.__empty_fuel       = False
        self.__max_fuel         = max_fuel
        self.__fuel_level       = fuel_level
        
        self.__invalid_moves    = 0
        self.__path_taken       = OrderedDict()
        self.__position         = (initial_position_x, initial_position_y)
        self.__steps_taken      = 0
        self.__turns_taken      = 0
        self.__random_choices   = 0
        
        self.__falsepos_list    = list() # a list of the coordinates of false positives that the SearchAgent class found
        self.__search_skill     = search_skill
        self.__targets_found    = 0

    def __search(self, environment = Environment()):
        # return the result of a search on the current tile it is on
        return environment.search_tile(self.__position[0], self.__position[1], self.__search_skill)

    def __think(self, adjacent_tiles = list()):
        nn_inputs = adjacent_tiles
        nn_inputs = self.__targets_found

        decision = self.__brain.evaluate(nn_inputs)

        # return a direction
        return resolve_decision_as_direction(decision)

    def turn(self, environment):
        self.__turns_taken += 1
        return self.__think(environment)

    def set_brain(self, new_brain = list()):
        self.__brain = NeuralNetwork(bias=0, num_layers=3, layers_info=dict({
                                                            0 : (9, 5),
                                                            1 : (5, 1)
                                                            }), num_weights= 50, weights= new_brain)
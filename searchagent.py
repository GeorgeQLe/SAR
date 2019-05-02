# Copyright 2019 George Le

import enum

from coord import Coord
from direction import resolve_decision_as_direction
from file import write_to_file
from neuralnetwork import NeuralNetwork
from tiletype import TileType

from collections import OrderedDict
from random import randint

class SearchAgentsType(enum.Enum):
    human = 0
    drone = 1

class SearchAgent:
    def __init__(self, initial_position_x = 0, initial_position_y = 0, search_skill = 2, fuel_level = 0, max_fuel = 0, search_agent_type = SearchAgentsType.human, ID = 0):
        self.__brain            = NeuralNetwork()   # the controller of the SearchAgent class
        self.__ID               = ID
        # self.__type             = search_agent_type
        
        self.__empty_fuel       = False
        self.__max_fuel         = max_fuel
        self.__fuel_level       = fuel_level
        
        self.__path_taken       = OrderedDict()
        self.__path_taken[0]    = (0, 0)

        self.__steps_taken      = 0
        self.__turns_taken      = 0
        
        # self.__falsepos_list    = list() # a list of the coordinates of false positives that the SearchAgent class found
        # self.__search_skill     = search_skill
        self.__targets_found    = 0

    def reset(self):
        self.__brain = None
        self.__empty_fuel = False
        self.__fuel_level = self.__max_fuel

        self.__path_taken.clear()
        self.__steps_taken = 0
        self.__turns_taken = 0
        self.__targets_found = 0

    """
        These three functions should be called sequentially: first think, then move, and finally search
    """
    def think(self, adjacent_tiles = list()):
        self.__turns_taken += 1
        nn_inputs = adjacent_tiles
        nn_inputs.append(self.__targets_found)
        decision = self.__brain.evaluate(nn_inputs)
        # return a direction
        return resolve_decision_as_direction(decision)
    def move(self, new_pos):
        self.__steps_taken+=1
        self.__path_taken[self.__turns_taken] = new_pos
    def search_success(self):
        self.__targets_found+=1
    def agent_id(self):
        return self.__ID
    def num_repeats(self):
        return len(self.__path_taken) - len(set(self.__path_taken.values()))
    def steps(self):
        return self.__steps_taken
    def target_found(self):
        return self.__targets_found
    def successful_return(self):
        if self.__targets_found > 0:
            if self.__path_taken[0] == self.__path_taken[self.__turns_taken]:
                return 1
        else:
            return 0

    def set_brain(self, new_brain = list()):
        self.__brain = NeuralNetwork(bias=0, num_layers=3, layers_info=dict({
                                                            0 : (9, 5),
                                                            1 : (5, 1)
                                                            }), num_weights= 50, weights= new_brain)

    
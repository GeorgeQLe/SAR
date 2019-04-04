# Copyright 2019 George Le

import enum

from environment import AdjacentTiles, Environment
from neuralnetwork import NeuralNetwork
from tile import resolve_tiletype_as_float, TileTargetInfo, TileType

from collections import OrderedDict
from random import randint

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

class SearchAgent:
    def __init__(self, initial_position_x = 0, initial_position_y = 0, search_skill = 2, fuel_level = 0, max_fuel = 0, search_agent_type = SearchAgentsType.human, ID = 0):
        self.__brain            = NeuralNetwork()
        self.__falsepos_list    = [ (int, int) ]
        self.__fuel_level       = fuel_level
        self.__ID               = ID
        self.__invalid_moves    = 0
        self.__max_fuel         = max_fuel
        self.__empty_fuel       = False
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
        print("Moving")
        # checks to see if the search agent has enough fuel to move
        if (self.__fuel_level - 1) < 0:
            print("No fuel")
            if environment.check_home(self.__position[0], self.__position[1]):
                # stay is only for the home tile and lets the search agent refuel
                self.__fuel_level = self.__max_fuel
                print("Refueled")
            else:
                print("Out of fuel")
                return Move_Error.NOTENOUGHFUEL
        print("Old Position:", self.__position)
        new_coord       = tuple()
        
        direction_nine  = True
        while direction_nine:
            print(direction)
            if direction == Direction.NW:
                print("Move NW")
                new_coord = (self.__position[0] - 1 , self.__position[1] + 1)
                direction_nine = False
            elif direction == Direction.N:
                print("Move N")
                new_coord = (self.__position[0], self.__position[1] + 1)
                direction_nine = False
            elif direction == Direction.NE:
                print("Move NE")
                new_coord = (self.__position[0] + 1, self.__position[1] + 1)
                direction_nine = False
            elif direction == Direction.E:
                print("Move E")
                new_coord = (self.__position[0] + 1, self.__position[1])
                direction_nine = False
            elif direction == Direction.SE:
                print("Move SE")
                new_coord = (self.__position[0] + 1, self.__position[1] - 1)
                direction_nine = False
            elif direction == Direction.S:
                print("Move S")
                new_coord = (self.__position[0], self.__position[1] - 1)
                direction_nine = False
            elif direction == Direction.SW:
                print("Move SW")
                new_coord = (self.__position[0] - 1, self.__position[1] - 1)
                direction_nine = False
            elif direction == Direction.W:
                print("Move W")
                new_coord = (self.__position[0] + 1, self.__position[1])
                direction_nine = False
            elif direction == Direction.STAY:
                print("Stay")
                new_coord = (self.__position[0], self.__position[1])
                direction_nine = False
            elif direction == 9 or direction == 10:
                print("Random movement")
                direction = randint(0, 8)
        print(new_coord)
        # checks to make sure that the new coordinates are actually in the environment
        if environment.check_tile(new_coord[0], new_coord[1]) == False:
            print("Out of bounds")
            return Move_Error.MOVEOUTOFBOUND
        # reduce the amount of fuel the search agent has by one
        self.__fuel_level    -= 1
        # increment the number of steps taken by one
        self.__steps_taken   += 1
        # update the new position of the search agent
        self.__position      = new_coord
        return self.__search(environment)

    def __search(self, environment = Environment()):
        # return the result of a search on the current tile it is on
        return environment.search_tile(self.__position[0], self.__position[1], self.__search_skill)

    def __think(self, environment = Environment(), current_tiletype = TileType.void):
        adjacent_tiles = self.__get_adjacent_tiles(environment)
        nn_inputs = adjacent_tiles.listify()
        nn_inputs.append(float(self.__fuel_level))

        decision = self.__brain.evaluate(nn_inputs)
        decision = int(round(decision, 1) * 10)

        move_result = self.__move(direction=decision, environment=environment)
        if isinstance(move_result, TileTargetInfo):
            if move_result == TileTargetInfo.falsepos:
                self.__falsepos_list.append(self.__position)
            elif move_result == TileTargetInfo.target:
                self.__targets_found += 1
        elif isinstance(move_result, Move_Error):
            if move_result == Move_Error.MOVEOUTOFBOUND:
                self.__invalid_moves += 1
            elif move_result == Move_Error.NOTENOUGHFUEL:
                self.__empty_fuel = True
        self.__path_taken[self.__turns_taken] = self.__position
        return self.__position

    def empty_fuel(self):
        return self.__empty_fuel
    def falsepos_found(self):
        return len(self.__falsepos_list) - 1
    def fuel_level(self):
        return self.__fuel_level
    def get_ID(self):
        return self.__ID
    def invalid_moves(self):
        return self.__invalid_moves
    def num_of_repeats(self):
        return len(self.__falsepos_list) - len(set(self.__falsepos_list))
    def path_taken(self):
        return self.__path_taken
    def steps(self):
        return self.__steps_taken
    def targets_found(self):
        return self.__targets_found
    def turns_taken(self):
        return self.__turns_taken

    def turn(self, environment):
        self.__turns_taken += 1
        return self.__think(environment)

    def set_brain(self, new_brain = list()):
        self.__brain = NeuralNetwork(bias=0, num_layers=3, layers_info=dict({
                                                            0 : (9, 4),
                                                            1 : (4, 1)
                                                            }), num_weights= 40, weights= new_brain)
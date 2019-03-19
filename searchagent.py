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

class SearchAgent:
    def __init__(self, initial_position_x = 0, initial_position_y = 0, search_skill = 2, fuel_level = 0, max_fuel = 0, search_agent_type = SearchAgentsType.human, ID = 0):
        self.__brain            = NeuralNetwork()
        self.__falsepos_list    = [ (int, int) ]
        self.__fuel_level       = fuel_level
        self.__ID               = ID
        self.__max_fuel         = max_fuel
        self.__path_taken       = OrderedDict()
        self.__position         = (initial_position_x, initial_position_y)
        self.__search_skill     = search_skill
        self.__steps_taken      = 0
        self.__targets_found    = 0
        self.__turns_taken      = 0
        self.__type             = search_agent_type

    def fuel_level(self):
        return self.__fuel_level

    def path_taken(self):
        return self.__path_taken

    def steps(self):
        return self.__steps_taken

    def targets_found(self):
        return self.__targets_found

    def turns_taken(self):
        return self.__turns_taken

    def __get_adjacent_tiles(self, environment = Environment()):
        print("Search adjacent tiles to:", self.__position[0], self.__position[1])
        return environment.search_adjacent_tiles(self.__position[0], self.__position[1])

    def __move(self, direction = 0, environment = Environment()):
        print("Moving")
        # checks to see if the search agent has enough fuel to move
        if (self.__fuel_level - 1) < 0:
            print("No fuel")
            print(environment.check_home(self.__position[0], self.__position[1]))
            if environment.check_home(self.__position[0], self.__position[1]):
                # stay is only for the home tile and lets the search agent refuel
                self.__fuel_level = self.__max_fuel
                print("Refueled")
            else:
                print("Out of fuel")
                return False

        new_coord = None
        if direction == Direction.NW:
            print("Moved up left")
            new_coord = (self.__position[0] - 1 , self.__position[1] + 1)
        elif direction == Direction.N:
            print("Moved up")
            new_coord = (self.__position[0], self.__position[1] + 1) 
        elif direction == Direction.NE:
            print("Moved up right")
            new_coord = (self.__position[0] + 1, self.__position[1] + 1)
        elif direction == Direction.E:
            print("Moved right")
            new_coord = (self.__position[0] + 1, self.__position[1]) 
        elif direction == Direction.SE:
            print("Moved down right")
            new_coord = (self.__position[0] + 1, self.__position[1] - 1)
        elif direction == Direction.S:
            print("Moved down")
            new_coord = (self.__position[0], self.__position[1] - 1)
        elif direction == Direction.SW:
            print("Moved down left")
            new_coord = (self.__position[0] - 1, self.__position[1] - 1)
        elif direction == Direction.W:
            print("Moved left")
            new_coord = (self.__position[0] + 1, self.__position[1])
        elif direction == Direction.STAY:
            print("Stayed in place")
        print("Checking:", new_coord)
        # checks to make sure that the new coordinates are actually in the environment
        if environment.check_tile(new_coord[0], new_coord[1]) == False:
            print("Not in grid, no move")
            return False
        # reduce the amount of fuel the search agent has by one
        self.__fuel_level    -= 1
        # increment the number of steps taken by one
        self.__steps_taken   += 1
        # update the new position of the search agent\
        print("New coordinates:", new_coord)
        self.__position      = new_coord
        return True

    def __search(self, environment = Environment()):
        print("Searching")
        self.__fuel_level   -= 1
        self.__steps_taken  += 1
        # return the result of a search on the current tile it is on
        return environment.search_tile(self.__position[0], self.__position[1], self.__search_skill)

    def __think(self, environment = Environment(), current_tiletype = TileType.void):
        adjacent_tiles = self.__get_adjacent_tiles(environment)
        adj_list = adjacent_tiles.listify()
        adj_list.append(resolve_tiletype_as_float(current_tiletype))

        self.__path_taken[self.__turns_taken] = self.__position

        decision_list = self.__brain.evaluate(NeuralNetworkInputs(adj_list))
        decision = decision_list.index(max(decision_list))
        print("Decision:", decision)
        if decision == 0 and not environment.check_home(self.__position[0], self.__position[1]):
            search_result = self.__search(environment) 
            if isinstance(search_result, TileTargetInfo):
                if search_result == TileTargetInfo.falsepos:
                    self.__falsepos_list.append(self.__position)
                elif search_result == TileTargetInfo.target:
                    self.__targets_found += 1
            elif isinstance(self.__search(environment), bool):
                pass
        else:
            if self.__move(decision, environment):
                print("New position:", self.__position)
                return self.__position
            else:
                print("New position:", self.__position)
                return False

    def get_ID(self):
        return self.__ID

    def turn(self, environment):
        self.__turns_taken += 1
        self.__think(environment)

    def set_brain(self, new_brain = NeuralNetwork()):
        self.__brain = new_brain

def resolve_turn(return_value):
    pass
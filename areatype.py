# Copyright 2019 George Le

from collections import OrderedDict

from tile import TileType

import enum
import random

class AreaType(enum.Enum):
    default = 0
    islands = 1
    mountain_range = 2
    rural_fields = 3
    swampland = 4
    woodlands = 5

class AreaTileProbabilities:
    def __init__(self):
        # Tuple of key-value pairs - corresponding to the probabilities of 
        # the tiletypes in a particular areatype
        self.__default =        [(TileType.forest, 1), 
                                (TileType.mountain, 3),
                                (TileType.plains, 5), 
                                (TileType.pond, 7), 
                                (TileType.river, 9), 
                                (TileType.swamp, 10)]

        self.__islands =        [(TileType.forest, 3),
                                (TileType.mountain, 4),
                                (TileType.plains, 6),
                                (TileType.pond, 6),
                                (TileType.river, 11),
                                (TileType.swamp, 11)]

        self.__mountain_range = [(TileType.forest, 2),
                                (TileType.mountain, 8),
                                (TileType.plains, 8),
                                (TileType.pond, 8),
                                (TileType.river, 11),
                                (TileType.swamp, 11)]

        self.__rural_fields =   [(TileType.forest, 1),
                                (TileType.mountain, 1),
                                (TileType.plains, 9),
                                (TileType.pond, 10),
                                (TileType.river, 11),
                                (TileType.swamp, 11)]

        self.__swamplands =     [(TileType.forest, 3),
                                (TileType.mountain, 3),
                                (TileType.plains, 3),
                                (TileType.pond, 4),
                                (TileType.river, 5),
                                (TileType.swamp, 11)]

        self.__woodlands =      [(TileType.forest, 5),
                                (TileType.mountain, 7),
                                (TileType.plains, 8),
                                (TileType.pond, 9),
                                (TileType.river, 10),
                                (TileType.swamp, 11)]

    def get_tile_type(self, random_num, areatype = AreaType.default):
        # print(areatype)
        tile_probabilities = self.get_values(areatype)
        # accessing the individual elements of the tile probabilities' 
        # inner dict ;)
        for probability in tile_probabilities.keys():
            # if the randomly generated number is less than the value of the 
            # assigned hard-coded probabilities for each of the tile types
            if random_num < tile_probabilities[probability]:
                return probability 

    def get_values(self, areatype = AreaType.default):
        if areatype == AreaType.islands:
            return OrderedDict(self.__islands)
        elif areatype == AreaType.mountain_range:
            return OrderedDict(self.__mountain_range)
        elif areatype == AreaType.rural_fields:
            return OrderedDict(self.__rural_fields)
        elif areatype == AreaType.swampland:
            return OrderedDict(self.__swamplands)
        elif areatype == AreaType.woodlands:
            return OrderedDict(self.__woodlands)
        print("Shouldn't get here")
        return OrderedDict(self.__default)

def generate_random_tile(areatype = AreaType.default, highest_possible_roll = 10):
    tile_probabilities = AreaTileProbabilities()
    # get a random number between 1 and the desired highest possible roll for a 
    # random tile
    roll = random.randint(0, highest_possible_roll)
    # returns the tile that corresponds to the areatype of the environment
    return tile_probabilities.get_tile_type(roll, areatype)
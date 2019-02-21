# Copyright 2019 George Le

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
        self.__tile_probabilities = {
            AreaType.default : {
                TileType.forest     : 1,
                TileType.mountain   : 3,
                TileType.plains     : 5,
                TileType.pond       : 7,
                TileType.river      : 9,
                TileType.swamp      : 11
            },
            AreaType.islands : {
                TileType.forest     : 3,
                TileType.mountain   : 5,
                TileType.plains     : 7,
                TileType.pond       : 7,
                TileType.river      : 11,
                TileType.swamp      : 11
            },
            AreaType.mountain_range : {
                TileType.forest     : 2,
                TileType.mountain   : 6,
                TileType.plains     : 7,
                TileType.pond       : 8,
                TileType.river      : 10,
                TileType.swamp      : 11
            },
            AreaType.rural_fields : {
                TileType.forest     : 1,
                TileType.mountain   : 1,
                TileType.plains     : 9,
                TileType.pond       : 10,
                TileType.river      : 11,
                TileType.swamp      : 11
            },
            AreaType.swampland : {
                TileType.forest     : 3,
                TileType.mountain   : 3,
                TileType.plains     : 3,
                TileType.pond       : 4,
                TileType.river      : 5,
                TileType.swamp      : 11
            },
            AreaType.woodlands : {
                TileType.forest     : 5,
                TileType.mountain   : 7,
                TileType.plains     : 8,
                TileType.pond       : 9,
                TileType.swamp      : 10,
                TileType.river      : 11
            }
        }

    def get_tile_type(self, random_num, areatype = AreaType.default):
        # accessing the individual elements of the tile probabilities' inner dict ;)
        for probability in self.__tile_probabilities[areatype].keys():
            # if the randomly generated number is less than the value of the 
            # assigned hard-coded probabilities for each of the tile types
            if random_num < self.__tile_probabilities[areatype][probability]:
                return probability

def generate_random_tile(areatype = AreaType.default):
    tile_probabilities = AreaTileProbabilities()
    # get a random number between 1 and 10
    roll = random.randint(0, 10)
    # returns the tile that corresponds to the areatype of the environment
    return tile_probabilities.get_tile_type(roll, areatype)
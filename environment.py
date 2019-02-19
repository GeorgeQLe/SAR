# Copyright 2019 George Le

from areatype import AreaType, AreaTileProbabilities, generate_random_tile
from collections import defaultdict
from tile import DisregardTile, Tile, TileType

import random

class AdjacentTiles:

    def __init__(self):
        # there are a total of 8 tiles adjacent to the caller tile
        # initially, these adjacent tiles are set to void which if
        # used should be disregarded
        self.NW = TileType.void
        self.N  = TileType.void
        self.NE = TileType.void
        self.E  = TileType.void
        self.SE = TileType.void
        self.S  = TileType.void
        self.SW = TileType.void
        self.W  = TileType.void

    # this function allows for the environment class to load the AdjacentTiles class with the current tile's
    # adjacent tiles
    def add_tiles(self, NW = TileType.void, N = TileType.void, NE = TileType.void, E = TileType.void,
                 SE = TileType.void, S = TileType.void, SW = TileType.void, W = TileType.void):
        self.NW = NW
        self.N  = N
        self.NE = NE
        self.E  = E
        self.SE = SE
        self.S  = S
        self.SW = SW
        self.W  = W

    # this is the main workhorse of the AdjacentTiles class
    def generate_tiletype_from_adj(self, areatype):
        temp = self.__count_tile_probabilities(areatype)
        random_roll = random.randint(1, 111)
        print(random_roll)
        print(temp)
        if random_roll >= 100:
            print("Generate random tile")
            return generate_random_tile(areatype)
        for probability in temp.keys():
            print(probability, ":", temp[probability])
            if temp[probability] < random_roll:
                print("Selected:", probability)
                return probability
        return generate_random_tile(areatype)

    def __add_probability(self, return_probabilities, tiletype, individual_probabilities):
        if tiletype != TileType.void and tiletype != TileType.home:
            return_probabilities[tiletype] += individual_probabilities
        return return_probabilities

    def __check_tile(self):
        disregard       = DisregardTile()
        disregarded_num = 0
        
        # the following determines if the adjacent tiles should be disregarded (if
        # they are )
        if disregard.check_tile(self.NW):
            disregarded_num += 1
        if disregard.check_tile(self.N):
            disregarded_num += 1
        if disregard.check_tile(self.NE):
            disregarded_num += 1
        if disregard.check_tile(self.E):
            disregarded_num += 1
        if disregard.check_tile(self.SE):
            disregarded_num += 1
        if disregard.check_tile(self.S):
            disregarded_num += 1
        if disregard.check_tile(self.SW):
            disregarded_num += 1
        if disregard.check_tile(self.W):
            disregarded_num += 1

        if disregarded_num == len(TileType):
            return 0

        return 100.0 / (len(TileType) - disregarded_num)

    def __count_tile_probabilities(self, areatype):
        individual_probabilities = self.__check_tile()
        return_probabilities = { TileType : float }

        # checks to see if the adjacent tiles are relevant (if this is the first time,
        # )
        if individual_probabilities == 0:
            return { }

        # set all of the adjacent tiles' probabilities to 0.0
        for tiletype in TileType:
            return_probabilities[tiletype] = 0.0

        # records the probabilities for each of the eight adjacent tiles
        return_probabilities = self.__add_probability(return_probabilities, self.NW, individual_probabilities)
        return_probabilities = self.__add_probability(return_probabilities, self.N, individual_probabilities)
        return_probabilities = self.__add_probability(return_probabilities, self.NE, individual_probabilities)
        return_probabilities = self.__add_probability(return_probabilities, self.E, individual_probabilities)
        return_probabilities = self.__add_probability(return_probabilities, self.SE, individual_probabilities)
        return_probabilities = self.__add_probability(return_probabilities, self.S, individual_probabilities)
        return_probabilities = self.__add_probability(return_probabilities, self.SW, individual_probabilities)
        return_probabilities = self.__add_probability(return_probabilities, self.W, individual_probabilities)

        return return_probabilities

class Environment:

    """----------------------------------------------------------------------------

        This class is used by the class simulation in order to train and test
        search agents. This environment runs using 5E D&D rules: grids are 5x5 ft,
        each round takes 6 seconds, agents can move in eight cardinal directions,
        and the grid is made up of tiles that loosely correspond to the MTG lands -
        (the only amend is islands would be a pain to program so they are instead
        switched out for rivers and ponds)

    ----------------------------------------------------------------------------"""

    def __init__(self, areatype = AreaType.default, x = 0, y = 0, num_targets = 0):
        self.__areatype             = areatype
        self.__grid                 = { (int, int) : Tile }
        self.__list_of_falsepos     = { (int, int) }
        self.__num_targets          = num_targets
        self.__x                    = x
        self.__y                    = y

        # this is a setup variable that should only be used during the set up of the simulation environment
        self.__generated_num_of_targets = 0
        self.__good_grid = False

    def __generate_null_tile(self, x, y):
        # creates a temp tile that will be returned by the function
        temp = Tile(x=x, y=y)
        temp.set_target(False)
        temp.set_tile_type(TileType.void)
        return temp

    def __generate_tile(self, x, y, frequency_falsepos):
        # creates a temp tile that will be returned by the function
        temp = Tile(x=x, y=y)
        
        # for the origin
        if x == 0 and y == 0:
            # the tile at the origin is set as home
            temp.set_tile_type(TileType.home)
            return temp
        # if there needs to be more targets, see if this tile will be randomly selected as a target
        if self.__generated_num_of_targets < self.__num_targets:
            # randomly roll to see if the generated tile be a target
            random_roll = random.randint(1, 101)
            if random_roll < 51:
                # randomly roll to see if the new target is a false positive
                random_roll = random.randint(1, 101)
                if random_roll < frequency_falsepos:
                    temp.set_target(True)
                else:
                    temp.set_target(False)
                    # the target only counts to the number of valid generated targets if it is not a falsepos
                    self.__generated_num_of_targets += 1
        # generates a tile from the adjacent tiles to the current tile
        temp_tiletype = self.search_adjacent_tiles(x, y).generate_tiletype_from_adj(self.__areatype)
        
        temp.set_tile_type(temp_tiletype)

        return temp

    def empty(self):
        """-----------------------------------------------------------------------------------------------------

            This function clears the environment and sets the environment to not good so that it cant be used.
        
        -----------------------------------------------------------------------------------------------------"""
        self.__grid.clear()
        self.__good_grid = False

    def generate(self, frequency_falsepos):
        for x in range(self.__x):
            for y in range(self.__y):
                print(x, ",", y, "Initial Add Null Tile")
                self.__grid[x, y] = self.__generate_null_tile(x, y)

        for y in range(self.__x):
            for x in range(self.__y):
                print(x, ",", y)
                self.__grid[x, y] = self.__generate_tile(x, y, frequency_falsepos)
                print("Grid at:", x, ",", y, "Tiletype:", self.__grid[x, y].tiletype())

    def search_adjacent_tiles(self, x, y):
        return_adjacent_tiles = AdjacentTiles()
        if x >= self.__x or y >= self.__y:
            return return_adjacent_tiles

        # for tiles in the center of the environment grid
        if x > 0 and x < self.__x - 1 and y > 0 and y < self.__y - 1:
            print("center of grid")
            return_adjacent_tiles.add_tiles(NW=self.__grid[x - 1, y + 1].tiletype(),
                                            N=self.__grid[x, y + 1].tiletype(), 
                                            NE=self.__grid[x + 1, y + 1].tiletype(),
                                            E=self.__grid[x + 1, y].tiletype(),
                                            SE=self.__grid[x + 1, y - 1].tiletype(),
                                            S=self.__grid[x, y - 1].tiletype(),
                                            SW=self.__grid[x - 1, y + 1].tiletype(),
                                            W=self.__grid[x - 1, y].tiletype())
        elif x == 0 and y == 0: # for tiles in the origin and the bottom left corner
            print("origin or bottom left corner")
            return_adjacent_tiles.add_tiles(N=self.__grid[x, y + 1].tiletype(), 
                                            NE=self.__grid[x + 1, y + 1].tiletype(),
                                            E=self.__grid[x + 1, y].tiletype())
        elif x == 0 and y == self.__y - 1: # for tile in top left corner
            print("top left corner")
            return_adjacent_tiles.add_tiles(E=self.__grid[x + 1, y].tiletype(),
                                            SE=self.__grid[x + 1, y - 1].tiletype(),
                                            S=self.__grid[x, y - 1].tiletype())
        elif x == self.__x - 1 and y == self.__y - 1: # for tile in top right corner
            print("top right corner")
            return_adjacent_tiles.add_tiles(S=self.__grid[x, y - 1].tiletype(),
                                            SW=self.__grid[x - 1, y + 1].tiletype(),
                                            W=self.__grid[x - 1, y].tiletype())
        elif x == self.__x - 1 and y == 0: # for tile in bottom right corner
            print("bottom right corner")
            return_adjacent_tiles.add_tiles(NW=self.__grid[x - 1, y + 1].tiletype(),
                                            N=self.__grid[x, y + 1].tiletype(),
                                            W=self.__grid[x - 1, y].tiletype())
        elif x == 0 and y > 0: # for tiles in left side
            print("left side")
            return_adjacent_tiles.add_tiles(N=self.__grid[x, y + 1].tiletype(), 
                                            NE=self.__grid[x + 1, y + 1].tiletype(),
                                            E=self.__grid[x + 1, y].tiletype(),
                                            SE=self.__grid[x + 1, y - 1].tiletype(),
                                            S=self.__grid[x, y - 1].tiletype())
        elif x == self.__x - 1 and y > 0: # for tiles in right side
            print("right side")
            return_adjacent_tiles.add_tiles(NW=self.__grid[x - 1, y + 1].tiletype(),
                                            N=self.__grid[x, y + 1].tiletype(), 
                                            S=self.__grid[x, y - 1].tiletype(),
                                            SW=self.__grid[x - 1, y + 1].tiletype(),
                                            W=self.__grid[x - 1, y].tiletype())
        elif x > 0 and y == 0: # for tiles in bottom row
            print("bottom row")
            return_adjacent_tiles.add_tiles(NW=self.__grid[x - 1, y + 1].tiletype(),
                                            N=self.__grid[x, y + 1].tiletype(), 
                                            NE=self.__grid[x + 1, y + 1].tiletype(),
                                            E=self.__grid[x + 1, y].tiletype(),
                                            W=self.__grid[x - 1, y].tiletype())
        elif x > 0 and y == self.__y - 1: # for tiles in the top row
            print("top row")
            return_adjacent_tiles.add_tiles(E=self.__grid[x + 1, y].tiletype(),
                                            SE=self.__grid[x + 1, y - 1].tiletype(),
                                            S=self.__grid[x, y - 1].tiletype(),
                                            SW=self.__grid[x - 1, y + 1].tiletype(),
                                            W=self.__grid[x - 1, y].tiletype())
        return return_adjacent_tiles

    def set_environment(self, x = 1, y = 1, num_targets = 1):
        self.__x            = x
        self.__y            = y
        self.__num_targets  = num_targets

    def set_environment_details(self, areatype = AreaType.default):
        self.__areatype = areatype
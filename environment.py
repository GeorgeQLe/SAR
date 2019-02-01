# Copyright 2019 George Le

from areatype import AreaType, AreaTileProbabilities, generate_random_tile
from collections import defaultdict
from tile import DisregardTile, Tile, TileType

import random

class AdjacentTiles:
    def __init__(self):
        self.NW = TileType.void
        self.N  = TileType.void
        self.NE = TileType.void
        self.E  = TileType.void
        self.SE = TileType.void
        self.S  = TileType.void
        self.SW = TileType.void
        self.W  = TileType.void

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

    def generate_tiletype_from_adj(self, areatype):
        temp = self.__count_tile_probabilities(areatype)
        random_roll = random.randint(1, 111)
        if random_roll >= 100:
            return generate_random_tile(areatype)
        for probability in temp.keys():
            if temp[probability] < random_roll:
                return probability

    def __add_probability(self, return_probabilities, tiletype, individual_probabilities):
        if tiletype != TileType.void and tiletype != TileType.home:
            return_probabilities[tiletype] += individual_probabilities
        return return_probabilities

    def __check_tile(self):
        disregard       = DisregardTile()
        disregarded_num = 0

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

        if individual_probabilities == 0:
            return { }

        for tiletype in TileType:
            return_probabilities[tiletype] = 0.0

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

    def __init__(self, areatype = AreaType.default, x = 0, y = 0, num_targets = 0):
        self.__areatype             = areatype
        self.__grid                 = { int : { int : Tile } }
        self.__list_of_falsepos     = { int : int }
        self.__num_targets          = num_targets
        self.__x                    = x
        self.__y                    = y

    def __generate_null_tile(self, x, y):
        temp = Tile(x, y)
        temp.set_target(False)
        temp.set_tile_type(TileType.void)

    def __generate_tile(self, x, y, frequency_falsepos):
        temp = Tile(x, y)
        if x == 0 and y == 0:
            temp.set_target(False)
            temp.set_tile_type(TileType.home)
            return temp
        random_roll = random.randint(1, 101)
        if random_roll < frequency_falsepos:
            temp.set_target(True)
        else:
            temp.set_target(False)
        temp_tiletype = self.search_adjacent_tiles(x, y).generate_tiletype_from_adj(self.__areatype)
        temp.set_tile_type(temp_tiletype)
        return temp

    def empty(self):
        self.__grid.clear()

    def generate(self, frequency_falsepos):
        for i in range(self.__x):
            for j in range(self.__y):
                print(i, ",", j)
                self.__grid[i] = { j : self.__generate_null_tile(i, j) }
        for i in range(self.__x):
            for j in range(self.__y):
                self.__grid[i][j] = self.__generate_tile(i, j, frequency_falsepos)

    def search_adjacent_tiles(self, x, y):
        return_adjacent_tiles = AdjacentTiles()
        print(x, ",", y)
        if x >= self.__x or y >= self.__y:
            return return_adjacent_tiles

        if x > 0 and x < self.__x and y > 0 and y < self.__y:
            return_adjacent_tiles.add_tiles(NW=self.__grid[x - 1][y + 1].tiletype(),
                                            N=self.__grid[x][y + 1].tiletype(), 
                                            NE=self.__grid[x + 1][y + 1].tiletype(),
                                            E=self.__grid[x + 1][y].tiletype(),
                                            SE=self.__grid[x + 1][y - 1].tiletype(),
                                            S=self.__grid[x][y - 1].tiletype(),
                                            SW=self.__grid[x - 1][y + 1].tiletype(),
                                            W=self.__grid[x - 1][y].tiletype())
        elif x == 0 and y == 0: # the origin and the bottom left corner
            return_adjacent_tiles.add_tiles(N=self.__grid[x][y + 1].tiletype(), 
                                            NE=self.__grid[x + 1][y + 1].tiletype(),
                                            E=self.__grid[x + 1][y].tiletype())
        elif x == 0 and y == self.__y - 1: # top left corner
            return_adjacent_tiles.add_tiles(E=self.__grid[x + 1][y].tiletype(),
                                            SE=self.__grid[x + 1][y - 1].tiletype(),
                                            S=self.__grid[x][y - 1].tiletype())
        elif x == self.__x - 1 and y == self.__y - 1: # top right corner
            return_adjacent_tiles.add_tiles(S=self.__grid[x][y - 1].tiletype(),
                                            SW=self.__grid[x - 1][y + 1].tiletype(),
                                            W=self.__grid[x - 1][y].tiletype())
        elif x == self.__x - 1 and y == 0: # bottom right corner
            return_adjacent_tiles.add_tiles(NW=self.__grid[x - 1][y + 1].tiletype(),
                                            N=self.__grid[x][y + 1].tiletype(),
                                            W=self.__grid[x - 1][y].tiletype())
        elif x == 0 and y > 0: # left side
            return_adjacent_tiles.add_tiles(N=self.__grid[x][y + 1].tiletype(), 
                                            NE=self.__grid[x + 1][y + 1].tiletype(),
                                            E=self.__grid[x + 1][y].tiletype(),
                                            SE=self.__grid[x + 1][y - 1].tiletype(),
                                            S=self.__grid[x][y - 1].tiletype())
        elif x == self.__x - 1 and y > 0: # right side
            return_adjacent_tiles.add_tiles(NW=self.__grid[x - 1][y + 1].tiletype(),
                                            N=self.__grid[x][y + 1].tiletype(), 
                                            S=self.__grid[x][y - 1].tiletype(),
                                            SW=self.__grid[x - 1][y + 1].tiletype(),
                                            W=self.__grid[x - 1][y].tiletype())
        elif x > 0 and y == 0: 
            return_adjacent_tiles.add_tiles(NW=self.__grid[x - 1][y + 1].tiletype(),
                                            N=self.__grid[x][y + 1].tiletype(), 
                                            NE=self.__grid[x + 1][y + 1].tiletype(),
                                            E=self.__grid[x + 1][y].tiletype(),
                                            W=self.__grid[x - 1][y].tiletype())
        elif x > 0 and y == self.__y - 1:
            return_adjacent_tiles.add_tiles(E=self.__grid[x + 1][y].tiletype(),
                                            SE=self.__grid[x + 1][y - 1].tiletype(),
                                            S=self.__grid[x][y - 1].tiletype(),
                                            SW=self.__grid[x - 1][y + 1].tiletype(),
                                            W=self.__grid[x - 1][y].tiletype())
        return return_adjacent_tiles

    def set_environment(self, x = 1, y = 1, num_targets = 1):
        self.__x            = x
        self.__y            = y
        self.__num_targets  = num_targets

    def set_environment_details(self, areatype = AreaType.default):
        self.__areatype = areatype
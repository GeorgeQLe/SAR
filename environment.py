# Copyright 2019 George Le

from areatype import AreaType, AreaTileProbabilities, generate_random_tile
from collections import defaultdict
from tile import DisregardTile, get_tiletypes_after, resolve_tiletype_as_float, Tile, TileTargetInfo, TileType

import random

class AdjacentTiles:

    def __init__(self):
        """-----------------------------------------------------------
            There are a total of 8 tiles adjacent to the caller tile.
            Initially, these adjacent tiles are set to void which if
            used should be disregarded.
        -----------------------------------------------------------"""
        self.NW = TileType.void
        self.N  = TileType.void
        self.NE = TileType.void
        self.E  = TileType.void
        self.SE = TileType.void
        self.S  = TileType.void
        self.SW = TileType.void
        self.W  = TileType.void

    def __add_probability(self, return_probabilities, tiletype, add_probability):
        """---------------------------------------------------------------------------------

            Adds a value to the probability to the dict that stores the key-value pair:
            { tiletype : probability } 
        
        ---------------------------------------------------------------------------------"""
        if tiletype != TileType.void or tiletype != TileType.home:
            print(get_tiletypes_after(tiletype))
            for index_types in get_tiletypes_after(tiletype):
                return_probabilities[index_types] += add_probability
        return return_probabilities

    def __check_tile(self):
        """---------------------------------------------------------------------------------

            This function checks each of the adjacent tiles to the center tile to determine
            if any of the adjacent tiles' tiletype should be disregarded. Most common uses
            for this function is when the grid is being initialized and there are "null"
            tiles on the grid with void tiles and when the center tile is on the edges of
            the grid where an adjacent tile may not exist and thus must be disregarded.
            This function returns the modifier to the probability of a generated tile.
        
        ---------------------------------------------------------------------------------"""
        disregard       = DisregardTile()
        disregarded_num = 0
        
        # the following determines if the adjacent tiles should be disregarded (if
        # they are void or home)
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

        # this is for the first two tiles, to return zero
        if disregarded_num == 8:
            return 0.0
        print("Disregard num:", 8 / (8 - disregarded_num))
        return 8 / (8 - disregarded_num)

    def __count_tile_probabilities(self, areatype):
        """---------------------------------------------------------------------------------

            This function determines how much each tiletype is worth which is used to
            calculate the probability for each tiletype. It bases any modification to the
            probabilities on how many of a certain tiletype exists within the adjacent tiles
            of the center tile and whether the tiletype is not to be included in the 
            simulation.
        
        ---------------------------------------------------------------------------------"""
        individual_probability_modifier = self.__check_tile()
        return_probabilities = AreaTileProbabilities().get_values(areatype=areatype)
        print("Return probabilities: ", return_probabilities)

        # checks to see if the adjacent tiles are relevant (if this is the first time,
        # )
        # set all of the adjacent tiles' probabilities to 0.0
        # for tiletype in TileType:
        #     return_probabilities[tiletype] = 0.0
        
        if individual_probability_modifier == 0:
            return return_probabilities
        
        print("NW: ", self.NW, ", N: ", self.N, ", NE: ", self.NE, ", E: ", self.E, ", SE: ", self.SE, ", S: ", self.S, ", SW: ", self.SW, ", W: ", self.W)
        # modifies the probabilities for each of the eight adjacent tiles
        return_probabilities = self.__add_probability(return_probabilities, self.NW, individual_probability_modifier)
        print("NW")
        print("NW: ", self.NW, ", N: ", self.N, ", NE: ", self.NE, ", E: ", self.E, ", SE: ", self.SE, ", S: ", self.S, ", SW: ", self.SW, ", W: ", self.W)
        return_probabilities = self.__add_probability(return_probabilities, self.N, individual_probability_modifier)
        print("N")
        print("NW: ", self.NW, ", N: ", self.N, ", NE: ", self.NE, ", E: ", self.E, ", SE: ", self.SE, ", S: ", self.S, ", SW: ", self.SW, ", W: ", self.W)
        return_probabilities = self.__add_probability(return_probabilities, self.NE, individual_probability_modifier)
        print("NE")
        print("NW: ", self.NW, ", N: ", self.N, ", NE: ", self.NE, ", E: ", self.E, ", SE: ", self.SE, ", S: ", self.S, ", SW: ", self.SW, ", W: ", self.W)
        return_probabilities = self.__add_probability(return_probabilities, self.E, individual_probability_modifier)
        print("E")
        print("NW: ", self.NW, ", N: ", self.N, ", NE: ", self.NE, ", E: ", self.E, ", SE: ", self.SE, ", S: ", self.S, ", SW: ", self.SW, ", W: ", self.W)
        return_probabilities = self.__add_probability(return_probabilities, self.SE, individual_probability_modifier)
        print("SE")
        print("NW: ", self.NW, ", N: ", self.N, ", NE: ", self.NE, ", E: ", self.E, ", SE: ", self.SE, ", S: ", self.S, ", SW: ", self.SW, ", W: ", self.W)
        return_probabilities = self.__add_probability(return_probabilities, self.S, individual_probability_modifier)
        print("S")
        print("NW: ", self.NW, ", N: ", self.N, ", NE: ", self.NE, ", E: ", self.E, ", SE: ", self.SE, ", S: ", self.S, ", SW: ", self.SW, ", W: ", self.W)
        return_probabilities = self.__add_probability(return_probabilities, self.SW, individual_probability_modifier)
        print("SW")
        print("NW: ", self.NW, ", N: ", self.N, ", NE: ", self.NE, ", E: ", self.E, ", SE: ", self.SE, ", S: ", self.S, ", SW: ", self.SW, ", W: ", self.W)
        return_probabilities = self.__add_probability(return_probabilities, self.W, individual_probability_modifier)
        print("W")
        print("NW: ", self.NW, ", N: ", self.N, ", NE: ", self.NE, ", E: ", self.E, ", SE: ", self.SE, ", S: ", self.S, ", SW: ", self.SW, ", W: ", self.W)
        return return_probabilities 

    # this function allows for the environment class to load the AdjacentTiles class with the current tile's
    # adjacent tiles
    def add_tiles(self, NW = TileType.void, N = TileType.void, NE = TileType.void, E = TileType.void,
                 SE = TileType.void, S = TileType.void, SW = TileType.void, W = TileType.void):
        """---------------------------------------------------------------------------------

            This function serves as a setter function for this AdjacentTiles class
        
        ---------------------------------------------------------------------------------"""
        self.NW = NW
        self.N  = N
        self.NE = NE
        self.E  = E
        self.SE = SE
        self.S  = S
        self.SW = SW
        self.W  = W

    # this is the main workhorse of the AdjacentTiles class
    def generate_tiletype_from_adj(self, areatype = AreaType.default):
        """-----------------------------------------------------------------------------------

            This function determines the probabilities that each tiletype have of being
            returned by this function to be the assigned as the tiletype for the center tile.
        
        ----------------------------------------------------------------------------------"""
        temp = self.__count_tile_probabilities(areatype)
        random_roll = random.randint(1, 111)
        print("Random roll:", random_roll)
        print("Temp:", temp)
        if random_roll >= 100:
            print("Generate random tile")
            return generate_random_tile(areatype)
        for probability in temp.keys():
            print("Generate from existing")
            print("Probability:", probability, ":", temp[probability])
            random_roll = random.randint(0, 11)
            if temp[probability] > random_roll:
                print("Selected:", probability)
                return probability
        return generate_random_tile(areatype)

    def listify(self):
        return_list = list()
        
        return_list.append(resolve_tiletype_as_float(self.NW))
        return_list.append(resolve_tiletype_as_float(self.N))
        return_list.append(resolve_tiletype_as_float(self.NE))
        return_list.append(resolve_tiletype_as_float(self.E))
        return_list.append(resolve_tiletype_as_float(self.SE))
        return_list.append(resolve_tiletype_as_float(self.S))
        return_list.append(resolve_tiletype_as_float(self.SW))
        return_list.append(resolve_tiletype_as_float(self.W))
        
        return return_list

class Environment:
    """-----------------------------------------------------------------------------

        This class is used by the class simulation in order to train and test
        search agents. This environment runs using 5E D&D rules: grids are 5x5 ft,
        each round takes 6 seconds, agents can move in eight cardinal directions,
        and the grid is made up of tiles that loosely correspond to the MTG lands -
        (the only amend is islands would be a pain to program so they are instead
        switched out for rivers and ponds).

    -----------------------------------------------------------------------------"""
    def __init__(self, areatype = AreaType.default, x = 0, y = 0, num_targets = 0):
        self.__areatype             = areatype
        self.__grid                 = { (int, int) : Tile }
        self.__targets              = { (int, int) : TileTargetInfo }
        self.__num_targets          = num_targets
        self.__x                    = x
        self.__y                    = y

        # this is a setup variable that should only be used during the set up of the simulation environment
        self.__generated_num_of_targets = 0
        self.__good_grid = False

    def __generate_null_tile(self, x, y):
        """---------------------------------------------------------------------------------

            This function creates a non-usaable tile to be used to initialize the grid.
        
        ---------------------------------------------------------------------------------"""
        # creates a temp tile that will be returned by the function
        temp = Tile(x=x, y=y)
        temp.set_target(False)
        temp.set_tile_type(TileType.void)
        return temp

    def __generate_tile(self, x, y, frequency_falsepos):
        """---------------------------------------------------------------

            This function controls how the environment class generates a
            tile at a certain coordinate.
            
        ---------------------------------------------------------------"""
        # creates a temp tile that will be returned by the function
        temp = Tile(x=x, y=y)
        
        # for the origin
        if x == 0 and y == 0:
            # the tile at the origin is set as home
            temp.set_tile_type(TileType.home)
            return temp
        
        # generates a tile from the adjacent tiles to the current tile
        temp_tiletype = self.search_adjacent_tiles(x, y).generate_tiletype_from_adj(self.__areatype)
        temp.set_tile_type(temp_tiletype)

        return temp

    def draw(self):
        """------------------------------------------------------------------

            This function prints out the various representations of the
            grid's tile to stdout. The representations are based on the
            tiletype of the tile and taking priority over the tiletype,
            is whether the tile is a target (or falsepos) for the search 
            agent.

        ------------------------------------------------------------------"""
        if self.__good_grid == True:
            for i in range(self.__x * 2 + 1):
                print("-", end="")
            print()
            for y in range(self.__y):
                print("|", end="")
                for x in range(self.__x):
                    if self.__grid[x, y].is_falsepos() == True:
                        print("O", end="|")
                    elif self.__grid[x, y].is_target() == True:
                        print("X", end="|")
                    elif self.__grid[x, y].tiletype() == TileType.home:
                        print("H", end="|")
                    elif self.__grid[x, y].tiletype() == TileType.forest:
                        print("Y", end="|")
                    elif self.__grid[x, y].tiletype() == TileType.mountain:
                        print("^", end="|")
                    elif self.__grid[x, y].tiletype() == TileType.plains:
                        print("_", end="|")
                    elif self.__grid[x, y].tiletype() == TileType.pond:
                        print("=", end="|")
                    elif self.__grid[x, y].tiletype() == TileType.river:
                        print("~", end="|")
                    elif self.__grid[x, y].tiletype() == TileType.swamp:
                        print(".", end="|")
                print("")
                for i in range(self.__x * 2 + 1):
                    print("-", end="")
                print()
            print()

    def empty(self):
        """-----------------------------------------------------------------------------------------------------

            This function clears the environment and sets the environment to not good so that it cant be used.
        
        -----------------------------------------------------------------------------------------------------"""
        self.__grid.clear()
        self.__good_grid = False

    def generate(self, frequency_falsepos):
        """---------------------------------------------------------------

            This function creates the grid in a pseudo-random manner.
        
        ---------------------------------------------------------------"""
        # initialize the grid and fills it with "null" tiles
        for x in range(self.__x):
            for y in range(self.__y):
                self.__grid[x, y] = self.__generate_null_tile(x, y)
        # pseudo-randomly generate tiles on the grid
        for y in range(self.__x):
            for x in range(self.__y):
                print("Tile at: ", x, ",", y)
                self.__grid[x, y] = self.__generate_tile(x, y, frequency_falsepos)

        # generates the tiles for the grid
        while self.__generated_num_of_targets < self.__num_targets:
            # randomly roll to get the coordinate for the new target/falsepos
            random_x = random.randint(0, self.__x - 1)
            random_y = random.randint(0, self.__y - 1)

            # randomly roll to see if the new target is a false positive
            random_roll = random.randint(1, 101)

            # checks to see if the random roll warrants the tile being a target or falsepos
            if random_roll < frequency_falsepos:
                print("Set target - falsepos")
                self.__grid[random_x, random_y].set_target(True)
                self.__targets[random_x, random_y] = TileTargetInfo.falsepos
            else:
                print("Set target")
                self.__grid[random_x, random_y].set_target(False)
                self.__targets[random_x, random_y] = TileTargetInfo.target
                # the target only counts to the number of valid generated targets if it is not a falsepos
                self.__generated_num_of_targets += 1
        
        # the grid now is ready for use
        self.__good_grid = True

    def search_adjacent_tiles(self, x, y):
        """-------------------------------------------------------------------------------

            This function searches the adjacent tiles (in all eight cardinal directions)
            and returns a class that contains the tiletype of the eight adjacent tiles.
        
        -------------------------------------------------------------------------------"""
        # creates a temp AdjacentTiles class to be returned by this function
        return_adjacent_tiles = AdjacentTiles()
        # checks to make sure that the passed in tile is within the confines of the grid
        if x >= self.__x or y >= self.__y:
            return return_adjacent_tiles

        # for tiles in the center of the environment grid
        if x > 0 and x < self.__x - 1 and y > 0 and y < self.__y - 1:
            return_adjacent_tiles.add_tiles(NW=self.__grid[x - 1, y + 1].tiletype(),
                                            N=self.__grid[x, y + 1].tiletype(), 
                                            NE=self.__grid[x + 1, y + 1].tiletype(),
                                            E=self.__grid[x + 1, y].tiletype(),
                                            SE=self.__grid[x + 1, y - 1].tiletype(),
                                            S=self.__grid[x, y - 1].tiletype(),
                                            SW=self.__grid[x - 1, y + 1].tiletype(),
                                            W=self.__grid[x - 1, y].tiletype())
        elif x == 0 and y == 0: # for tiles in the origin and the bottom left corner
            return_adjacent_tiles.add_tiles(N=self.__grid[x, y + 1].tiletype(), 
                                            NE=self.__grid[x + 1, y + 1].tiletype(),
                                            E=self.__grid[x + 1, y].tiletype())
        elif x == 0 and y == self.__y - 1: # for tile in top left corner
            return_adjacent_tiles.add_tiles(E=self.__grid[x + 1, y].tiletype(),
                                            SE=self.__grid[x + 1, y - 1].tiletype(),
                                            S=self.__grid[x, y - 1].tiletype())
        elif x == self.__x - 1 and y == self.__y - 1: # for tile in top right corner
            return_adjacent_tiles.add_tiles(S=self.__grid[x, y - 1].tiletype(),
                                            SW=self.__grid[x - 1, y - 1].tiletype(),
                                            W=self.__grid[x - 1, y].tiletype())
        elif x == self.__x - 1 and y == 0: # for tile in bottom right corner
            return_adjacent_tiles.add_tiles(NW=self.__grid[x - 1, y + 1].tiletype(),
                                            N=self.__grid[x, y + 1].tiletype(),
                                            W=self.__grid[x - 1, y].tiletype())
        elif x == 0 and y > 0: # for tiles in left side
            return_adjacent_tiles.add_tiles(N=self.__grid[x, y + 1].tiletype(), 
                                            NE=self.__grid[x + 1, y + 1].tiletype(),
                                            E=self.__grid[x + 1, y].tiletype(),
                                            SE=self.__grid[x + 1, y - 1].tiletype(),
                                            S=self.__grid[x, y - 1].tiletype())
        elif x == self.__x - 1 and y > 0: # for tiles in right side
            return_adjacent_tiles.add_tiles(NW=self.__grid[x - 1, y + 1].tiletype(),
                                            N=self.__grid[x, y + 1].tiletype(), 
                                            S=self.__grid[x, y - 1].tiletype(),
                                            SW=self.__grid[x - 1, y + 1].tiletype(),
                                            W=self.__grid[x - 1, y].tiletype())
        elif x > 0 and y == 0: # for tiles in bottom row
            return_adjacent_tiles.add_tiles(NW=self.__grid[x - 1, y + 1].tiletype(),
                                            N=self.__grid[x, y + 1].tiletype(), 
                                            NE=self.__grid[x + 1, y + 1].tiletype(),
                                            E=self.__grid[x + 1, y].tiletype(),
                                            W=self.__grid[x - 1, y].tiletype())
        elif x > 0 and y == self.__y - 1: # for tiles in the top row
            return_adjacent_tiles.add_tiles(E=self.__grid[x + 1, y].tiletype(),
                                            SE=self.__grid[x + 1, y - 1].tiletype(),
                                            S=self.__grid[x, y - 1].tiletype(),
                                            SW=self.__grid[x - 1, y - 1].tiletype(),
                                            W=self.__grid[x - 1, y].tiletype())
        return return_adjacent_tiles

    def search_tile(self, x = 1, y = 1, falsepos_rate = 0):
        coord = (x, y)
        if coord in self.__targets.keys():
            if random.randint(1, 10) > falsepos_rate:
                pass

    def set_environment(self, x = 1, y = 1, areatype = AreaType.default, num_targets = 1):
        """------------------------------------------------------------------

            This function is the setter function for the environment class.
        
        ------------------------------------------------------------------"""
        self.__areatype     = areatype
        self.__num_targets  = num_targets
        self.__x            = x
        self.__y            = y
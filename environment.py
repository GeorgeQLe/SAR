# Copyright 2019 George Le

from collections import defaultdict
from adjacenttiles import AdjacentTiles, AreaType, TileType
from tile import Tile, TileTargetInfo

from collections import OrderedDict
import random

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
        self.__grid                 = OrderedDict()
        self.__home_coord           = (0, 0)
        self.__num_targets          = num_targets
        self.__searchagents         = { int : (int, int) } # search agent ID : coordinates
        self.__targets              = { (int, int) : TileTargetInfo }
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

    def add_search_agents(self, num_searchagents = 0):
        for i in range(num_searchagents - 1):
            self.__searchagents[i] = self.__home_coord

    def change_home_tile(self, x = 0, y = 0):
        self.__home_coord = (x, y)

    def check_home(self, x = 0, y = 0):
        if self.check_tile(x, y) == True:
            if self.__grid[x, y] == TileType.home:
                return True
        return False

    def check_tile(self, x = 0, y = 0):
        """---------------------------------------------------------------

            This function checks to see if the tile is in the grid. If it 
            is return True, if not return False.
            
        ---------------------------------------------------------------"""
        coord = (x, y)
        # checks to see if the coordinates are in the grid
        for grid_coord in self.__grid.keys():
            if grid_coord == coord:
                return True
        return False
        

    def draw(self):
        """------------------------------------------------------------------

            This function prints out the various representations of the
            grid's tile to stdout. The representations are based on the
            tiletype of the tile and taking priority over the tiletype,
            is whether the tile is a target (or falsepos) for the search 
            agent.

        ------------------------------------------------------------------"""
        print("Search agents info")
        for i in range(len(self.__searchagents) - 1):
            print(self.__searchagents[i + 1])
        if self.__good_grid == True:
            for i in range(self.__x * 2 + 1):
                print("-", end="")
            print()
            for y in range(self.__y):
                print("|", end="")
                for x in range(self.__x):
                    has_agent = False
                    for i in range(len(self.__searchagents) - 1):
                        if self.__searchagents[i + 1] == (x, y):
                            print("1", end="|")
                            has_agent = True
                            break
                    if has_agent != True:
                        if self.__grid[x, y].tiletype() == TileType.home:
                            print("H", end="|")
                        if self.__grid[x, y].is_falsepos() == True:
                            print("O", end="|")
                        elif self.__grid[x, y].is_target() == True:
                            print("X", end="|")
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
                # print("Tile at: ", x, ",", y)
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
                # print("Set target - falsepos")
                self.__grid[random_x, random_y].set_target(True)
                self.__targets[random_x, random_y] = TileTargetInfo.falsepos
            else:
                # print("Set target")
                self.__grid[random_x, random_y].set_target(False)
                self.__targets[random_x, random_y] = TileTargetInfo.target
                # the target only counts to the number of valid generated targets if it is not a falsepos
                self.__generated_num_of_targets += 1
        
        # the grid now is ready for use
        self.__good_grid = True

    def get_number_of_targets(self):
        return len(self.__targets)

    def get_tiletype_at_coord(self, x = 0, y = 0):
        if self.check_tile(x, y) == True:
            return self.__grid[x, y].tiletype()

    def move_search_agent(self, searchagent_ID = -1, new_position = (-1, -1)):
        self.__searchagents[searchagent_ID] = new_position

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

    def search_tile(self, x = 1, y = 1, search_skill = 2):
        coord = (x, y)
        if coord in self.__targets.keys():
            # if the current tile triggers a false positive, give the search agent a chance to resolve
            # the falsepositive
            if self.__targets[coord] == TileTargetInfo.falsepos and random.randint(1, 10) <= search_skill:
                self.__targets.pop(coord)
                return TileTargetInfo.falsepos
            elif self.__targets[coord] == TileTargetInfo.target:
                self.__targets.pop(coord)
                return TileTargetInfo.target
        else:
            return TileTargetInfo.empty

    def set_environment(self, x = 1, y = 1, areatype = AreaType.default, num_targets = 1):
        """------------------------------------------------------------------

            This function is the setter function for the environment class.
        
        ------------------------------------------------------------------"""
        self.__areatype     = areatype
        self.__num_targets  = num_targets
        self.__x            = x
        self.__y            = y
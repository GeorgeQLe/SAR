# Copyright 2019 George Le

from collections import OrderedDict
from random import randint

from coord import Coord
from direction import Direction, northwest, north, northeast, east, southeast, south, southwest, west
from tiletype import TileType

class Environment:

    def __init__(self, x_max = 10, y_max = 10):
        self.x              = x_max  # specifies the max x coordinate
        self.y              = y_max  # specifies the max y coordinate

        self.grid           = dict() # a dict which holds a key-value pair of Coord to Tiletype

        self.num_agents     = 0      # holds the number of search agents that are currently in the environment grid
        self.searchagents   = list() # list of coordinates for the search agents currently in the environment grid

        self.num_targets    = 0      # holds the number of targets that are still in the environment grid
        self.target_coords  = list() # list of coordinates for the targets currently in the environment grid
        self.target_set     = False  # boolean value which tracks whether or not a target has been created in the grid
        self.total_targets  = 0      # hold the total number of targets that are in the environment grid

    def add_search_agent(self, start_coord = Coord(0, 0), num_search_agents = 1):
        if num_search_agents >= 1:
            for i in range(num_search_agents):
                self.searchagents.append(start_coord)

    def add_target(self, random = True, set_location = Coord(0, 0)):
        if random == True:
            self.target_coords.append(Coord(randint(0, self.x - 1), randint(0, self.y - 1)))
            self.num_targets+=1
            self.total_targets+=1
        else:
            self.target_coords.append(set_location)
            self.num_targets+=1
            self.total_targets+=1
        self.target_set = True
    def add_targets(self, random = True, target_locations = list(), num_targets = 1):
        if len(target_locations) == 0:
            return
        if random == True:
            for i in range(num_targets):
                self.target_coords.append(Coord(randint(0, self.x - 1), randint(0, self.y - 1)))
            self.num_targets+=num_targets
            self.total_targets+=num_targets
        else:
            for location in target_locations:
                if isinstance(location, Coord):
                    self.target_coords.append(location)
            self.num_targets+=num_targets
            self.total_targets+=num_targets
        self.target_set = True

    def check_target(self, potential_coord):
        if potential_coord in self.target_coords:
            self.found_target(potential_coord)
            return True
        return False
    def found_target(self, found_coord = Coord(0, 0)):
        self.target_coords.remove(found_coord)
        self.num_targets-=1

    def remove_target(self, remove_coord = Coord(0, 0)):
        if self.total_targets == 0:
            return
        else:
            self.target_coords.remove(remove_coord)
            self.num_targets-=1
            self.total_targets-=1
    def remove_all_targets(self):
        if self.total_targets == 0:
            return
        else:
            self.target_coords.clear()
            self.num_targets = 0
            self.target_set = False
            self.total_targets = 0

    def draw(self):
        pass

    def generate(self):
        for y in range(self.y):
            for x in range(self.x):
                random_roll = randint(1, 100)
                if random_roll < 90:
                    self.grid[Coord(x, y)] = TileType.empty
                else:
                    self.grid[Coord(x, y)] = TileType.obstacle
        for target_coord in self.target_coords:
            self.grid[target_coord] = TileType.target
    def clear(self):
        self.grid.clear()

    def move_searchagent(self, agent_id, direction = Direction()):
        pass
    def get_adjacent_tiles(self, agent_id):
        return_tiletypes    = list() # list of tiletypes of the tiles adjacent to the current agent
        current_coord       = self.searchagents[agent_id]

        # get the northwest tiletype
        nw                  = northwest(current_coord)
        if nw in self.grid.keys():
            # appends to the list of tiletypes to be returned 
            return_tiletypes.append(self.grid[nw])
        else:
            # choosen coordinate is outside the grid so therefore is a wall
            return_tiletypes.append(TileType.wall)

        # get the north tiletype
        n                   = north(current_coord)
        if n in self.grid.keys():
            return_tiletypes.append(self.grid[n])
        else:
            # choosen coordinate is outside the grid so therefore is a wall
            return_tiletypes.append(TileType.wall)

        # get the northeast tiletype
        ne                  = northeast(current_coord)
        if ne in self.grid.keys():
            return_tiletypes.append(self.grid[ne])
        else:
            # choosen coordinate is outside the grid so therefore is a wall
            return_tiletypes.append(TileType.wall)

        # get the east tiletype
        e                   = east(current_coord)
        if e in self.grid.keys():
            return_tiletypes.append(self.grid[e])
        else:
            # choosen coordinate is outside the grid so therefore is a wall
            return_tiletypes.append(TileType.wall)

        # get the southeast tiletype
        se                  = southeast(current_coord)
        if se in self.grid.keys():
            return_tiletypes.append(self.grid[se])
        else:
            # choosen coordinate is outside the grid so therefore is a wall
            return_tiletypes.append(TileType.wall)

        # get the south tiletype
        s                   = south(current_coord)
        if s in self.grid.keys():
            return_tiletypes.append(self.grid[s])
        else:
            # choosen coordinate is outside the grid so therefore is a wall
            return_tiletypes.append(TileType.wall)

        # get the southwest tiletype
        sw                  = southwest(current_coord)
        if sw in self.grid.keys():
            return_tiletypes.append(self.grid[sw])
        else:
            # choosen coordinate is outside the grid so therefore is a wall
            return_tiletypes.append(TileType.wall)

        # get the west tiletype
        w                   = west(current_coord)
        if w in self.grid.keys():
            return_tiletypes.append(self.grid[w])
        else:
            # choosen coordinate is outside the grid so therefore is a wall
            return_tiletypes.append(TileType.wall)

        return return_tiletypes

    def searchagent_position(self, agent_id):
        return self.searchagents[agent_id]

    def valid_coord(self, requested_coord):
        if (requested_coord.x < self.x) and (requested_coord.y < self.y) and (requested_coord.x >= 0) and (requested_coord.y >= 0):
            return True
        return False

    
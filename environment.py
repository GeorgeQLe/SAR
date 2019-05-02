# Copyright 2019 George Le

from collections import OrderedDict
from random import randint

import enum

from coord import Coord
from direction import Direction, resolve_direction_as_new_coord
from tiletype import TileType

class Environment:

    def __init__(self, x_max = 10, y_max = 10):
        self.x              = x_max  # specifies the max x coordinate
        self.y              = y_max  # specifies the max y coordinate
        self.grid           = OrderedDict() # a dict which holds a key-value pair of Coord to Tiletype

        self.num_agents     = 0      # holds the number of search agents that are currently in the environment grid
        self.searchagents   = list() # list of coordinates for the search agents currently in the environment grid

        self.num_targets    = 0      # holds the number of targets that are still in the environment grid
        self.target_coords  = list() # list of coordinates for the targets currently in the environment grid
        self.target_set     = False  # boolean value which tracks whether or not a target has been created in the grid
        self.total_targets  = 0      # hold the total number of targets that are in the environment grid

    def at(self, x, y):
        return self.grid[(x, y)]

    def add_search_agent(self, start_coord = Coord(0, 0), num_search_agents = 1):
        if num_search_agents >= 1:
            for i in range(num_search_agents):
                self.searchagents.append(start_coord)
            self.num_agents = num_search_agents

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

    def check_target(self, agent_id):
        potential_coord = self.searchagents[agent_id]
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
        for y in range(self.y):
            for x in range(self.x):
                pass

    def generate(self, x_max=10, y_max=10):
        self.x = x_max
        self.y = y_max

        for y in range(self.y):
            for x in range(self.x):
                random_roll = randint(1, 100)
                coord = Coord(x, y)
                if random_roll < 90:
                    self.grid[(coord.x, coord.y)] = TileType.empty
                else:
                    self.grid[(coord.x, coord.y)] = TileType.obstacle
        for target_coord in self.target_coords:
            self.grid[(target_coord.x, target_coord.y)] = TileType.target

    def clear(self):
        self.grid.clear()
        self.searchagents.clear()
        self.remove_all_targets()

    def move_searchagent(self, agent_id, direction):
        if self.valid_coord(resolve_direction_as_new_coord(direction, self.searchagents[agent_id])):
            self.searchagents[agent_id] = resolve_direction_as_new_coord(direction, self.searchagents[agent_id])
            return ((self.searchagents[agent_id].x, self.searchagents[agent_id].y), True)
        return ((self.searchagents[agent_id].x, self.searchagents[agent_id].y), False)

    def valid_coord(self, requested_coord):
        if (requested_coord.x < self.x) and (requested_coord.y < self.y) and (requested_coord.x >= 0) and (requested_coord.y >= 0):
            return True
        return False
    def get_adjacent_tiles(self, agent_id):
        return_tiletypes    = list() # list of tiletypes of the tiles adjacent to the current agent

        nw = resolve_direction_as_new_coord(Direction.NW, self.searchagents[agent_id])
        if self.valid_coord(nw):
            return_tiletypes.append(int(self.grid[(nw.x, nw.y)]))
        else:
            # choosen coordinate is outside the grid so therefore is a wall
            return_tiletypes.append(TileType.wall)

        # get the north tiletype
        n = resolve_direction_as_new_coord(Direction.N, self.searchagents[agent_id])
        if self.valid_coord(n):
            return_tiletypes.append(self.at(n.x, n.y))
        else:
            # choosen coordinate is outside the grid so therefore is a wall
            return_tiletypes.append(TileType.wall)

        # get the northeast tiletype
        ne = resolve_direction_as_new_coord(Direction.NE, self.searchagents[agent_id])
        if self.valid_coord(ne):
            return_tiletypes.append(self.at(ne.x, ne.y))
        else:
            # choosen coordinate is outside the grid so therefore is a wall
            return_tiletypes.append(TileType.wall)

        # get the east tiletype
        e = resolve_direction_as_new_coord(Direction.E, self.searchagents[agent_id])
        if self.valid_coord(e):
            return_tiletypes.append(self.at(e.x, e.y))
        else:
            # choosen coordinate is outside the grid so therefore is a wall
            return_tiletypes.append(TileType.wall)

        # get the southeast tiletype
        se = resolve_direction_as_new_coord(Direction.SE, self.searchagents[agent_id])
        if self.valid_coord(se):
            return_tiletypes.append(self.at(se.x, se.y))
        else:
            # choosen coordinate is outside the grid so therefore is a wall
            return_tiletypes.append(TileType.wall)

        # get the south tiletype
        s = resolve_direction_as_new_coord(Direction.S, self.searchagents[agent_id])
        if self.valid_coord(s):
            return_tiletypes.append(self.at(s.x, s.y))
        else:
            # choosen coordinate is outside the grid so therefore is a wall
            return_tiletypes.append(TileType.wall)

        # get the southwest tiletype
        sw = resolve_direction_as_new_coord(Direction.SW, self.searchagents[agent_id])
        if self.valid_coord(sw):
            return_tiletypes.append(self.at(sw.x, sw.y))
        else:
            # choosen coordinate is outside the grid so therefore is a wall
            return_tiletypes.append(TileType.wall)

        # get the west tiletype
        w = resolve_direction_as_new_coord(Direction.W, self.searchagents[agent_id])
        if self.valid_coord(w):
            return_tiletypes.append(self.at(w.x, w.y))
        else:
            # choosen coordinate is outside the grid so therefore is a wall
            return_tiletypes.append(TileType.wall)

        return return_tiletypes

    def searchagent_position(self, agent_id):
        return self.searchagents[agent_id]
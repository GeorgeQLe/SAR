# Copyright 2019 George Le

import enum

class SearchAgentsType(enum.Enum):
    human = 0
    drone = 1

class SearchAgents:
    def __init__(self, search_agent_type = SearchAgentsType.human):
        self.__fuel_level       = 0
        self.__max_fuel         = 0
        self.__position         = (0, 0)
        self.__steps_taken      = 0
        self.__targets_found    = 0
        self.__turns_taken      = 0
        self.__type             = search_agent_type
        
    def search(self, adjacent_tiles):
        pass

    def move(self, adjacent_tiles):
        pass
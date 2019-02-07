# Copyright 2019 George Le

import areatype
import enum

class TileType(enum.Enum):
    void        = 0
    forest      = 1
    mountain    = 2
    plain       = 3
    pond        = 4
    river       = 5
    swamp       = 6
    home        = 7

class DisregardTile():

    def __init__(self):
        self.__tiles = {  
            TileType.void       : True,
            TileType.forest     : False,
            TileType.mountain   : False,
            TileType.plain      : False,
            TileType.pond       : False,
            TileType.river      : False,
            TileType.swamp      : False,
            TileType.home       : True 
        }

    def check_tile(self, tiletype):
        return self.__tiles[tiletype]

class Tile:

    def __init__(self, falsepos = False, target = False, tiletype = TileType.void, x = 1, y = 1):
        self.__falsepos = falsepos
        self.__target   = target
        self.__tiletype = tiletype
        self.__x        = x
        self.__y        = y

    def is_target(self):
        return self.__target

    def is_falsepos(self):
        return self.__falsepos

    def tiletype(self):
        return self.__tiletype

    def set_tile_type(self, tiletype):
        self.__tiletype = tiletype

    def set_target(self, falsepos = False):
        self.__target = True
        if falsepos:
            self.__falsepos = True
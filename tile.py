# Copyright 2019 George Le

import areatype
import enum

class TileTargetInfo(enum.IntEnum):
    empty       = -1
    target      = 0
    falsepos    = 1

class TileType(enum.IntEnum):
    void        = 0.0
    home        = 0.125
    forest      = 0.25
    mountain    = 0.375
    plains      = 0.5
    pond        = 0.625
    river       = 0.875
    swamp       = 1.0

def resolve_tiletype_as_float(tiletype = TileType.void):
    return float(tiletype)

def get_tiletypes_after(index_tiletype = TileType.void):
    """
        TODO: FIX return_tiles is somehow empty
    """
    return_tiles = []
    if index_tiletype == TileType.void:
        return return_tiles

    for tiletype in TileType:
        # add to the list if the tiletype is the tiletype 
        # and after the tiletype in value
        # print("Index tile:", index_tiletype, " <= Tiletype: ", tiletype)
        if int(index_tiletype) <= int(tiletype):
            return_tiles.append(tiletype)
    return return_tiles

class DisregardTile():

    def __init__(self):
        self.__tiles = {  
            TileType.void       : True,
            TileType.forest     : False,
            TileType.mountain   : False,
            TileType.plains     : False,
            TileType.pond       : False,
            TileType.river      : False,
            TileType.swamp      : False,
            TileType.home       : True
        }

    def check_tile(self, tiletype):
        # print("Disregard tile", tiletype, ":", self.__tiles[tiletype])
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

    def coord(self):
        return (self.__x, self.__y)

    def tiletype(self):
        return self.__tiletype

    def set_tile_type(self, tiletype):
        self.__tiletype = tiletype

    def set_target(self, falsepos = False):
        self.__target = True
        if falsepos:
            self.__falsepos = True
# Copyright 2019 George Le
import enum

class TileType(enum.IntEnum):
    wall        = -2
    obstacle    = -1
    empty       = 0
    target      = 1
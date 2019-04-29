import enum

from coord import Coord

class Direction(enum.IntEnum):
    NW  = 1
    N   = 2
    NE  = 3
    E   = 4
    SE  = 5
    S   = 6
    SW  = 7
    W   = 8

def update_coords(coord = Coord(0, 0), direction = Direction()):
    if direction == Direction.NW:
        new_coord = Coord(coord.x -1, coord.y + 1)
    elif direction == Direction.N:
        new_coord = Coord(coord.x, coord.y + 1)
    elif direction == Direction.NE:
        new_coord = Coord(coord.x + 1, coord.y + 1)
    elif direction == Direction.E:
        new_coord = Coord(coord.x + 1, coord.y)
    elif direction == Direction.SE:
        new_coord = Coord(coord.x + 1, coord.y - 1)
    elif direction == Direction.S:
        new_coord = Coord(coord.x, coord.y - 1)
    elif direction == Direction.SW:
        new_coord = Coord(coord.x - 1, coord.y - 1)
    elif direction == Direction.W:
        new_coord = Coord(coord.x - 1, coord.y)
 
    return new_coord

def northwest(coord = Coord(0, 0)):
    return Coord(coord.x - 1, coord.y + 1)

def north(coord = Coord(0, 0)):
    return Coord(coord.x, coord.y + 1)

def northeast(coord = Coord(0, 0)):
    return Coord(coord.x + 1, coord.y + 1)

def east(coord = Coord(0, 0)):
    return Coord(coord.x + 1, coord.y)

def southeast(coord = Coord(0, 0)):
    return Coord(coord.x + 1, coord.y - 1)

def south(coord = Coord(0, 0)):
    return Coord(coord.x, coord.y - 1)

def southwest(coord = Coord(0, 0)):
    return Coord(coord.x - 1, coord.y - 1)

def west(coord = Coord(0, 0)):
    return Coord(coord.x - 1, coord.y)

def resolve_decision_as_direction(decision):
    if decision < 0.125:
        return Direction.NW
    elif decision < 0.25:
        return Direction.N
    elif decision < 0.375:
        return Direction.NE
    elif decision < 0.5:
        return Direction.E
    elif decision < 0.625:
        return Direction.SE
    elif decision < 0.75:
        return Direction.S
    elif decision < 0.875:
        return Direction.SW
    elif decision < 1.0:
        return Direction.W
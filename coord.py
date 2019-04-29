class Coord:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Coord):
            return False
        if (self.x == other.x) and (self.y == other.y):
            return True
        return False
    
    def __ne__(self, other):
        if isinstance(other, Coord):
            return False
        if (self.x != other.x) or (self.y != other.y):
            return True
        return False
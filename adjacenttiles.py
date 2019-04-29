# !!! THIS IS A DEFUNCT FILE

# from areatype import AreaTileProbabilities, AreaType, generate_random_tile
# from tile import DisregardTile, get_tiletypes_after, resolve_tiletype_as_float, TileType

# import random

# class AdjacentTiles:

#     def __init__(self):
#         """-----------------------------------------------------------
#             There are a total of 8 tiles adjacent to the caller tile.
#             Initially, these adjacent tiles are set to void which if
#             used should be disregarded.
#         -----------------------------------------------------------"""
#         self.NW = TileType.void
#         self.N  = TileType.void
#         self.NE = TileType.void
#         self.E  = TileType.void
#         self.SE = TileType.void
#         self.S  = TileType.void
#         self.SW = TileType.void
#         self.W  = TileType.void

#     def __add_probability(self, return_probabilities, tiletype, add_probability):
#         """---------------------------------------------------------------------------------

#             Adds a value to the probability to the dict that stores the key-value pair:
#             { tiletype : probability } 
        
#         ---------------------------------------------------------------------------------"""
#         if tiletype != TileType.void and tiletype != TileType.home:
#             # print("Get tiletype after:", tiletype, " : ", get_tiletypes_after(tiletype))
#             for index_types in get_tiletypes_after(tiletype):
#                 return_probabilities[index_types] += add_probability
#         return return_probabilities

#     def __check_tile(self):
#         """---------------------------------------------------------------------------------

#             This function checks each of the adjacent tiles to the center tile to determine
#             if any of the adjacent tiles' tiletype should be disregarded. Most common uses
#             for this function is when the grid is being initialized and there are "null"
#             tiles on the grid with void tiles and when the center tile is on the edges of
#             the grid where an adjacent tile may not exist and thus must be disregarded.
#             This function returns the modifier to the probability of a generated tile.
        
#         ---------------------------------------------------------------------------------"""
#         disregard       = DisregardTile()
#         disregarded_num = 0
        
#         # the following determines if the adjacent tiles should be disregarded (if
#         # they are void or home)
#         if disregard.check_tile(self.NW):
#             disregarded_num += 1
#         if disregard.check_tile(self.N):
#             disregarded_num += 1
#         if disregard.check_tile(self.NE):
#             disregarded_num += 1
#         if disregard.check_tile(self.E):
#             disregarded_num += 1
#         if disregard.check_tile(self.SE):
#             disregarded_num += 1
#         if disregard.check_tile(self.S):
#             disregarded_num += 1
#         if disregard.check_tile(self.SW):
#             disregarded_num += 1
#         if disregard.check_tile(self.W):
#             disregarded_num += 1

#         # this is for the first two tiles, to return zero
#         if disregarded_num == 8:
#             return 0.0
#         # print("Disregard num:", 8 / (8 - disregarded_num))
#         return 8 / (8 - disregarded_num)

#     def __count_tile_probabilities(self, areatype):
#         """---------------------------------------------------------------------------------

#             This function determines how much each tiletype is worth which is used to
#             calculate the probability for each tiletype. It bases any modification to the
#             probabilities on how many of a certain tiletype exists within the adjacent tiles
#             of the center tile and whether the tiletype is not to be included in the 
#             simulation.
        
#         ---------------------------------------------------------------------------------"""
#         individual_probability_modifier = self.__check_tile()
#         return_probabilities = AreaTileProbabilities().get_values(areatype=areatype)
#         # print("Return probabilities: ", return_probabilities)

#         # checks to see if the adjacent tiles are relevant (if this is the first time,
#         # )
#         # set all of the adjacent tiles' probabilities to 0.0
#         # for tiletype in TileType:
#         #     return_probabilities[tiletype] = 0.0
        
#         if individual_probability_modifier == 0:
#             return return_probabilities
        
#         # print("NW: ", self.NW, ", N: ", self.N, ", NE: ", self.NE, ", E: ", self.E, ", SE: ", self.SE, ", S: ", self.S, ", SW: ", self.SW, ", W: ", self.W)

#         # modifies the probabilities for each of the eight adjacent tiles
#         return_probabilities = self.__add_probability(return_probabilities, self.NW, individual_probability_modifier)
#         # print("NW")
#         # print("NW: ", self.NW, ", N: ", self.N, ", NE: ", self.NE, ", E: ", self.E, ", SE: ", self.SE, ", S: ", self.S, ", SW: ", self.SW, ", W: ", self.W)
#         return_probabilities = self.__add_probability(return_probabilities, self.N, individual_probability_modifier)
#         # print("N")
#         # print("NW: ", self.NW, ", N: ", self.N, ", NE: ", self.NE, ", E: ", self.E, ", SE: ", self.SE, ", S: ", self.S, ", SW: ", self.SW, ", W: ", self.W)
#         return_probabilities = self.__add_probability(return_probabilities, self.NE, individual_probability_modifier)
#         # print("NE")
#         # print("NW: ", self.NW, ", N: ", self.N, ", NE: ", self.NE, ", E: ", self.E, ", SE: ", self.SE, ", S: ", self.S, ", SW: ", self.SW, ", W: ", self.W)
#         return_probabilities = self.__add_probability(return_probabilities, self.E, individual_probability_modifier)
#         # print("E")
#         # print("NW: ", self.NW, ", N: ", self.N, ", NE: ", self.NE, ", E: ", self.E, ", SE: ", self.SE, ", S: ", self.S, ", SW: ", self.SW, ", W: ", self.W)
#         return_probabilities = self.__add_probability(return_probabilities, self.SE, individual_probability_modifier)
#         # print("SE")
#         # print("NW: ", self.NW, ", N: ", self.N, ", NE: ", self.NE, ", E: ", self.E, ", SE: ", self.SE, ", S: ", self.S, ", SW: ", self.SW, ", W: ", self.W)
#         return_probabilities = self.__add_probability(return_probabilities, self.S, individual_probability_modifier)
#         # print("S")
#         # print("NW: ", self.NW, ", N: ", self.N, ", NE: ", self.NE, ", E: ", self.E, ", SE: ", self.SE, ", S: ", self.S, ", SW: ", self.SW, ", W: ", self.W)
#         return_probabilities = self.__add_probability(return_probabilities, self.SW, individual_probability_modifier)
#         # print("SW")
#         # print("NW: ", self.NW, ", N: ", self.N, ", NE: ", self.NE, ", E: ", self.E, ", SE: ", self.SE, ", S: ", self.S, ", SW: ", self.SW, ", W: ", self.W)
#         return_probabilities = self.__add_probability(return_probabilities, self.W, individual_probability_modifier)
#         # print("W")
#         # print("NW: ", self.NW, ", N: ", self.N, ", NE: ", self.NE, ", E: ", self.E, ", SE: ", self.SE, ", S: ", self.S, ", SW: ", self.SW, ", W: ", self.W)
#         return return_probabilities 

#     # this function allows for the environment class to load the AdjacentTiles class with the current tile's
#     # adjacent tiles
#     def add_tiles(self, NW = TileType.void, N = TileType.void, NE = TileType.void, E = TileType.void,
#                  SE = TileType.void, S = TileType.void, SW = TileType.void, W = TileType.void):
#         """---------------------------------------------------------------------------------

#             This function serves as a setter function for this AdjacentTiles class
        
#         ---------------------------------------------------------------------------------"""
#         self.NW = NW
#         self.N  = N
#         self.NE = NE
#         self.E  = E
#         self.SE = SE
#         self.S  = S
#         self.SW = SW
#         self.W  = W

#     # this is the main workhorse of the AdjacentTiles class
#     def generate_tiletype_from_adj(self, areatype = AreaType.default):
#         """-----------------------------------------------------------------------------------

#             This function determines the probabilities that each tiletype have of being
#             returned by this function to be the assigned as the tiletype for the center tile.
        
#         ----------------------------------------------------------------------------------"""
#         temp = self.__count_tile_probabilities(areatype)
#         random_roll = random.randint(1, 111)
#         # print("Random roll:", random_roll)
#         # print("Temp:", temp)
#         if random_roll >= 100:
#             # print("Generate random tile")
#             return generate_random_tile(areatype)
#         for probability in temp.keys():
#             # print("Generate from existing")
#             # print("Probability:", probability, ":", temp[probability])
#             random_roll = random.randint(0, 11)
#             if temp[probability] > random_roll:
#                 # print("Selected:", probability)
#                 return probability
#         return generate_random_tile(areatype)

#     def listify(self):
#         return_list = list()
        
#         return_list.append(resolve_tiletype_as_float(self.NW)) 
#         return_list.append(resolve_tiletype_as_float(self.N))
#         return_list.append(resolve_tiletype_as_float(self.NE))
#         return_list.append(resolve_tiletype_as_float(self.E))
#         return_list.append(resolve_tiletype_as_float(self.SE))
#         return_list.append(resolve_tiletype_as_float(self.S))
#         return_list.append(resolve_tiletype_as_float(self.SW))
#         return_list.append(resolve_tiletype_as_float(self.W))
        
#         return return_list
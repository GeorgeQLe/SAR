# Copyright 2019 George Le

import np

class NeuralNetwork:
    # To construct a neural network, the user will need to pass in the array of 
    # input values for the input layer of the neural network as well as 
    def __init__(self, x, y):
        self.input      = x
        self.weights1   = np.random.rand(self.input.shape[1], )

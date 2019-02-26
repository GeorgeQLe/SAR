# Copyright 2019 George Le

class Neuron:
    
    def __init__(self, weight = 0.0):
        self.__weight   = weight

class NeuralNetworkInputs:
    """-----------------------------------------------------------------------------

        This class is that is the container and interface for the neural networks'
        inputs. The aim is that this class will serve as the base class so that
        the input can be easily reformatted.

    -----------------------------------------------------------------------------"""
    def __init__(self):
        self.__inputs        = list()
        self.__good_inputs   = False

    def set_inputs(self, inputs):
        self.__inputs       = self.__verify_inputs(inputs)
        self.__good_inputs  = True

    def __verify_inputs(self, inputs):
        for input in inputs:
            if not isinstance(input, int):
                return []
        return inputs

class NeuralNetwork:
    """-----------------------------------------------------------------------------

        This class is the base class for neural networks; it includes the weights,
        biases, and output.

    -----------------------------------------------------------------------------"""

    # To construct a neural network, the user will need to pass in the array of 
    # input values for the input layer of the neural network
    def __init__(self, inputs = NeuralNetworkInputs, num_layers = 3):
        self.__input            = inputs
        self.__good_neural_net  = False
        self.__layers           = { int : list(Neuron) }
        self.__num_layers       = num_layers

    def define_layers(self, num_layers):
        if num_layers > 3:
            self.__num_layers = num_layers

    def define_size_of_layer(self, index = 0, size = 1):
        if index > 0 and index < self.__num_layers:
            self.__layers[index].append(Neuron())
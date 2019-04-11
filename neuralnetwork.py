# # Copyright 2019 George Le

# from collections import OrderedDict
from math import exp
from random import uniform

def sigmoid(input):
    # print("Sigmoid:", 1.0 / (1.0 + exp(input * -1)))
    return (1.0 / (1.0 + exp(input * -1)))

class NeuralNetwork:
    def __init__(self, bias = 0, num_layers = 0, layers_info = dict(), num_weights = 0, weights = list()):
        if num_layers == 0:
            return
        if num_weights == 0:
            return
        if len(layers_info.keys()) != num_layers - 1:
            return

        self.__bias                 = bias
        self.__output               = 0
        self.__layers_info          = layers_info # this is a dict that holds a key-value pair 
                                                  # => (Key - layer index) : (Value - Tuple (number of neuron weights, number of neurons))
        self.__num_layers           = num_layers
        self.__num_weights          = num_weights
        
        temp_weights                = weights
        if len(weights) == 0:
            temp_weights.clear()
            for i in range(self.__num_weights):
                temp_weights.append(round(uniform(0.0, 1.0), 2))
        self.__weights              = temp_weights

    def __evaluate_neural_net_layer(self, layerNi = list(), weightsGi = list()):
        if (len(layerNi) != len(weightsGi)):
            return -1.0
        else:
            sum                     = 0
            for j in range(len(layerNi)):
                sum += (layerNi[j] * weightsGi[j])
            # print("Sum:", sum)
            return sigmoid(sum)

    def evaluate(self, inputN1 = list()):
        # tracks the current weights index
        current_index       = 0
        # tracks the outputs of a layer to be
        # passed in as the input into the next layer
        inputNi             = inputN1
        # tracks the results of the neural network
        # to be returned by this function
        result              = 0
        # for each of the layers of the neural network
        for layer_index in range(self.__num_layers - 1):
            # inputs to be passed into the new layer evalations
            passed_inputs = list(inputNi)
            # clears the inputs container so that the inputs to the next layer
            # can be stored
            inputNi.clear()
            # for each of the neurons of the neural network
            for i in range(self.__layers_info[layer_index][1]):
                # create a temporary container for the neuron weights that will be
                # used in the evaluation
                GAi             = list()
                # gather all of the neuron weights for a particular layer
                for j in range(self.__layers_info[layer_index][0]):
                    # grab the weight at the current weights counter index
                    GAi.append(self.__weights[current_index])
                    # move the weights counter along
                    current_index+=1
                inputNi.append(self.__evaluate_neural_net_layer(passed_inputs, GAi))
            # print("InputNi after layer evaluation:", inputNi)
        result = inputNi[0]
        
        return result

    def get_weights(self):
        return self.__weights
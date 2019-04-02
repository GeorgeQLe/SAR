# # Copyright 2019 George Le

# from collections import OrderedDict
from math import exp
from random import uniform

def sigmoid(input):
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
        for layer_index in range(self.__num_layers):
            # inputs to be passed into the new layer evalations
            passed_inputs = inputNi
            # clears the inputs container so that the inputs to the next layer
            # can be stored
            inputN1.clear()
            # for each of the neurons of the neural network
            for i in range(self.__layers_info[1]):
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
        result = inputNi[0]
        
        return result

    def get_weights(self):
        return self.__weights

# class NeuralNetworkInputs:
#     """--------------------------------------------------------------------------

#         This class is the container and interface for the neural networks'
#         inputs. The aim is that this class will serve as the base class so that
#         the input can be easily reformatted.

#     --------------------------------------------------------------------------"""
#     def __init__(self, inputs = list()):
#         # print("In Creating Neural Network Inputs")
#         # print("Inputs:", inputs)
#         self.__good_inputs   = False
#         self.__inputs        = inputs
#         self.__num_of_inputs = len(inputs)

#         if len(self.__verify_inputs(self.__inputs)) > 0:
#             self.__good_inputs = True
#             # print("Good inputs")

#     def __verify_inputs(self, inputs):
#         """---------------------------------------------------------------------
#             This function checks to see if the inputs added into this class
#             are floating point values. If the list of inputs are verified to
#             have only floats, then the inputs are returned by this function.
#             Otherwise if there is an issue with the inputs, then an empty list
#             is returned.
#         ---------------------------------------------------------------------"""
#         if isinstance(inputs, list):
#             for input in inputs:
#                 if not isinstance(input, float):
#                     return []
#         else:
#             return []
#         return inputs

#     @property
#     def inputs(self):
#         if self.__good_inputs:
#             return self.__inputs
#         return []

#     @inputs.setter
#     def inputs(self, inputs):
#         self.__inputs       = self.__verify_inputs(inputs)

# class NeuralNetworkWeights:
#     """-----------------------------------------------------------------------------

#         This class holds and tracks all of the weights of the neural network in 
#         two separate OrderDict data structures.

#         The layers_size ordered dictionary holds the key-value pairs of:
#         (layer index : layer size). This parameter will be copied by this 
#         class's member with the same name and will allow for the neural
#         network to ensure that the neural network architecture is abided.

#         The weights ordered dictionary holds the key-value pairs of:
#         (neuron id : list(weights)). This member variable is used to load
#         the output weights into the corresponding neuron.
#     -----------------------------------------------------------------------------"""
#     def __init__(self, layers_size = OrderedDict(), num_of_weights = 1, weights = OrderedDict()):
#         # print("In Creating Neural Network Weights")
#         # print("Weights:", weights)
#         self.__good_layer_info  = False             # the status of the information about the layers
#         self.__good_weights     = False             # the status of the weights
#         self.__layers_size      = layers_size       # layer index (int) : layer size (int)
#         self.__num_of_weights   = num_of_weights    # total number of weights 
#         self.__weights          = weights           # neuron id (int) : list of weights (floats)

#         if len(self.__verify_weights(self.__weights)) > 0:
#             self.__good_weights = True
#             # print("Good weights")
#         if len(self.__verify_layer_info(self.__layers_size)) > 0:
#             self.__good_layer_info = True
#             # print("Good layer size")

#     def __verify_layer_info(self, layer_info):
#         if isinstance(layer_info, OrderedDict):
#             for layer_index in layer_info.keys():
#                 if not isinstance(layer_index, int):
#                     return OrderedDict()
#                 elif not isinstance(layer_info[layer_index], int):
#                     return OrderedDict()
#         else:
#             return OrderedDict()
#         return layer_info

#     def __verify_weights(self, weights):
#         """---------------------------------------------------------------------
#             This function checks to see if the weights added into this class
#             are floating point values. If the list of weights are verified to
#             have only floats, then the weights are returned by this function.
#             Otherwise if there is an issue with the weights, then an empty list
#             is returned. 
#         ---------------------------------------------------------------------"""
#         if isinstance(weights, OrderedDict):
#             for input in weights.keys():
#                 if not isinstance(input, int):
#                     print("Problem with keys")
#                     return OrderedDict()
#                 elif not isinstance(weights[input], list):
#                     print("Problem with the neuron weights container")
#                     return OrderedDict()
#                 if len(weights) > 0:
#                     for weight in weights[input]:
#                         if not isinstance(weight, float):
#                             print("Problem with the neuron weight")
#                             return OrderedDict()
#         else:
#             return OrderedDict()
#         return weights

#     def check_weights(self):
#         if self.__good_layer_info == True and self.__good_weights == True:
#             return True
#         return False

#     @property
#     def layer_size(self):
#         if self.__good_layer_info:
#             return self.__layers_size
#         return []

#     @property
#     def weights(self):
#         if self.__good_weights:    
#             return self.__weights
#         return []

#     @layer_size.setter
#     def layer_size(self, layer_size):
#         self.__layers_size  = self.__verify_layer_info(layer_size)
#         if len(self.__layers_size) > 0:
#             self.__good_layer_info = True

#     @weights.setter
#     def weights(self, weights):
#         self.__weights      = self.__verify_weights(weights)
#         if len(self.__weights) > 0:
#             self.__good_weights = True

# class NeuronInputs:
#     """-----------------------------------------------------------------------------

#         This class is that is the container and interface for the neuron's inputs. 
#         The aim is that this class will serve as the base class so that the input 
#         can be easily reformatted.

#     -----------------------------------------------------------------------------"""
#     def __init__(self, inputs = list()):
#         self.__good_inputs      = False
#         self.__inputs           = inputs
#         self.__num_of_inputs    = len(inputs)

#         if len(self.__verify_inputs(self.__inputs)) > 0:
#             self.__good_inputs = True
#             # print("Good inputs")

#     def __verify_inputs(self, inputs):
#         """---------------------------------------------------------------------
#             This function checks to see if the inputs added into this class
#             are floating point values. If the list of inputs are verified to
#             have only floats, then the inputs are returned by this function.
#             Otherwise if there is an issue with the inputs, then an empty list
#             is returned.
#         ---------------------------------------------------------------------"""
#         if isinstance(inputs, list):
#             for input in inputs:
#                 if not isinstance(input, float):
#                     return []
#         elif isinstance(inputs, float):
#             return inputs
#         else:
#             return []
#         return inputs

#     @property
#     def inputs(self):
#         if self.__good_inputs:
#             return self.__inputs
#         return []

#     @inputs.setter
#     def inputs(self, inputs):
#         self.__inputs       = self.__verify_inputs(inputs)

# class NeuronWeights:
#     """-----------------------------------------------------------------------------

#         This class is that is the container and interface for the neuron's weights. 
#         The aim is that this class will serve as the base class so that the weights 
#         can be easily reformatted.

#     -----------------------------------------------------------------------------"""
#     def __init__(self, weights = list()):
#         self.__good_weights     = False

#         if isinstance(weights, list):
#             self.__num_of_weights   = len(weights)
#             self.__weights          = weights
#         else:
#             return

#         if len(self.__verify_weights(self.__weights)) > 0:
#             self.__good_weights = True
#             # print("Good weights")

#     def __verify_weights(self, weights):
#         """---------------------------------------------------------------------
#             This function checks to see if the weights added into this class
#             are floating point values. If the list of weights are verified to
#             have only floats, then the weights are returned by this function.
#             Otherwise if there is an issue with the weights, then an empty list
#             is returned. 
#         ---------------------------------------------------------------------"""
#         if isinstance(weights, list):
#             for input in weights:
#                 if not isinstance(input, float):
#                     return []
#         else:
#             return []
#         return weights

#     def check_weights(self):
#         if self.__good_weights == True:
#             return True
#         return False

#     def create_from_neural_network_weights(self, layers_size = OrderedDict()):
#         incoming_weights = OrderedDict()
#         for layer in layers_size.keys():
#             for i in range(layers_size[layer]):
#                 incoming_weights[i] = self.__weights
#         print(incoming_weights)
#         return NeuralNetworkWeights(layers_size, self.__num_of_weights, incoming_weights)

#     @property
#     def weights(self):
#         if self.__good_weights:    
#             return self.__weights
#         return []

#     @weights.setter
#     def weights(self, weights):
#         self.__weights      = self.__verify_weights(weights)
#         if len(self.__weights) > 0:
#             self.__good_weights = True

# class Neuron:
#     """-----------------------------------------------------------------------------

#         This class is that is the container and interface for the neural networks'
#         inputs. The aim is that this class will serve as the base class so that
#         the input can be easily reformatted.

#     -----------------------------------------------------------------------------"""
#     def __init__(self, ID = 0, num_of_connections = 1, num_of_weights = 1, weights = NeuronWeights()):
#         # print("Create Neuron")
#         # print("ID:", ID, "Number of connections:", num_of_connections, "Number of weights:", num_of_weights)
#         # print("Weights:", weights.weights)
#         self.__ID                   = ID                    # the ID for the neuron
#         self.__num_of_connections   = num_of_connections    # the number of neurons that receive the
#                                                             # output and weights of this neuron
#         self.__num_of_weights       = num_of_weights        # the number of weights held by the neuron
#         self.__outputs              = 0.0                   # the result of the function held in the Neuron 
#                                                             # that will be passed to all of the neurons in 
#                                                             # the next layer (Feedforward)
#         self.__output_weights       = NeuronWeights()
#         # print("Weights:", weights)
#         if isinstance(weights, NeuronWeights):
#             self.__output_weights       = weights
#         elif isinstance(weights, list):
#             self.__output_weights       = NeuronWeights(weights=weights)

#     def __sigmoid(self, input):
#         return (1.0 / (1.0 + exp(input * -1)))

#     def __str__(self):
#         return str(self.__output_weights)

#     def evaluate_neuron(self, inputs = NeuronInputs(), input_weights = NeuronWeights(), bias = 0.0):
#         sum = 0.0
#         # If the neuron is in the input layer, then the input is a single float
#         # and there are no weights.
#         # print(len(input_weights.weights))
#         # print(isinstance(inputs, float))
#         if len(input_weights.weights) == 0 and isinstance(inputs, float) == True:
#             sum = inputs
#         # For the hidden and output layer, the sum is assigned the value of the input multipied 
#         # by each of the input weights sum = wi * xi, where wi is the weight at the i'th position
#         # and xi is the input in the i'th position.
#         else:
#             # print("Neuron #", self.__ID, ":") 
#             weight          = input_weights.weights
#             neuron_inputs   = inputs.inputs
#             for i in range(len(weight)):
#                 # print(weight[i], "*", neuron_inputs[i], end="=")
#                 sum = round(weight[i] * neuron_inputs[i], 4)
#                 # print(sum)
#         # sum - bias
#         sum -= bias
#         self.__output = round(self.__sigmoid(sum), 4)
#         return self.__output

#     def ID(self):
#         return self.__ID
#     def get_num_of_connections(self):
#         return self.__num_of_connections
#     def get_num_of_weights(self):
#         return self.__num_of_weights    
#     def get_output(self):
#         return self.__output
#     def get_output_weights(self):
#         return self.__output_weights
#     def set_output_weights(self, weights = NeuronWeights()):
#         if weights.check_weights() == True:
#             self.__output_weights = weights

# class NeuralNetwork:
#     """-----------------------------------------------------------------------------

#         This class is the base class for neural networks;

#     -----------------------------------------------------------------------------"""
#     # To construct a neural network, the user will need to pass in the array of 
#     # input values for the input layer of the neural network
#     def __init__(self, inputs = NeuralNetworkInputs(), num_layers = 3):
#         # print("Creating Neural Network")
#         self.__input            = inputs
#         self.__layers           = OrderedDict() # this OrderedDict() holds key-value pairs:
#                                                 # (layer index : list(Neuron))
#         self.__layers_size      = OrderedDict() # this OrderedDirt() holds key-value pairs:
#                                                 # (layer index : layer size) 
#         self.__neuron_ID        = 1
#         self.__num_layers       = num_layers
#         self.__num_neurons      = 0
#         self.__num_weights      = 0

#     def __insert_weights(self, ID = 0, weights = NeuronWeights()):
#         neuron_index = find_neuron_id_in_layer(self.__layers_size, ID)
#         self.__layers[neuron_index][ID - self.__layers_size[neuron_index] - 1].set_output_weights(weights)

#     def create_layer(self, index = 0, size = 1, size_of_next_layer = 0, last_layer = False):
#         # print("Creating layer #", index)
#         if index >= 0 and index < self.__num_layers and size > 0:
#             # temp variable that stores all of the neurons for 
#             # a particular layer 
#             neurons                         = list()

#             # record the range of IDs in a layer of the neural network
#             if index > 0:
#                 self.__layers_size[index]   = self.__layers_size[index - 1] + size
#             elif index == 0:
#                 self.__layers_size[index]   = size

#             # add all of the neurons of a certain layer
#             for i in range(size):
#                 input_weights = list()
#                 for j in range(size_of_next_layer):
#                     input_weights.append(round(uniform(0.0, 1.0), 2))
#                 # print("Input weights", input_weights)
#                 neurons.append(Neuron(ID = self.__neuron_ID, num_of_connections=size_of_next_layer, num_of_weights=len(input_weights), weights = NeuronWeights(input_weights)))
#                 self.__neuron_ID += 1
#             # add the list of neurons to the neural network
#             self.__layers[index] = neurons

#             if last_layer == True:
#                 for size in self.__layers_size:
#                     self.__num_neurons += size
#                 # for each layer in the neural network
#                 for layer_index in self.__layers.keys():
#                     # for each neuron in the layer
#                     for neuron in self.__layers[layer_index]:
#                         self.__num_weights += neuron.get_num_of_weights()
#             # print("Layers size:", self.__layers_size)
#             # print("Number of weights in the neural network:", self.__num_weights)

#     def evaluate(self, inputs = NeuralNetworkInputs()):
#         if len(inputs.inputs) != len(self.__layers[0]):
#             print("Not enough inputs")
#             return

#         for layer_index in self.__layers.keys():
#             for neuron in self.__layers[layer_index]:
#                 # for the input layer
#                 if layer_index == 0:
#                     neuron.evaluate_neuron(inputs= inputs.inputs[neuron.ID() - 1])
#                 else:
#                     # If the current layer is not the input layer, then collect the weights from the previous
#                     # layer for the current neuron. Do the same for the outputs from the previous neuron -> inputs
#                     # for the current layer's neurons.
#                     list_weights    = list()
#                     list_inputs     = list()
#                     for prev_neuron in self.__layers[layer_index - 1]:
#                         # print("Prev neuron weights:", prev_neuron.get_output_weights().weights)
#                         list_weights.append(prev_neuron.get_output_weights().weights[neuron.ID() - self.__layers_size[layer_index] - 1])
#                         list_inputs.append(prev_neuron.get_output())
#                     # print("Prev neuron outputs:", list_inputs)
#                     input_weights = NeuronWeights(list_weights)
#                     neuron_inputs = NeuronInputs(list_inputs)
#                     # print("Neuron ID:", neuron.ID())
#                     neuron.evaluate_neuron(inputs= neuron_inputs, input_weights= input_weights)
#         neural_network_output = list()
#         for neuron in self.__layers[2]:
#             neural_network_output.append(self.__layers[2][neuron.ID() - self.__layers_size[2] - 1].get_output())
#         # print("Number of neurons", self.__num_neurons)
#         return neural_network_output

#     def get_weights(self):
#         # is an ordereddict that has a key-value pair
#         # neuron_id (int) : list(neuron_weights (float))
#         weights = OrderedDict()
        
#         # for each layer in the neural network
#         for layer_index in self.__layers.keys():
#             # for each neuron in the layer
#             for neuron in self.__layers[layer_index]:
#                 weights[neuron.ID()] = neuron.get_output_weights().weights
#         return_weights = NeuralNetworkWeights(layers_size= self.__layers_size, num_of_weights= self.__num_weights, weights= weights)
#         return return_weights

#     def override_weights(self, weights = NeuralNetworkWeights()):
#         """
#             This function will take in two structured dictionaries that will create the
#             structure of a new neural network. This function will override an old neural
#             network.
            
#         """
#         if weights.check_weights() == False:
#             return
#         # update the neural network to the new neural network size and structure
#         self.__layers_size  = weights.layer_size
#         self.__num_layers = max(self.__layers_size, key= int)

#         # replaces the weights for each neuron of the neural network
#         for neuron_id in weights.weights.keys():
#             self.__insert_weights(neuron_id, NeuronWeights(weights.weights[neuron_id]))

#     def search_neuron_by_ID(self, ID):
#         neuron_index    = find_neuron_id_in_layer(self.__layers_size, ID)
#         return self.__layers[neuron_index][ID - self.__layers_size[neuron_index - 1] - 1]
        
#     def search_neuron_weights_by_ID(self, ID):

#         neuron_index    = find_neuron_id_in_layer(self.__layers_size, ID)
#         return_weights  = { ID : self.__layers[neuron_index][ID - self.__layers_size[neuron_index - 1] - 1].get_output_weights().weights }

#         # is a tuple containing a neuron_id (int) and a list of weights (double) belonging to the 
#         # corresponding neuron with the neuron_id   
#         return return_weights

#     def set_num_layers(self, num_layers):
#         if num_layers > 3:
#             self.__num_layers = num_layers

# def find_neuron_id_in_layer(layer_info = OrderedDict, neuron_id = 0):
#     for layer_index in layer_info.keys():
#         if neuron_id <= (layer_info[layer_index]):
#             return layer_index